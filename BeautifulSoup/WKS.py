import requests
import csv
from bs4 import BeautifulSoup


URL = "https://stowarzyszeniepolskiegosportu.pl/team/wks-orzel-tychy/"  # nazwa drużyny, małe litery, '-' zamiast spacji
page = requests.get(URL)

soup = BeautifulSoup(page.content, "lxml")

nazwa_druzyny = soup.find("h1", class_="entry-title")

tabela = soup.find("table", class_=["sp-player-list", "dataTable"])
wiersze = tabela.find_all("tr", class_=["odd", "even"])

file = open("%s.csv" %nazwa_druzyny.text.strip(), "w", encoding="utf-8", newline="")
writer = csv.writer(file, delimiter=",")  # przecinek dzieli kolumny
writer.writerow(["Dane zawodnika", "Pozycja", "Gole", "Asysty"])  # header

for wiersz in wiersze:
    dane = wiersz.find("a")
    pozycja = wiersz.find("td", class_="data-position")
    gole = wiersz.find("td", class_="data-goals")
    asysty = wiersz.find("td", class_="data-assists")

    dane_text = dane.text.strip() if dane else ""
    pozycja_text = pozycja.text.strip() if pozycja else ""
    gole_text = gole.text.strip() if gole else ""
    asysty_text = asysty.text.strip() if asysty else ""
    writer.writerow([dane_text, pozycja_text, gole_text, asysty_text])

file.close()
