# Deep research playbook: birthplaces in their time

Contents: 1. Ground rules · 2. The loop for one place · 3. The ten questions · 4. Search order and tools · 5. Writing queries · 6. Judging sources · 7. Reasoning from the register · 8. The world-events spine · 9. Splitting work across subagents · 10. Done when

The goal is not a Wikipedia summary of each town. It is: *what was this place like in the years this person was born there, why did the family live there, and what pushed or pulled them away?* Every sentence that reaches the story must trace back to a source, and the confidence must survive the trip.

## 1. Ground rules

- **Search places and periods, never people.** External searches, APIs and page fetches contain place names, years, events and topics only. A family member's name never goes into a query, URL or form. Names stay in local files. The scripts in `scripts/research/` are built around this rule.
- **One claim, one source, one confidence.** Write each finding as a claim in `research/dossier.json` with its source and `documented / probable / tradition / speculative`. If you cannot cite it, it is `speculative` and the story says so.
- **Primary beats secondary beats tertiary.** An Ottoman yearbook (salname) or census table beats a journal article beats Wikipedia beats a municipal website. Wikipedia is for orientation and for its references; follow the references.
- **Read the local-language sources.** The best material about a Greek town is in Greek, about a Bosnian village in Bosnian, about a Kars village in Russian, Armenian or Turkish. Fetch it and read it; translate in your head. Quote briefly; don't reproduce long passages.
- **Keep the dead ends.** A question you could not answer goes to `open_questions` with the archive that probably holds the answer. That is useful to the family and honest in the report.

## 2. The loop for one place

Run `python3 -I scripts/tree_tool.py targets familytree.json research/targets.json` first. Each target is a place string with the years the family was there (`window`) and its role (birthplace, register place, residence). Then, for each target:

1. **Resolve it.** `python3 -I scripts/research/places.py "<place as written>" --lang <ui language> [--near lon,lat]`. Pick the candidate that fits the context (a village in the right province, not a namesake). Record the QID, coordinates, names in every language and the admin chain. If nothing matches, the place was probably renamed, merged or spelt in an older form; see §7.
2. **Fix the period.** The window from `targets.json`, widened to one generation before the earliest birth there. That is when the family arrived or was already rooted.
3. **Answer the ten questions** (§3), using the search order in §4.
4. **Write claims** into `dossier.json` as you go, not at the end: `place`, `when`, `topic`, `text`, `confidence`, `sources`, `people` (ids, local only).
5. **Collect images**: a period photo, map or engraving of the place, the ship, the event (`commons_search.py`). Note the license.
6. **Note open questions.**

Do the places in the order the family lived in them: it makes the migrations visible early.

## 3. The ten questions

For each place × period, aim to answer most of these. They are what turned a list of birthplaces into a story in practice:

1. **Name and state.** What was the place called then, in which languages, and which state, province and district was it in? (Ottoman vilayet/sancak/kaza; Habsburg Bezirk; Russian oblast/okrug.) When did that change, and how?
2. **Who lived there.** Size and make-up of the population in the period: Muslims/Christians/Jews, Turkish/Greek/Bulgarian/Armenian/Kurdish/Laz/Circassian speakers, villagers/townsmen. Use yearbooks (salname), censuses, travellers' counts.
3. **What people did.** The local economy: tobacco, fishing, silk, olives, mining, trade, a garrison, a railway. It tells you what a family member likely did.
4. **Wars and violence** within the person's lifetime: front lines, occupations, sieges, massacres, deportations.
5. **Migrations.** Did people arrive (muhacir settlement after 1878, refugees after 1912-13, exchange settlers after 1923) or leave (emigration to America, flight, deportation)? Who organised it, by land or sea, along which route?
6. **The other side of the mirror.** If the family left place A for place B under an exchange or expulsion, who left B, and who arrived in A after them? (Greek refugees from Anatolia settled in the Macedonian towns Muslims had left; Bulgarians, Armenians, Greeks left places Muslim refugees then settled.) This is often the most moving part of the story and is well documented.
7. **Disasters and disease**: fires, earthquakes, cholera, typhus, famine, Spanish flu.
8. **Laws and institutions** that touched the family: conscription, land registration, the 1934 Surname Law in Turkey, citizenship rules, exchange property rules (tasfiye, iskân), the end of the caliphate, alphabet reform, new borders.
9. **What is still there**: buildings, a mosque or church, a cemetery, a museum (exchange museums, local history museums), the old name on a map, a festival, a dish, a dialect.
10. **What the register implies.** Register place, register volume/household numbers, marriage partners' origins, dates rounded to 1 July. See §7.

