---
name: pachet-comentator-fotbal
description: Creează pachete de comentator (briefing-uri pre-meci) pentru meciuri de fotbal, în format PDF descărcabil, stil Sky Sports/Opta Facts (bare de secțiune compacte, bullet points, tabele). Folosește acest skill de fiecare dată când utilizatorul cere un "pachet de comentator", un "briefing pentru meci", informații complete despre un meci de fotbal (stadion, arbitri, antrenori, cap la cap, transferuri, loturi) menite să fie folosite ca material de comentariu, chiar dacă nu spune explicit "PDF" sau "Opta Facts". Se declanșează și pentru cereri de genul "vreau tot ce trebuie să știu despre meciul X vs Y" sau "fă-mi un research pentru meciul de azi/mâine".
---

# Pachet comentator de fotbal

Acest skill produce un PDF de tip briefing pentru comentatori sportivi, pentru un meci de fotbal specificat de utilizator. Combină cercetare web extensivă cu un format vizual compact, inspirat de fișele „Opta Facts" ale Sky Sports.

## Pasul 0 — Loturile complete și detaliile complete per jucător sunt implicite, întotdeauna

**Implicit, inclusiv fără să fie cerut explicit: lotul complet, pentru ambele echipe, cu nivelul maxim de detaliu per jucător (înălțime, carieră, statistici, plus orice fapt interesant găsit — vezi mai jos), la fiecare pachet.** Nu întreba utilizatorul dacă vrea "doar titularii" sau "tot lotul", și nici cât de detaliat să fie fiecare jucător — presupune nivelul maxim în ambele privințe. Excepție: dacă utilizatorul cere explicit un scop redus (ex. "doar titularii", "doar nume și vârstă, fără carieră"), respectă asta.

Pentru meciuri europene (UEFA), sursa cea mai autoritară e **lista oficială UEFA înregistrată pentru acea dublă confruntare** (`uefa.com/{competiție}/match/{id}--{echipa-a}-vs-{echipa-b}/lineups/`, secțiunea „Squad lists" / „Official squad list") — nu lotul general de club. Lotul general de club (footmercato, site oficial) deseori include jucători care NU sunt înregistrați pentru competiția europeană (ex: jucători transferați recent la alt club, sau pur și simplu neînscriși pe lista UEFA acel sezon) — aceștia nu trebuie incluși ca disponibili pentru meciul respectiv.

### Verificare sistematică, obligatorie — nu doar reactivă

După ce ai compilat lotul, **verifică-l post cu post, jucător cu jucător**, contra sursei oficiale (UEFA squad list pentru cupe europene; site-ul oficial de club sau `superliga.ro`/`footmercato.net/club/{club}/effectif/` pentru campionate interne). Nu te limita să adaugi doar jucătorii pe care utilizatorul îi semnalează explicit ca lipsă — dacă un utilizator a găsit o lipsă (ex. un portar, un fundaș titular), tratează asta ca semnal că verificarea inițială a fost incompletă și **re-verifică integral toate posturile**, nu doar cel semnalat. Numără explicit: dacă sursa oficială arată 3 portari și tu ai listat doar 1, asta e un eșec de verificare, nu un detaliu minor.

### Detaliile per jucător (înălțime, carieră, statistici) — pentru tot lotul, nu doar ce cere explicit utilizatorul

Acest nivel de detaliu per jucător cere volum mare de cercetare — pentru un lot de 20+ jucători per echipă, poate ajunge la 40-90+ căutări/fetch-uri suplimentare doar pentru înălțime+carieră. Nu e un motiv să reduci scopul sau să întrebi utilizatorul dacă vrea mai puțin — e volumul de lucru normal, așteptat, pentru acest skill. Ca să lucrezi eficient:
- Transfermarkt (cea mai bună sursă pentru înălțime) blochează fetch direct — se poate doar căuta și citi din fragmentele de căutare.
- Pentru jucătorii tineri de academie, înălțimea și cariera detaliată adesea nu există public — marchează „n/d", nu inventa.
- Wikipedia (pagina individuală, dacă există) e adesea cea mai eficientă sursă unică: infobox cu înălțime + carieră de cluburi + carieră la națională, dintr-un singur fetch — verifică-l primul înainte de a face mai multe căutări separate.

Marchează onest „n/d" (indisponibil public) acolo unde chiar nu găsești date, în loc să inventezi cifre.

