"""
projekt_3 (ENGETO): Election scraper
author: Veronika Čížková

email: veronika.cizkova21@gmail.com
discord: veronikacizkova
"""

import csv
import sys
import requests
from bs4 import BeautifulSoup

def ziskej_html(url):
    """Načte HTML obsah z dané URL adresy."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Chyba. Nelze načíst {url}.")
        return None

def zkontroluj_url_prefix(url):
    """Zkontroluje, zda URL začíná konkrétním prefixem."""
    pozadovany_prefix = "https://volby.cz/pls/ps2017nss/ps"
    if not url.startswith(pozadovany_prefix):
        print("Chyba. Zkontrolujte 1. argument (odkaz na stránky).")
        quit()

def zkontroluj_csv_priponu(soubor):
    """Zkontroluje, zda má soubor příponu .csv."""
    if not soubor.endswith('.csv'):
        print("Chyba. Výstupní soubor musí mít příponu .csv.")
        quit()

def ziskej_id_obci(html):
    """Extrahuje ID obcí z HTML obsahu."""
    id_obci = [td.text for td in html.find_all("td", class_="cislo")]
    return id_obci

def ziskej_nazvy_obci(html):
    """Extrahuje názvy obcí z HTML obsahu."""
    nazvy_obci = [td.text for td in html.find_all("td", class_="overflow_name")]
    return nazvy_obci

def ziskej_odkazy_na_obce(html):
    """Extrahuje URL odkazy pro jednotlivé obce."""
    odkazy_na_obce = [f"https://volby.cz/pls/ps2017nss/{td.a['href']}" for td in html.find_all("td", class_="cislo")]
    return odkazy_na_obce

def ziskej_strany(html_obce):
    """Vytvoří seznam politických stran kandidujících v konkrétní obci."""
    strany = [td.text for td in html_obce.find_all("td", class_="overflow_name")]
    return strany

def ziskej_pocet_registrovanych_volicu(odkazy_na_obce):
    """Získá počet registrovaných voličů v každé obci"""
    pocet_registrovanych_volicu = []
    for odkaz in odkazy_na_obce:
        html_obce = ziskej_html(odkaz)
        registrovani = html_obce.find("td", headers="sa2").text.replace('\xa0', ' ')
        pocet_registrovanych_volicu.append(registrovani)
    return pocet_registrovanych_volicu

def ziskej_pocet_zucastnenych_volicu(odkazy_na_obce):
    """Zjistí pro každou obec počet voličů, kteří se zúčastnili voleb."""
    pocet_zucastnenych_volicu = []
    for odkaz in odkazy_na_obce:
        html_obce = ziskej_html(odkaz)
        zucastneni = html_obce.find("td", headers="sa3").text.replace('\xa0', ' ')
        pocet_zucastnenych_volicu.append(zucastneni)
    return pocet_zucastnenych_volicu

def ziskej_pocet_platnych_hlasu(odkazy_na_obce):
    """Zjistí počet platných hlasů v každé obci."""
    pocet_platnych_hlasu = []
    for odkaz in odkazy_na_obce:
        html_obce = ziskej_html(odkaz)
        platne_hlasy = html_obce.find("td", headers="sa6").text.replace('\xa0', ' ')
        pocet_platnych_hlasu.append(platne_hlasy)
    return pocet_platnych_hlasu

def ziskej_hlasy_stran(odkazy_na_obce):
    """Zjistí počet hlasů, které strany získaly v jednotlivých obcích."""
    hlasy_stran = []
    for odkaz in odkazy_na_obce:
        html_obce = ziskej_html(odkaz)
        hlasy = [td.text for td in html_obce.find_all("td", class_="cislo", headers=["t1sb3", "t2sb3"])]
        hlasy_stran.append(hlasy)
    return hlasy_stran

def vytvor_dataset(html_obce):
    """Vytvoří dataset obsahující informace o obcích a počtech hlasů pro jednotlivé strany."""
    id_obci = ziskej_id_obci(html_obce)
    nazvy_obci = ziskej_nazvy_obci(html_obce)
    odkazy_na_obce = ziskej_odkazy_na_obce(html_obce)

    registrovani_volici = ziskej_pocet_registrovanych_volicu(odkazy_na_obce)
    zucastneni_volici = ziskej_pocet_zucastnenych_volicu(odkazy_na_obce)
    platne_hlasy = ziskej_pocet_platnych_hlasu(odkazy_na_obce)
    hlasy_stran = ziskej_hlasy_stran(odkazy_na_obce)

    sloucena_data = []
    zakladni_info = zip(id_obci, nazvy_obci, registrovani_volici, zucastneni_volici, platne_hlasy)
    for info, hlasy in zip(zakladni_info, hlasy_stran):
        sloucena_data.append(list(info) + hlasy)

    return sloucena_data

def hlavni_funkce(url, vystupni_soubor):
    """Funkce zpracovává data a ukládá je do CSV souboru."""

    zkontroluj_url_prefix(url)
    zkontroluj_csv_priponu(vystupni_soubor)

    print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}.")
    html_obce = ziskej_html(url)

    if html_obce:
        sloupce = ['Číslo obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
        strany = ziskej_strany(ziskej_html(ziskej_odkazy_na_obce(html_obce)[0]))

        sloupce.extend(strany)
        radky = vytvor_dataset(html_obce)

        print(f"UKLÁDÁM DO SOUBORU: {vystupni_soubor}.")
        with open(vystupni_soubor, "w", encoding="UTF-8", newline="") as soubor:
            writer = csv.writer(soubor)
            writer.writerow(sloupce)
            writer.writerows(radky)
        print("UKONČUJI PROGRAM.")

    else:
        print("Chyba. Zkontrolujte zadané argumenty.")

if __name__ == "__main__" and len(sys.argv) == 3:
    hlavni_funkce(sys.argv[1], sys.argv[2])
else:
    print("Chyba. Špatný počet argumentů")
    quit()