import random
import pandas as pd
from tabulate import tabulate as tb


f = open("players.txt", "r", encoding='utf-8')  # włączenie polskiego kodowania


players = []  # lista wszystkich zawodników

for player in f:
    # ETL - split(" ", 1)[1] - dzielimy na 2 substringi po pierwszej spacji i bierzemy 2 część
    players.append(player.split(" ", 1)[1].split("\n")[0])

f.close()

team1 = []
team2 = []

for n in players:
    # losujemy zawodnika
    rand_player = players[random.randint(0, len(players) - 1)]
    # sprawdzamy, czy nie jest już przydzielony
    if (rand_player not in team1 ):
        team1.append(rand_player)
    # wychodzimy z pętli, gdy wypełnimy całą drużynę, >= zamiast == (gdy nieparzysta liczba)
    if (len(team1) >= len(players)/2):
        break

# uzupełnienie drugiej drużyny resztą zawodników
for n in range(len(players)):
    if players[n] not in team1:
        team2.append(players[n])

# uzupełnienie drugiej przy nieparzystej liczbie graczy
if len(team2) < len(team1):
    team2.append("pusty")

# print(team1)
# print(team2)

full_data = {
    "TEAM 1": team1,
    "TEAM 2": team2
}

df = pd.DataFrame(full_data)

# formatujemy df, przy pomocy tabulate, zamieniamy do na stringa
formated_df = tb(df, headers="keys", showindex=False, tablefmt="outline")

print(formated_df)

# zapis do pliku
of = open("teams.txt", "w")
of.write(formated_df)
of.close()