### Fapte interesante per jucător — legătură cu adversarul, poveste personală sau de carieră

Pe măsură ce cercetezi cariera fiecărui jucător pentru rândul de lot, fii atent la orice detaliu care ar da culoare comentariului — nu ca o căutare separată, dedicată, per jucător (asta ar dubla volumul deja mare de research), ci ca atenție suplimentară la ce apare deja în sursele de carieră/statistici pe care oricum le consulți. Caută în special:
- **Legătură cu adversarul din acest meci**: a jucat anterior pentru echipa adversă, s-a format în academia ei, a marcat împotriva ei recent, sau joacă acum pentru prima dată împotriva fostului club.
- **Poveste personală**: relații de familie cu alt jucător/antrenor din meci (frați, tată-fiu), revenire pe orașul natal, revenire după o accidentare gravă/absență lungă, o bornă de carieră (ex. al 100-lea meci, prima convocare la națională).
- **Fapt de carieră notabil**: golgheter al ligii, cel mai tânăr/cel mai în vârstă din lot, record de club, parcurs neobișnuit (ex. venit dintr-o ligă inferioară).

Adaugă un asemenea fapt DOAR dacă chiar există și e confirmat de o sursă — nu forța o „poveste" pentru fiecare jucător. Majoritatea jucătorilor dintr-un lot complet (mai ales rezervele și tinerii) n-au nimic public relevant de acest gen, și e normal ca rândul lor să rămână doar cu carieră+statistici, fără linia suplimentară.

## Pasul 1 — Cercetare (folosește web_search / web_fetch)

Adună, în această ordine, cât mai multe din următoarele (nu toate sunt mereu disponibile — nu inventa ce nu găsești):

