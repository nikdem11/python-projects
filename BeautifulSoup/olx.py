import requests
import csv
from bs4 import BeautifulSoup

produkt = "podwodne-miasta-gra"

for strona in range(1, 5):

    URL = ("https://www.olx.pl/oferty/q-" + str(produkt) + "/?page=" + str(strona) + "/")
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "lxml")

    wszystkie_oferty = soup.find("div", class_="listing-grid-container css-d4ctjd")

    pojedyncze_oferty = wszystkie_oferty.find_all("div", class_="css-1sw7q4x")

    file = open("%s.csv" % produkt, "w", encoding="utf-8", newline="")
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["Oferta", "Cena", "Uzytkowanie", "Miejsce", "Data", "Link do oferty"])

    for x in pojedyncze_oferty:
        tytul_oferty = x.find("h6", class_="css-16v5mdi er34gjf0")
        cena = x.find("p", class_="css-10b0gli er34gjf0")
        uzytkowanie = x.find("span", class_="css-3lkihg")
        miejsce_data = x.find("p", class_="css-veheph er34gjf0")
        link = x.find("a")

        if tytul_oferty:
            tytul_oferty_text = tytul_oferty.text.strip()
        else:
            tytul_oferty_text = "Title not found"

        if cena:
            cena_str = cena.text.strip().replace(" ", "")
            if cena_str[:-2].isdigit():  # 25zł
                cena_int = int(cena_str[:-2])
                cena_text = cena_int
            elif cena_str[:-5].isdigit():  # 25,99zł
                cena_int = int(cena_str[:-5])
                cena_text = cena_int
            elif cena_str == "Zadarmo":
                cena_text = 0
            elif cena_str == "Zamienię":
                cena_text = 111111
            elif cena_str[:-9].isdigit():  # 23zł/zadobę
                cena_int = int(cena_str[:-9])
                cena_text = cena_int
            elif cena_str[:-12].isdigit():  # 23,99zł/zadobę
                cena_int = int(cena_str[:-12])
                cena_text = cena_int
            elif cena_str[:-14].isdigit():  # 23złdonegocjacji
                cena_int = int(cena_str[:-14])
                cena_text = cena_int
            elif cena_str[:-17].isdigit():  # 23,99złdonegocjacji
                cena_int = int(cena_str[:-17])
                cena_text = cena_int
            else:
                cena_text = 999999
        else:
            cena_text = 999999

        if uzytkowanie:
            uzytkowanie_text = uzytkowanie.text.strip()
        else:
            uzytkowanie_text = "Usage not found"

        if miejsce_data:
            miejsce_data_str = miejsce_data.text.strip()
            x = miejsce_data_str.split("-")
            miejsce_text = x[0]
            data_text = x[1]
        else:
            miejsce_text = "Place not found"
            data_text = "Date not found"

        if link:
            link_text = "https://www.olx.pl" + link.get("href")
        else:
            link_text = "Link not found"

        writer.writerow([tytul_oferty_text, cena_text, uzytkowanie_text, miejsce_text, data_text, link_text])

    file.close()