## 4. Search order and tools

| step | what | how |
|---|---|---|
| 1 | Orientation | Wikipedia in the local language and English (links from `places.py`). Read with WebFetch. Harvest its references. |
| 2 | Scholarship | `scripts/research/papers.py` (OpenAlex + Crossref; covers most of DergiPark). Run several phrasings in several languages. Open the PDFs that matter (`oa_url`) and read the relevant pages; cite page numbers. Theses: YÖK Ulusal Tez Merkezi, national repositories. |
| 3 | Digitised primary sources | `scripts/research/archives.py` (Internet Archive, Europeana) plus `--links` for archives without an API: Ottoman State Archives catalogue, HathiTrust, Google Books, Library of Congress, Gallica, ANNO, Greek press. Yearbooks (salname) and census tables are often on Internet Archive or HathiTrust. |
| 4 | Statistics | Census and yearbook tables by place: see `archives-by-region.md`. Even one number ("in 1906 the kaza had 14,200 Muslims and 3,100 Greeks") anchors a scene. |
| 5 | Press | Newspapers of the day (Gallica, ANNO, Chronicling America, Greek and Turkish press archives) for the event as it was reported. |
| 6 | Images | `scripts/research/commons_search.py`, then SALT Research, Library of Congress, Europeana. Only reuse images with a clear free license; record author and license. |
| 7 | Local and oral | Municipality and association sites, exchange-heritage foundations, local histories, village blogs. Useful leads, but usually `tradition` until confirmed. |

Use WebSearch (mode `extended` for niche or non-English topics) to find what the APIs miss, then WebFetch the pages. When a site refuses automated access, use the built-in browser if the user is watching, or move on. Never try to get around a block.

When a PDF is downloaded, read it locally (`uv run --with pypdf python -I -c "…"`) and cite the page.

## 5. Writing queries

A query has a **place form**, a **period marker** and a **topic**. Rotate all three.

- **Place forms**: the modern name, the old name, the name in each language and script from `places.py` (`names`, `aliases`, `official_names`), the old admin unit (kaza or sancak), and the region (Western Thrace, Pontus, Herzegovina, Kars Oblast).
- **Period markers**: a year or decade, a war ("Balkan War", "Balkan Savaşı", "Βαλκανικοί Πόλεμοι"), a treaty (Berlin 1878, Lausanne 1923), a regime (Habsburg occupation, Russian rule 1878-1918).
- **Topic words in the local language**: migration (göç, muhacir, mübadil, iskân / πρόσφυγες, ανταλλαγή πληθυσμών / iseljavanje, muhadžiri / переселение), population (nüfus, salname / απογραφή / popis / перепись), economy (tütün / καπνός / duhan), settlement (köy, iskân, ζεύγος), records (defter, kayıt, arşiv).

Examples (place-only):
- `"Karaferye kazası salname"`, `"Veria 1924 refugees settlement"`, `"Βέροια πρόσφυγες 1923"`
- `"Bosna muhacirleri İzmir 1878"`, `"muhadžiri Sarajevo 1900 iseljavanje Turska"`
- `"Kars oblast 1897 census Muslim emigration"`, `"Карсская область переселение мусульман"`
- `"Urla mübadil iskân 1924"`, `"İzmir 1924 mübadil vapur"`

