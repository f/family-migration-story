# Archives and literature by region

Contents: Everywhere · Turkey and the Ottoman Empire · Population exchange 1923 · Greece · Balkans (Bulgaria, Bosnia, Serbia, North Macedonia, Albania) · Caucasus and the Russian Empire · Middle East and North Africa · Europe and the Americas · Name-based record searches

What each archive is good for, and how to get in. Archives marked *(no API)* are read with WebFetch or the built-in browser; `scripts/research/archives.py --links` prints search links for the main ones. URLs change: if one fails, search for the institution's name.

## Everywhere

- **Wikipedia** (local languages first): orientation and references. Follow the footnotes.
- **OpenAlex / Crossref**: `papers.py`. Most journals with DOIs, including much of DergiPark, many Greek and Balkan journals.
- **Internet Archive** (`archives.py --only ia`): digitised books, yearbooks, travel accounts, consular reports, old maps. Search old spellings ("Salonica", "Smyrna", "Trebizond", "Cavalla").
- **HathiTrust** (full-text search, *no API*): 19th and early-20th c. books in full view; good for yearbooks, statistics, British and American travel writing.
- **Google Books** (*no API*): snippets confirm that a fact exists in a book and on which page.
- **Europeana** (`archives.py --only europeana`): photos, postcards, maps from European collections.
- **Wikimedia Commons** (`commons_search.py`): freely licensed photos, maps, engravings for the video.
- **Wikisource**: treaty and law texts (Berlin 1878, Lausanne 1923, Turkish laws).
- **JSTOR, Persée, Cairn**: articles; JSTOR's early-journal content is open. Persée for French scholarship on the Levant and Balkans.
- **UK National Archives, Discovery** (https://discovery.nationalarchives.gov.uk, *no API*): catalogue of Foreign Office files; British consular reports on trade and population in Ottoman ports (Salonica, Smyrna, Trebizond, Samsun) are often printed in Parliamentary Papers and digitised on Internet Archive/HathiTrust.

## Turkey and the Ottoman Empire

- **Devlet Arşivleri Başkanlığı, Ottoman archive catalogue** (https://katalog.devletarsivleri.gov.tr/, *no API*, free sign-up): document summaries in modern Turkish; search by place + topic ("Karaferye muhacir", "Urla iskân"). Summaries alone often settle a date or a number; cite the fond code and number (e.g. `DH.MKT. 1234/56`).
- **Salnames (provincial yearbooks, 1866-1918)**: population, officials, schools, mosques, villages per kaza. Search "salname-i vilayet-i Selanik", "Trabzon vilayeti salnamesi" on Internet Archive, HathiTrust, Atatürk Kitaplığı, İSAM library (https://ktp.isam.org.tr). Many have transliterated editions as books or theses.
- **Censuses**: Kemal Karpat, *Ottoman Population 1830-1914* (1985) gives the 1881/82-1893 and 1906/07 counts by kaza and religion. Turkish Republic censuses 1927, 1935, 1945 … (TÜİK library, published volumes, often on Internet Archive).
- **DergiPark** (https://dergipark.org.tr) and **YÖK Ulusal Tez Merkezi** (https://tez.yok.gov.tr/UlusalTezMerkezi/): Turkish local-history articles and theses on almost every district: migration, settlement, a village's waqf, a town's 19th-century economy.
- **Nişanyan Map / Index Anatolicus** (https://www.nisanyanmap.com): old and new names of Turkish villages, with the date of each change.
- **SALT Research** (https://archives.saltresearch.org): Ottoman and Republican photographs, postcards, maps, city plans.
- **Library of Congress, Abdul Hamid II collection** (*no API* from scripts here; browse on loc.gov): 1880s-1890s photographs of Ottoman schools, barracks, towns.
- **Atatürk Kitaplığı** (Istanbul Metropolitan Municipality library): digitised Ottoman periodicals, maps, postcards, yearbooks.
- **Republican Archives (BCA), settlement fonds** (same catalogue as above; codes `272.11`, `272.12` and the `271` iskân registers): what happened to migrants on arrival. Reports such as "in June 1924, 785 people from a kaza were settled in province X", the exchangees' application forms (talepname, naming the home village and the place of settlement), and 1930s settlement registers that list immigrants by village and household. Scholars often tabulate them for one origin district; search DergiPark for "<origin kaza> mübadil iskân" or "<province> mübadil".
- **Tahrir registers (15th-16th c.)**: Ottoman tax surveys village by village (BOA `TT.d.` series; Tapu Kadastro's Kuyûd-ı Kadîme archive). Published village and nahiye studies on DergiPark show whether a village already existed in, say, 1485, what it grew and which district it belonged to. Useful for an old Anatolian village with no migration in its story.
- **Temettuat and 1840s population registers (1844-1845)**: household-level income and head counts for towns and villages; many are transcribed in local-history books and articles ("<town> temettuat defteri", "1844 nüfus defteri").
- **Millî Mücadele'nin Yerel Tarihi 1918-1923** (TÜBA, 2023, open access with DOIs): one chapter per province on 1918-1923: occupations, local resistance, refugee movements. A quick, cited start for those years in any Anatolian province.

## Population exchange 1923 (Turkey ↔ Greece)

- **Treaty text**: Convention Concerning the Exchange of Greek and Turkish Populations, Lausanne, 30 January 1923 (Wikisource). Exemptions: Muslims of Western Thrace east of the Nestos/Mesta border and Greeks established in Istanbul before 30 October 1918.
- **Lozan Mübadilleri Vakfı** (https://www.lozanmubadilleri.org.tr): settlement lists by origin and destination, ship arrivals, oral histories. Good leads; check against the archives.
- **Exchange museums**: e.g. the Mübadele museums in Çatalca and Alaçam; their panels and catalogues cite local numbers.
- **Standard works**: Kemal Arı, *Büyük Mübadele*; Bruce Clark, *Twice a Stranger*; Renée Hirschon (ed.), *Crossing the Aegean*; Onur Yıldırım, *Diplomacy and Displacement*; Stephen Ladas, *The Exchange of Minorities* (1932, on Internet Archive). The Turkish government published settlement statistics by province (iskân).
- **Ships**: mübadil transport ships (Gülcemal, Ak Deniz and others) are named in newspapers and memoirs. A specific family's ship is usually oral tradition; check the ship's existence and route, then hedge.
- **Western Macedonia's Greek-speaking Muslims** (Vallahades; in Turkey "Patriyot"; the kazas of Grebene/Grevena, Nasliç/Neapoli and Kozana): a group with its own literature. Refik Engin (2014) works from the talepnames of 1,857 exchangees from the Grebene area, listing their home villages and the provinces they were sent to; Zeynep Özcan (2024, *Balkan Sosyal Bilimler Dergisi*) reads Grebene as a Patriyot place. Testimonies give the route: on foot to Karaferye (Veria), by train to Selanik, about two weeks at the port, then a ship to İzmir (Ercan Haytoğlu 2006, on Honaz). Özcan notes that they called themselves "Selanik göçmeni" after the port they left from, so "from Selanik" in a family story can mean an inland kaza.

## Greece

- **General State Archives, ΓΑΚ** (https://gak.gr): regional branches hold refugee settlement and land files.
- **ELSTAT digital library** (https://dlib.statistics.gr): 1920, 1928 censuses by settlement, including refugee counts in 1928.
- **Pandektis, National Hellenic Research Foundation** (http://pandektis.ekt.gr): database of Greek settlement name changes (old Turkish/Slavic names → new Greek names, with dates).
- **National Library press archive** (https://efimeris.nlg.gr): Greek newspapers.
- **ELIA, Hellenic Literary and Historical Archive** (https://www.elia.org.gr): photographs, maps, ephemera.
- **Centre for Asia Minor Studies (Κέντρο Μικρασιατικών Σπουδών)**: oral testimony of Greek refugees from Anatolia, by place of origin. This is the other side of the exchange.
- **Village-level statistics of Ottoman Macedonia before 1912**: Vasil Kançov, *Македония. Етнография и статистика* (1900); the Greek consular counts of 1904; D. Halkiopoulos (1910). Each counts villages by religion and language and each has an agenda: compare at least two and report the range, not one number. Wikipedia village pages in Greek and Bulgarian usually quote all three.

## Balkans

- **Bulgaria**: State Archives Agency (https://archives.government.bg); 1880s-1930s Bulgarian censuses; Muslim emigration after 1878 (Karpat; McCarthy, *Death and Exile*).
- **Bosnia and Herzegovina**: Archive of BiH; Gazi Husrev-beg Library (https://www.ghb.ba); Austro-Hungarian censuses of 1879, 1885, 1895, 1910 (published volumes, on Internet Archive/Google Books, e.g. *Die Ergebnisse der Volkszählung in Bosnien und der Hercegovina vom 10. Oktober 1910*); emigration to the Ottoman Empire after 1878 and 1908 (Safet Bandžović's studies). **ANNO** (https://anno.onb.ac.at): Austrian newspapers, which reported on Bosnia daily.
- **Serbia**: Digital National Library of Serbia (https://digitalna.nb.rs); 1878 and 1912 expulsions of Muslims from Niš, Vranje, Kosovo regions.
- **North Macedonia, Albania, Kosovo**: Ottoman yearbooks of Selanik, Manastır, Kosova, İşkodra vilayets; Balkan War 1912-13 reports (Carnegie Endowment *Report of the International Commission to Inquire into the Causes and Conduct of the Balkan Wars*, 1914, on Internet Archive).

## Caucasus and the Russian Empire

- **Kars, Ardahan, Batum** (Russian rule 1878-1918): 1897 Russian census by uyezd (Demoscope Weekly tables, https://www.demoscope.ru); the *Kavkazskiy kalendar'* yearbooks (Russian National Library, Internet Archive); Muslim emigration to Ottoman lands after 1878 (Candan Badem, *Çarlık Yönetiminde Kars, Ardahan, Artvin*); the 1855 siege of Kars.
- **Russian State Library** (https://search.rsl.ru): digitised Russian books and statistics.
- **Crimea, North Caucasus**: Crimean Tatar and Circassian migrations 1850s-1900s (muhacir settlement across Anatolia and the Balkans).
- **Armenia, Georgia**: national archives; for Armenian history of a shared town, the Houshamadyan project (village memory books) is a strong secondary source.

## Middle East and North Africa

- Ottoman yearbooks of Beirut, Syria, Aleppo, Baghdad, Mosul, Basra, Hejaz, Tripoli, Benghazi; French mandate archives (Centre des Archives diplomatiques de Nantes); British mandate records (UK National Archives); Library of Congress Matson collection (Palestine photographs).

## Europe and the Americas (emigrant branches)

- **Germany**: Bundesarchiv; local city archives (Stadtarchiv) for guest-worker arrivals after 1961; DOMiD (migration documentation centre, Cologne).
- **USA**: NARA (https://www.archives.gov); Chronicling America (US newspapers); Ellis Island arrival records.
- **UK, France, Netherlands, Sweden**: national archives and newspaper archives (Gallica for France; Delpher for the Netherlands).

## Name-based record searches

Passenger lists, Arolsen Archives, FamilySearch, Ancestry, cemetery databases and the Ottoman archive's name indexes are searched by personal name. They can find a specific ancestor, but they send family names to an outside service. Do these only when the user asks for it and agrees to the names being sent, one search at a time. Without that, stay with place and period research.
