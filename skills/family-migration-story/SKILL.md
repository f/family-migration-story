---
name: family-migration-story
description: Turn family tree data (Turkish e-Devlet Alt-Üst Soy Belgesi PDF, a GEDCOM export from Ancestry/MyHeritage/FamilySearch, or a typed list of ancestors) into a deeply researched family history. Every ancestor's birthplace is researched in its own time from historical archives, census and yearbook data and academic papers, the findings go into a cited HTML report, and the result becomes a narrated documentary video on an animated map (Remotion, local open-source TTS; natural Turkish voice via yazgi-tts). Use this skill whenever someone shares a soy ağacı, family tree, ancestry or genealogy data and wants to know where their family came from, what their ancestors' villages were like, why they migrated (göç, mübadele, muhacir, exchange, emigration), or wants a family history report, story, map animation or video, even if they only say "research my family tree" or "soyağacımı araştır".
model: claude-opus-5-5
effort: xhigh
---

# Family migration story

From a family tree to (1) a research dossier with sources, (2) an HTML report, (3) a narrated map video. Each phase produces files the next one reads, so the work can stop and resume at any phase.

```
<work>/
  familytree.json            phase 0: the family, normalised
  research/targets.json      phase 1: places x years to research
  research/dossier.json      phase 1: places, claims, world events, sources
  research/images.tsv        phase 1: Commons images for the video
  report.html                phase 2
  video/                     phases 3-4: Remotion project (story.json + data + narration)
  video/out/<name>.mp4       phase 4: 1080p and 720p deliverables
```

`$SKILL` means this skill's directory. Scripts are plain Python 3 / Node / zsh; run Python with `-I`.

## Privacy: names stay on this machine

Family trees hold names, dates and places of real, partly living people.
- Research queries, API calls, page fetches and image searches contain **places, years and topics only**, never a person's name. The research scripts are built that way; keep your WebSearch/WebFetch queries the same.
- Speech synthesis and speech recognition run locally (yazgi-tts, macOS `say`, faster-whisper). Don't send narration to a cloud TTS.
- The report and the video contain family names. Keep them as local files; publish or upload only if the user asks.
- Name-based record searches (passenger lists, archive name indexes, FamilySearch) need the user's explicit OK first. See the end of `references/archives-by-region.md`.

## Phase 0: Intake

1. Get the tree into `familytree.json` (format: `references/data-formats.md` §1):
   - e-Devlet PDF: `uv run --with pypdf python -I $SKILL/scripts/import_edevlet.py soyagaci.pdf familytree.json`
   - GEDCOM: `python3 -I $SKILL/scripts/import_gedcom.py tree.ged familytree.json [--subject @I12@]`
   - anything else (spreadsheet, photo, text): write the JSON by hand, one person per entry with `father`/`mother` links.
2. `python3 -I $SKILL/scripts/tree_tool.py validate familytree.json`, then `summary` to see the generations. Resolve `review` items and ERRORs with the user; WARNs about implausible parent ages are usually register artefacts worth mentioning.
3. Ask for what isn't in the data and only the family knows: stories about origins, a ship, a trunk, why they moved. Record them in `oral_history`. One short question is enough; don't block on it.
4. Settle the deliverables and language. The default is the report plus the video, in the user's language; Turkish narration uses yazgi-tts.

## Phase 1: Deep research (the heart of it)

Read `references/research-playbook.md` before starting, and `references/archives-by-region.md` for the regions involved.

1. `python3 -I $SKILL/scripts/tree_tool.py targets familytree.json research/targets.json` lists each place with the years the family was there.
2. For each place, in the order the family lived in them:
   - `python3 -I $SKILL/scripts/research/places.py "<place>"`: identity, coordinates, names in every language, admin history.
   - `python3 -I $SKILL/scripts/research/papers.py "<place> <topic>" "<old name> <period>" …`: journal articles and theses (OpenAlex, Crossref, DergiPark).
   - `python3 -I $SKILL/scripts/research/archives.py "<query>" --links`: digitised books, yearbooks and photos, plus links into archives without APIs (Ottoman archive catalogue, HathiTrust, Library of Congress, Gallica, national libraries).
   - WebSearch and WebFetch for what the APIs miss. Read the local-language sources and the PDFs, and cite pages.
   - Answer the playbook's ten questions and write each finding as a claim with sources and a confidence grade in `research/dossier.json`.