Run 5-15 queries per important place; fewer for places only passed through.

## 6. Judging sources

| grade | examples | confidence it can carry |
|---|---|---|
| A | archival document with a call number; census or yearbook table; treaty text; peer-reviewed paper or thesis citing archives | `documented` |
| B | scholarly book without archival detail; reference work; museum label; reputable newspaper of the time | `documented` if two agree, else `probable` |
| C | Wikipedia; municipal history page; foundation or association site | `probable` at best; follow its sources |
| D | blog, forum, village Facebook page, family memory | `tradition` |

Check every precise number and date against a second source when it is central to a scene. When sources disagree, keep both and say so.

## 7. Reasoning from the register

Civil registers hide a lot of history. Patterns worth checking:

- **Birthplace abroad, register place in the new country** (born Karaferye, registered in Urla) = a migrant household entered on arrival. Look up the settlement scheme for that district and year.
- **Odd place strings.** Clerks wrote what they heard: "Serin Bosna" could be Saray-Bosna (Sarajevo) or a village named Serin. Test each reading against the period and the migration patterns, then write the reasoning with `probable` or `speculative`.
- **Dates on 1 July** (Turkey: `01/07/YYYY`) mean only the year was known. Older ones are often estimates made decades later; a 90-year gap between a parent and a child is a register artefact, not a fact.
- **Grouped register numbers** (same volume and household) = one household at the moment it was registered. Turkish registers continue the late-Ottoman population registers, so a household number can point back to the first registration after arrival.
- **Surnames** appear in Turkish records after 21 June 1934; a surname on an older ancestor was added later. Surnames often name the village of origin, a trade or a nickname: a lead.
- **Village renames.** Turkey renamed thousands of villages (mostly 1940s-1980s). Greece renamed most Turkish and Slavic place names in 1926-1928. Look up old/new pairs (Nişanyan Map/Index Anatolicus for Turkey; the Greek "Pandektis" database of name changes).
- **District instead of village.** A birthplace is often written as the kaza or district, not the village: people registered in one village can have the district's name as birthplace. Villages also moved between districts (a village of district A in 1890 may be in district B today), and the register shows today's district. Check the village's administrative history before reading two place names as a migration.
- **Today's neighbourhood names.** Registers show the current name of a mahalle. Some Turkish towns renamed most of their neighbourhoods in the Republic (in Burdur about four in five, with names like Zafer, Emek, Sakarya), so a mahalle name can be younger than the people registered in it. Search for the old name ("<town> mahalle isimleri", "şehirsel toponimi") before researching the neighbourhood.

## 8. The world-events spine

The story cross-cuts family moments with what was happening in the country and the world. Build a list of 10-20 events inside the family's years in `dossier.world`, each with a date, a scope (`world`, `country`, `region`) and a source. Prefer events that touched the family's places (a war reaching the town, a treaty moving the border, a law changing names or property) over generic headlines. Check exact dates; they appear on screen.

## 9. Splitting work across subagents

For more than about six places, give each cluster of nearby places to a subagent so the research runs in parallel and the main context stays small. Brief each one with:

- the places (as written), their coordinates or QIDs if known, and the year windows (no personal names);
- the ten questions, the search order and the query advice from this file (point it to this file's path);
- the output: claims, places and sources in the dossier format from `data-formats.md`, plus open questions and image candidates (Commons titles with licenses);
- the rules: places and periods only in queries, cite pages, grade confidence, don't evade blocks.

Merge the results into one `dossier.json`, de-duplicate sources, and re-check the claims the story will lean on.

## 10. Done when

- every target place is resolved (or explained as unresolvable);
- every family place has at least three claims, and every migration has its why, when and how;
- 10-20 dated world/country events are on the spine;
- each claim the story will use has a source, and anything weaker than `documented` is phrased as such in the narration;
- there are image candidates for most scenes;
- `render_report.py` runs without "claims without a source" warnings.