1. **Meci de bază**: dată, oră, competiție, etapă.
2. **Stadion**: nume oficial + nume de sponsorizare, capacitate, orice sancțiune specială (porți închise, tribune închise etc. — verifică știri disciplinare recente ale ligii).
3. **Arbitri**: principal, asistenți, al 4-lea oficial, VAR/AVAR; istoricul arbitrului principal cu fiecare echipă (câte meciuri, ce bilanț) dacă se găsește.
4. **Antrenori**: cariera COMPLETĂ de antrenor pentru fiecare, ca listă cronologică — fiecare club unde a fost antrenor principal, perioada, și realizări notabile dacă există — nu doar un rezumat de o propoziție cu „cluburile anterioare". Include și motivul plecării/schimbării dacă e cunoscut și relevant (demis, retrogradare, expirare de contract, avansare la alt club). Cea mai bună sursă pentru cariera completă e de obicei pagina Wikipedia a antrenorului (secțiunea/infobox-ul „Managerial career", cu ani și cluburi) sau profilul de manager de pe Transfermarkt (doar via search, fetch direct blochează) — ambele au de regulă un istoric cronologic complet dintr-un singur loc. Verifică mereu identitatea curentă a antrenorului — se schimbă des în fotbal. **Nu descrie mandatul curent ca „a doua aventură"/„revenire" la club decât dacă o sursă confirmă explicit un mandat anterior la același club** — vezi regula despre afirmații de tip „premieră"/„revenire" din secțiunea de acuratețe, e o greșeală ușor de făcut din grabă și greu de observat la o citire rapidă.
5. **Cap la cap**: ultimele 2-3 întâlniri directe (dată, scor, competiție) + orice statistică istorică agregată găsită (cu sursă, pentru că diferite agregatoare dau cifre diferite pe eșantioane diferite — menționează asta dacă apar discrepanțe). SoccerStats.com are o pagină H2H dedicată, structurată — vezi secțiunea dedicată mai jos.
6. **Performanțele din sezonul trecut**: clasament final, puncte, parcurs în cupe, golgheter, schimbări de antrenor în timpul sezonului. Pentru forma curentă (nu doar sezonul trecut) — ultimele rezultate, PPG, „Last 8", statistici acasă/deplasare, over/under goluri — SoccerStats.com e cea mai rapidă sursă structurată; vezi secțiunea dedicată mai jos.
7. **Absenți**: accidentări, suspendări, incertitudini — caută știri de team news chiar din preziua/ziua meciului.
8. **Echipa probabilă/confirmată**: caută compos probabile din surse specializate (maxifoot, VAVEL, Sports Mole etc.) sau, dacă meciul s-a jucat deja între timp, caută rezultatul și alinierea reală (surse ca footmercato au adesea „Équipe type" calculată din meciul jucat).
9. **Mercato/transferuri de vară**: sosiri și plecări pentru ambele echipe, cu sume, folosind footmercato.net/tableau sau echivalent — de obicei cea mai bogată sursă structurată.
10. **Pregătirea de vară**: toate amicalele jucate, cu scoruri, pentru ambele echipe.
11. **Loturi complete**: vezi secțiunea dedicată mai jos.
12. **Top știri recente**: caută cele mai proaspete știri despre fiecare club. **Regulă strictă: nicio știre mai veche de 2-3 zile față de data curentă** (verifică data explicită a articolului — dacă nu găsești o dată clară de 2-3 zile, caută mai insistent sau renunță la acea știre, nu o folosi doar pentru că e interesantă). Site-urile oficiale ale cluburilor au de obicei o listă cronologică de știri pe prima pagină (`{club}.com`, `fcX.ch` etc.), dar deseori conțin doar comunicate logistice (bilete, deplasări) — pentru veritabile știri de ultimă oră (transferuri, antrenamente, conferințe de presă, accidentări), caută pe agregatoare specifice de țară (ex: pentru Olanda: `headliner.nl`, `voetbalprimeur.nl`, `fcupdate.nl`; pentru Franța: `footmercato.net/actualite`; pentru România: `superliga.ro`) care afișează explicit ora/data fiecărei știri, ceea ce permite filtrarea corectă după vechime. footmercato.net afișează și el o listă de "actualité" recentă per club. Prioritizează știri cu relevanță directă pentru meci (accidentări de ultimă oră, transferuri de jucători din lot, motivație/context de la antrenor, conferințe de presă pre-meci) — nu doar zgomot general de mercato fără legătură cu echipa.
13. **Cote pariuri**: dacă utilizatorul le cere, agregă din 2-3 case de pariuri/agregatoare.
14. **Subiecte de discuție / fapte interesante**: sintetizează cele mai bune povești găsite pe parcurs (jucători care se întorc împotriva fostului club, antrenori care-și schimbă locul, recorduri, coincidențe) — acestea fac diferența într-un pachet bun.

### Surse preferate (în ordine)
Site-uri oficiale ale ligii/clubului → footmercato.net (efectiv live + tablou de transferuri + fișe de jucători) → FBref (verificare lot efectiv folosit în meciuri de campionat — vezi secțiunea „Loturi complete" de mai jos; fetch direct blochează des, ca la Transfermarkt) → Transfermarkt (doar via search, nu fetch direct — blochează) → Soccerway → The Analyst → agregatoare de cote (Sportytrader etc.) → presă specializată (L'Équipe, Sky Sports etc., doar parafrazat, niciodată citat extins — vezi regulile de copyright).

Pentru **clasament, formă curentă, cap la cap și statistici de goluri** (nu pentru loturi/transferuri — nu acoperă asta), adaugă **SoccerStats.com** la research indiferent de ligă — e fetch-abil direct, spre deosebire de Transfermarkt/FBref, deci nu costă căutări suplimentare. Vezi secțiunea dedicată mai jos pentru URL-uri și pentru ce aduce în plus un cont de membru.

**Excepție — Liga 1 / SuperLiga România**: pentru meciuri din campionatul românesc, `superliga.ro` (site-ul oficial, administrat de LPF) e de departe cea mai bună sursă și trebuie folosită prioritar, înaintea oricăreia din lista de mai sus. Un singur fetch pe pagina de club (`superliga.ro/cluburi/{nume-club}`) dă: stadion (nume, capacitate, adresă, coordonate), antrenor, lot complet pe posturi cu numere și meciuri jucate, statistici detaliate de echipă (ofensiv/defensiv/disciplină), ultimul rezultat și următorul meci. Paginile individuale de jucător (link din lotul de club) dau în plus **înălțime, greutate**, dată naștere, picior preferat, și un set foarte bogat de statistici stil Opta (atingeri/meci, tackling-uri, dueluri câștigate/totale, acuratețe pase, poziție în clasamentul intern al echipei pentru fiecare stat). Pagina generală `superliga.ro/jucatori` (căutare) e randată prin JavaScript și nu se poate citi prin fetch — mergi direct pe pagina clubului sau a jucătorului.
- Notă: liga se numește oficial „SuperLiga" (rebrand al fostei „Liga 1"), dar presa și fanii încă zic des „Liga 1" — folosește ambele denumiri interschimbabil, dar verifică denumirea curentă exactă în meta-titlul paginii.
- OneFootball nu s-a dovedit util pentru date de lot/jucător (fragmentele de căutare arată doar agregare de știri) — nu-l prioritiza.
- AiScore poate fi o sursă rapidă de rezervă: uneori afișează înălțime + greutate + valoare de piață pentru tot lotul direct în fragmentul de căutare, fără să fie nevoie de fetch.

### Loturi complete — sfaturi practice
- **Pentru meciuri europene (UEFA)**: mergi direct pe lista oficială UEFA a meciului (`uefa.com/.../match/{id}--.../lineups/`) — dă lotul complet înregistrat pentru ambele echipe, pe posturi, cu meciuri jucate și goluri în competiția respectivă. Jucătorii marcați cu „*" sunt de obicei „List B" (tineri sub 21 de ani, fără restricții de înregistrare). Aceasta e sursa de bază pentru orice pachet de cupă europeană — nu lotul general de club.
- Pentru campionate interne, caută pagina „efectiv" a clubului pe footmercato.net (`footmercato.net/club/{nume-club}/effectif/`) — de obicei conține numărul de tricou, vârsta, naționalitatea și un mini-tabel de statistici curente pentru tot lotul într-un singur fetch. E cea mai bună sursă pentru **lotul curent corect** (numere, vârste, statistici recente), dar NU are înălțime.
- **Pentru meciuri de campionat intern (nu cupe europene), folosește FBref ca a doua verificare, în plus față de footmercato/site oficial**: pagina „Standard Stats — All Competitions" a clubului pentru sezonul curent (`fbref.com/en/squads/{id}/{sezon}/all_comps/{Club}-Stats-All-Competitions`, ex. `fbref.com/en/squads/19c3f8c4/2025-2026/all_comps/Ajax-Stats-All-Competitions`) listează *fiecare* jucător care a prins măcar un minut într-un meci oficial în acest sezon (toate competițiile), cu post, vârstă, naționalitate, meciuri jucate (MP), titularizări, minute și statistici de bază (goluri, pase decisive, cartonașe, xG). E util în special pentru a scoate din lot jucători care încă apar pe pagina de club dar n-au mai jucat deloc (accidentați pe termen lung, marginalizați total) sau pentru a confirma că un tânăr de academie a debutat efectiv — exact genul de discrepanță care duce la un lot greșit dacă te bazezi doar pe o listă „pe hârtie". FBref blochează des fetch direct (403), la fel ca Transfermarkt — caută-l și citește din fragmentele de căutare; dacă un fetch direct reușește, cu atât mai bine, dar nu te baza pe asta. Nu e o sursă primară pentru lotul complet „pe hârtie" (nu arată rezervele care încă n-au debutat) — combină-l cu footmercato/site oficial, nu-l folosi izolat.
- Pentru lotul „oficial" de club, site-ul propriu al clubului (ex. `fclorient.bzh/lequipe-professionnelle-.../`) e adesea cel mai de încredere pentru numere și nume exacte.
- **Pentru înălțime, per jucător**, în ordinea șansei de succes:
  1. **Wikipedia** (pagina individuală a jucătorului, dacă există) — cel mai bun caz: infobox complet cu înălțime + toată cariera de cluburi + carieră la națională, într-un singur loc. Caută `{nume jucător} wikipedia footballer` sau `{nume jucător} (footballer)`.
  2. **Sofascore** (`sofascore.com/football/player/{nume}/{id}`) — afișează înălțimea clar în profilul individual ("X is Y years old, Z cm tall"), găsibil de obicei direct din fragmentul de căutare fără fetch. Pagina de echipă (`sofascore.com/football/team/{club}/{id}`) NU are înălțimi în tabel și poate fi cache-uită/veche — nu te baza pe ea pentru lotul curent.
  3. **footmercato.net/joueur/{nume}/** — uneori are înălțime, dar des lipsește la jucători tineri.
  4. Transfermarkt — cea mai completă bază de date, dar blochează fetch direct; poate apărea în fragmente de căutare.
  - Pentru jucători foarte tineri de academie, e normal să nu găsești înălțimea nicăieri public — marchează „n/d", nu inventa.
- Nu presupune că un jucător menționat într-un articol vechi mai e la club — verifică-l în lista curentă de efectiv (footmercato sau site-ul oficial), pentru că transferurile se schimbă rapid vara, iar pagini precum Sofascore pot afișa scheme de lot vechi/cache-uite.

### SoccerStats.com — clasament, formă, cap la cap, statistici de goluri

Bun de folosit la fiecare pachet, indiferent de ligă, pentru orice altceva decât loturi/transferuri (nu e o sursă de squad):
- Pagina de ligă (`soccerstats.com/latest.asp?league={liga}`, ex. `league=england`) dă clasamentul complet cu formă, PPG, „Last 8", tabele separate acasă/deplasare (goluri marcate/primite) și o secțiune „Over/Under" cu procentul de meciuri peste 1.5/2.5 goluri — util direct pentru bara „Performanțele din sezonul trecut"/formă curentă și pentru „Opta Facts".
- Pagina de echipă (`soccerstats.com/teamstats.asp?league={liga}&stats=u{id}-{nume-echipă}`) detaliază aceleași statistici doar pentru un club.
- Pagina H2H (`soccerstats.com/h2h.asp?league={liga}&t1id={id1}&t2id={id2}`; dacă nu știi ID-urile echipelor, pornește de la `soccerstats.com/h2h_selection.asp?league={liga}`) dă istoricul direct dintre cele două echipe — o alternativă structurată la cap la cap-ul adunat manual din presă.
- Spre deosebire de Transfermarkt/FBref, soccerstats.com **nu blochează fetch direct** — se poate citi normal cu un fetch, fără să te bazezi pe fragmente de căutare.
- **Dacă utilizatorul are cont de membru** (Standard/Fan/Supporter, prin Steady) și, în sesiunea curentă, computerul lui e conectat și e logat în soccerstats.com în propriul browser: poți naviga paginile ca utilizator logat (fără reclame) și, de la nivelul Fan în sus, declanșa un export CSV al datelor de pe pagină, în loc să parsezi tabelul din HTML. Fișierul exportat ajunge în folderul de Downloads al utilizatorului — citește-l de acolo (direct, dacă folderul e conectat, sau cerându-i utilizatorului fișierul). Nu presupune că ai acces la cont dacă nu ai confirmarea că browserul utilizatorului e conectat și logat chiar în sesiunea curentă — nu poți refolosi un login din altă sesiune.

### The Analyst (theanalyst.com) — unghiuri de poveste stil Opta, predicții

Site-ul oficial de analiză al Opta/Stats Perform — sursa cea mai apropiată ca ton de stilul „Opta Facts" pe care îl imită acest pachet, și un model bun pentru cum arată o bară de „poveste" bine scrisă (vezi Pasul 2). Pentru meciuri din ligile mari (Premier League, La Liga, Serie A, Bundesliga, Ligue 1, competiții UEFA), caută `{echipa A} v {echipa B} preview theanalyst.com` sau `site:theanalyst.com {echipa}` — de multe ori au deja un preview cu predicții („Opta supercomputer": șanse de victorie/egal/înfrângere, scor probabil) și 5-10 fapte narative gata formulate, exact genul de unghi care poate fi parafrazat direct ca bară de poveste. Nu e disponibil pentru orice meci (mai ales ligi mai mici) — dacă nu găsești un preview dedicat, treci mai departe fără să insiști.

### Unghiuri de poveste statistică (stil Sky Sports „Opta Facts") — pentru barele dedicate de poveste

Pe lângă bara „STORY OF THE MATCH" (cele mai bune 6-10 fapte generale despre meci, echivalentul fostei bare unice „OPTA FACTS"), un pachet complet include acum și câteva bare de **poveste dedicată**, per echipă (vezi Pasul 2) — fiecare cu titlu propriu, punchy, stil tabloid sportiv (ex. „SET-PIECES A CONCERN FOR CARRICK", „HOME TURNAROUND UNDER CARRICK", „SUPER SUB JACK"), nu doar bullet-uri seci sub un titlu generic. Fiecare bară de poveste tratează **un singur unghi** (un jucător, un trend tactic, o bornă, o secvență de rezultate), cu 2-5 bullet-uri care îl susțin — nu o listă eterogenă de fapte fără legătură între ele.

Multe dintre cele mai bune fapte din pachetele Opta/Sky NU sunt găsite gata scrise nicăieri — sunt **calculate** din date brute pe care oricum le-ai adunat: un procent (ex. ce % din golurile primite au venit de la faze fixe), un clasament relativ (ex. „cel mai mic % de dueluri câștigate dintre echipele din etapă"), o secvență numărată meci cu meci (câte meciuri consecutive fără înfrângere, câte victorii din ultimele N). Nu te limita să cauți fapte gata formulate — dacă ai lista de rezultate sau statistici brute (din SoccerStats, footmercato, site-ul oficial), fă tu calculul (procent, medie, rang) și **verifică-l de două ori** înainte să-l pui în pachet ca „fapt". Un calcul greșit e la fel de grav ca un fapt inventat.

Unghiuri utile de căutat activ (nu doar de așteptat să apară din research-ul general de la Pasul 1): forma ultimelor N meciuri (PPG, victorii/egaluri/înfrângeri, „Last 8" de pe SoccerStats), statistici de fază fixă (goluri marcate/primite din corner sau lovitură liberă, ca procent din total), statistici de posesie/dueluri/presare comparativ cu restul ligii (SoccerStats sau pagini de statistici de ligă), borne individuale pentru un jucător cheie (a N-a apariție, revenire după accidentare/împrumut, primul gol la noua echipă, statistici „ultimele 2 sezoane" într-un mini-tabel), tipare istorice la acest stadion sau împotriva acestui tip de adversar (nou-promovate, echipe din top 6 etc.), record-uri de club sau de ligă, parcursul antrenorului de la numire încoace (puncte/victorii comparativ cu predecesorul).

## Pasul 2 — Format PDF (stil Sky Sports „Opta Facts")

Structura standard, în această ordine (ajustează după ce e disponibil):

1. **Titlu + subtitlu**: „ECHIPA A vs ECHIPA B" + competiție/etapă/dată/stadion/oră.
2. **Bara „STORY OF THE MATCH"**: 6-10 bullet points cu cele mai bune fapte/statistici/povești generale despre meci — cea mai importantă secțiune, pusă prima.
3. **Bare de poveste dedicată, per echipă** (2-5 per echipă): vezi „Formatul barei de poveste dedicată" mai jos. Aici intră analizele mai lungi — un jucător cheie, un trend tactic, o bornă, o revenire — cu titlu propriu punchy, nu generic. Un grafic simplu (bar sau scatter, vezi Pasul 3) merge bine aici dacă ai date comparative reale (nu decorativ). Pune toate barele echipei A, apoi toate barele echipei B (sau alternează dacă poveștile sunt clar perechi, ca „form under noul antrenor" pentru ambele).
4. **Bara „STADION"**: 1-3 bullet-uri.
5. **Bara „ANTRENORI"**: câte un bloc per antrenor — vârstă/naționalitate pe scurt, apoi cariera COMPLETĂ de antrenor ca listă cronologică (un bullet per club, cu perioadă și realizare notabilă dacă există), nu un rezumat de o propoziție. Format:
   ```
   {Nume antrenor} ({vârstă} ani, {naționalitate})
   Cariera de antrenor:
   - {club} ({an-an}): {realizare/rezultat notabil, dacă există}
   - {club} ({an-an}): {...}
   - {club curent} (din {an}): {motiv numire, dacă e recent}
   ```
6. **Bara „CAP LA CAP"**: tabel cu ultimele întâlniri.
7. **Bara „PERFORMANȚELE DIN SEZONUL TRECUT"**: tabel comparativ pe 2 coloane.
8. **Bara „ABSENȚI ȘI ECHIPE PROBABILE"**: tabele de absenți per echipă + tabel cu aliniere probabilă/confirmată.
9. **Bara „ARBITRU"**: bullet-uri.
10. **Bara „MERCATO — VARA [an]"**: tabel comparativ IN/OUT per echipă.
11. **Bara „PREGĂTIREA DE VARĂ"**: tabele cu amicale per echipă.
12. **Bare „LEGĂTURI DIRECTE" (Link Lines), per echipă**: vezi „Formatul barei de legături directe" mai jos.
13. **Bara „LOTURI COMPLETE"**: vezi format special mai jos.
14. **Bara „TOP ȘTIRI"**: pagină dedicată, cu câte 3-5 bullet-uri per echipă (fiecare bullet: o propoziție-două, cu dată quando relevant), despre cele mai proaspete evenimente de club — separat pe secțiuni per echipă cu subtitlu (`bigsect`), la fel ca la loturi. Se pune de obicei chiar înainte de secțiunea de loturi.
15. **Notă de surse** la final (font mic, gri): ce surse au fost folosite, data compilării, disclaimer că datele se pot schimba.

### Formatul barei de poveste dedicată

Fiecare poveste e o sub-secțiune cu titlu propriu (nu „STORY 1" — un titlu punchy, specific unghiului, gen presă sportivă: „SET-PIECES A CONCERN FOR CARRICK", „SUPER SUB JACK"), urmat de 2-5 bullet-uri și, opțional, un tabel „ultimele 2 sezoane" sau un grafic simplu (vezi Pasul 3):

```
{TITLU PUNCHY, MAJUSCULE}
•  {bullet 1 — faptul central al poveștii}
•  {bullet 2 — statistică sau context care-l susține}
•  {bullet 3, opțional}
[tabel sau grafic opțional]
```

Nu forța o poveste dacă research-ul n-a scos la iveală nimic cu adevărat notabil pentru un unghi — 2-3 povești solide per echipă bat 5 povești diluate. Dacă un fapt e interesant dar nu justifică o bară proprie, poate rămâne un bullet în „STORY OF THE MATCH".

### Formatul barei de legături directe (Link Lines)

Diferit de linia „Fapt interesant" din rândul de lot (Pasul 0), care e opțională și acoperă orice tip de poveste per jucător — bara de „Legături directe" e dedicată strict jucătorilor/antrenorului cu **istoric direct verificabil față de adversarul din acest meci** (goluri marcate împotriva lui, meciuri jucate/câștigate/pierdute, cartonaș roșu primit, gol decisiv). Cercetează-o țintit pentru titulari probabili și antrenor (nu tot lotul) — caută `{jucător} vs {echipa adversă}` sau istoricul de meciuri directe pe Transfermarkt/pagina de club. Format:

```
{NUME JUCĂTOR SAU ANTRENOR, MAJUSCULE}
•  {rezumatul istoricului direct — meciuri, goluri, rezultat, dată}
```

Include doar dacă istoricul e confirmat de o sursă — nu completa cu „nicio legătură găsită" pentru fiecare jucător din lot, secțiunea listează doar cazurile relevante găsite.

### Formatul rândului de jucător (pentru loturi)

Fiecare jucător e un bloc de text comprimat, gândit să poată fi copiat direct ca element în Miro sau alt tool vizual. Acesta e formatul implicit, pentru fiecare jucător din lot (vezi Pasul 0 — nivelul maxim de detaliu e implicit, nu doar la cerere explicită):

```
{număr}. {nume} - {vârstă} ani - {NAȚ} - {înălțime}
Carieră: {cluburi anterioare → club curent, pe scurt}
Sezonul trecut (20XX/YY): {statistică sau rol relevant}
Fapt interesant: {legătură cu adversarul / poveste personală / fapt de carieră notabil}
```

Linia „Fapt interesant" apare doar dacă ai găsit efectiv ceva concret și confirmat (vezi secțiunea dedicată din Pasul 0) — nu o completa cu ceva generic doar ca să existe o linie; pentru majoritatea jucătorilor (mai ales rezerve și tineri) rândul se oprește firesc la statistica sezonului trecut.

Excepție: dacă utilizatorul cere explicit un format redus (ex. „doar nume și vârstă", „fără carieră"), folosește formatul scurt:
```
{număr}. {nume} - {vârstă} ani - {NAȚ}
{1-2 fapte comprimate relevante}
```

Grupează jucătorii pe post (Portari / Fundași / Mijlocași / Atacanți), fiecare grup într-un tabel cu rânduri alternând culoarea de fundal.

## Pasul 3 — Implementare tehnică (PDF)

Folosește Python + reportlab (Platypus), **nu** artefacte HTML — output-ul e un fișier PDF descărcabil.

- **Diacritice**: obligatoriu înregistrează fontul DejaVu Sans (`/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` și `-Bold.ttf`) și înlocuiește toate stilurile Helvetica din `getSampleStyleSheet()` cu DejaVuSans — altfel ș/ț/ă/â/î nu se afișează corect. Vezi `references/pdf_boilerplate.py` pentru codul complet, testat.
- Culoare de accent: alege o culoare specifică per echipă/club (roșu Forest, bleumarin OM, grena Nice etc.) pentru barele de secțiune și headerele de tabel — dă identitate vizuală pachetului.
- Bara de secțiune (`band_bar`): un tabel cu un singur rând, fundal deschis, text bold, pe toată lățimea paginii — vezi funcția din boilerplate.
- Tabelele de conținut: header cu fundal colorat + text alb, rânduri alternând alb/gri deschis.
- **Grafice simple** (opțional, pentru barele de poveste dedicată — vezi Pasul 2): folosește `matplotlib` (`pip install matplotlib --break-system-packages` dacă lipsește) pentru grafice bar orizontale sau scatter, ca în exemplul Sky Sports (ex. puncte-per-sezon, % dueluri câștigate comparativ cu restul ligii, puncte vs goluri de la numirea unui antrenor). Funcțiile `bar_chart()` și `scatter_chart()` din `references/pdf_boilerplate.py` generează un PNG (fundal alb, font compact, fără chenar sus/dreapta, echipa/jucătorul discutat evidențiat cu culoarea de accent, restul în gri) și îl întorc direct ca obiect `Image` de reportlab, gata de adăugat în `story`. Nu încerca touch map-uri sau shot map-uri stil Opta — cer date de poziție brute (coordonate x/y per atingere/șut) pe care research-ul web nu le oferă de obicei; rămâi la bar/scatter cu cifre agregate găsite sau calculate (vezi „Unghiuri de poveste statistică" din Pasul 1). Nu pune un grafic doar ca decor — doar unde compararea vizuală chiar ajută mai mult decât un bullet sau un tabel mic, și nu mai mult de 3-5 grafice per pachet, ca să nu aglomereze documentul.
- Salvează fișierul cu un nume descriptiv (`pachet_comentator_EchipaA_EchipaB.pdf`), copiază-l în `/mnt/user-data/outputs/` și cheamă `present_files`.

## Pasul 4 — Limbă și ton

Implicit română (dacă utilizatorul a scris în română), dar adaptează la limba conversației. Ton de comentator sportiv profesionist: concis, orientat spre fapte, fără umplutură. Bullet-urile din „STORY OF THE MATCH" și din barele de poveste dedicată trebuie să fie propoziții complete, informative, nu doar cifre seci.

## Reguli de acuratețe (importante)

- **Nu inventa date.** Dacă o informație nu se găsește (înălțime, statistică precisă), marchează explicit „n/d" sau „indisponibil public" — nu completa cu o presupunere.
- **Afirmațiile de tip „premieră", „revenire" sau „record" cer o sursă care spune exact asta, nu o inferență.** Genul „a doua aventură ca antrenor la club X", „revine după Y ani", „primul jucător din istoria clubului care...", „X nu a mai câștigat aici din 20XX" sunt exact ce face un pachet de comentator memorabil — dar sunt și cele mai ușor de inventat din greșeală, pentru că, spre deosebire de un fapt curent (cine e antrenorul acum), ele cer certitudine despre *tot* istoricul relevant. O presupunere plauzibilă (confuzie cu alt antrenor/jucător, extrapolare dintr-un fapt parțial adevărat) se poate strecura foarte natural ca „fapt", pentru că sună exact ca genul de detaliu găsit prin cercetare. Dacă nicio sursă nu afirmă explicit acel unghi istoric, prezintă faptul simplu, fără înflorirea narativă (ex. „Míchel preia Ajax din vara aceasta, venind de la Girona" — nu „a doua sa aventură la Ajax" dacă n-ai o sursă care confirmă clar un mandat anterior acolo).
- **Verifică din nou** dacă utilizatorul semnalează o eroare sau o lipsă — de multe ori are dreptate (jucători transferați recent, antrenori schimbați, jucători omiși dintr-un lot). Fă o căutare țintită și corectează, nu te apăra reflex.
- **Copyright**: parafrazează întotdeauna faptele culese din presă; niciun citat de peste 15 cuvinte; niciun citat per sursă mai mult de unul.
- **Actualitate**: fotbalul se schimbă rapid — un antrenor sau jucător menționat într-o sursă mai veche poate să nu mai fie valabil. Prioritizează sursele cele mai recente găsite (verifică datele articolelor).