3. Build the world-events spine (10-20 dated events touching the family's places) and the "other side of the mirror" for every forced migration.
4. Images: `python3 -I $SKILL/scripts/research/commons_search.py 6 "<place> 1900" …` → choose free-licensed period images that really show the place, then list them in `research/images.tsv`.
5. With more than ~6 places, research place clusters in parallel subagents (brief in playbook §9), then merge the results and check them.

## Phase 2: Report

`python3 -I $SKILL/scripts/render_report.py familytree.json research/dossier.json report.html`

It shows the ancestry mix, people by generation, each place then and now with graded and cited claims, a merged family and world timeline, open questions, and the bibliography. Fix every "claims without a source" warning. Show the user the report and the most surprising findings, and ask whether anything is wrong or missing before writing the story.

## Phase 3: Story

Read `references/story-guide.md`. Write the scenes into `video/src/data/story.json` (schema: `data-formats.md` §4): one interleaved timeline across all branches, life events, the world in the room, hedged wording for anything below `documented`, chapter cards, a closing scene with `origins` (`tree_tool.py origins`), and a credits scene. Show the user the outline (year, title, one line per scene) before synthesis.

## Phase 4: Video

Read `references/video-pipeline.md`. In short:
```bash
zsh $SKILL/scripts/new_project.sh <work>/video
zsh $SKILL/scripts/setup_tts.sh                          # once per machine
# fill video/src/data/*.json, fetch images with commons_fetch.py
npm run geo && npm run check
npm run vo -- --engine yazgi --voice male-01             # or --engine say --voice <macOS voice>
~/.cache/family-migration-story/venv/bin/python -I $SKILL/scripts/asr_check.py . --lang tr
npx remotion still FamilyStory out/check/a.jpg --frame=<n> --scale=0.5   # look before rendering
npm run render
zsh $SKILL/scripts/deliver.sh out/master.mp4 out/<name>
zsh $SKILL/scripts/qa_video.sh out/<name>.mp4
```

Look at stills from the busiest scenes (photo card plus facts, the origins bar, the credits) before the full render. Afterwards, send the 720p file (phone-sized), mention the 1080p one, and say what was not verified, such as how natural the voice sounds, which is the user's call.

## Example

`assets/example/` is a small fictional family (two lineages, Selanik → İzmir and Of → İstanbul; the people are invented, the history and sources are real) with a finished familytree.json, dossier.json, images.tsv and video data. Use it as the pattern for the JSON files, or run it to check a machine's setup (about 2 minutes of video, a few minutes end to end):
```bash
zsh $SKILL/scripts/new_project.sh /tmp/fms-demo/video && cd /tmp/fms-demo/video
cp $SKILL/assets/example/video-data/*.json src/data/
python3 -I $SKILL/scripts/research/commons_fetch.py $SKILL/assets/example/images.tsv public/img src/data/credits.json
npm run geo && npm run vo -- --engine yazgi && npm run check && npm run render
```

## Lessons from real runs

- Users want the branches **interleaved in time**, with "meanwhile…" cross-cuts and life events (marriages, births), not one lineage after another.
- A static screen feels dead. Every scene should move: camera drift, a route drawing, a photo slowly zooming. The template does this; keep scenes from being all text.
- Text must not jitter. Labels live in an HTML layer moved with sub-pixel transforms; don't move them into the SVG.
- Concrete details (a ship's history, a village's household count, a museum) are what people remember. Find them in the research and hedge them honestly.
- Register places reveal settlement history: a person born abroad and registered in a Turkish village points to that village's arrival history.
- The most natural local Turkish voice found was yazgi-tts male-01. Chatterbox-multilingual was much slower and needed ~6 GB of disk, so check disk space before installing large TTS models.
- Some archives (Library of Congress, Gallica) refuse scripted access from some networks. Use their links in a browser instead of working around the block.
- Photo cards hid a family place in both test runs. `npm run check` now flags it; fix the `cam` before rendering instead of finding it in stills.
- Don't assume the route of a forced migration: Drama's exchangees mostly left by train through Eastern Thrace, not by ship from Kavala. Draw the documented route, mark it representative, and say in the narration that the family's own route is unknown.
- e-Devlet PDFs differ in layout (header split, notes block at the end, the browser's print header and footer when the page was saved with "Print"); after importing, compare the person count and a few rows with the PDF.
