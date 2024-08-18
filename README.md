Závěrečný projekt kurzu Python Akademie (ENGETO)
-	Tento projekt extrahuje výsledky parlamentních voleb v ČR v roce 2017.
-	Použité knihovny jsou v souboru requiments.txt
-	Verze Pythonu: Python 3.12.5

Projekt obsahuje:
1.	dokumentace (README.md), 
2.	soupis všech knihoven a jejich verzí (requirements.txt),
3.	skript pro stáhnutí požadovaných dat (electionscraper),
4.	soubor s uloženým výstupem (novy_jicin.csv).

Při spuštění je nutno zadat povinné argumenty: 
1.	odkaz, který územní celek chcete zpracovat
2.	jméno výstupního souboru (csv)
Výsledkem bude soubor ve formátu csv.

Ukázka projektu:
Zadáme argumenty:
1.https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104
2.novy_jicin.csv
Tj. do příkazového řádku zadáme:
python electionscraper „https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104“ „novy_jicin.csv“

Průběh programu:
STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104.
UKLÁDÁM DO SOUBORU: novy_jicin.csv .
UKONČUJI PROGRAM.

Částečný výstup:
Číslo obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,Řád národa...
568741,Albrechtičky,559,358,355,36,0,1,23,1,12,23,3,2,1,2,1,39,0,1,22,106,0,1,47,0,1,0,0,33,0
599212,Bartošovice,1 341,735,734,39,3,0,56,2,6,104,13,2,9,0,0,38,0,0,7,281,1,2,23,0,1,3,2,140,2
568481,Bernartice nad Odrou,779,547,542,70,1,0,25,1,18,21,12,2,4,1,6,47,0,1,11,163,0,0,110,0,6,0,0,43,0
546984,Bílov,442,264,264,16,0,0,13,0,3,42,3,2,3,1,0,20,0,0,2,103,0,2,10,0,2,1,0,41,0