# 10 highest ppg of current season
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

#database connection
conn = sqlite3.connect('my_database.db')
cur = conn.cursor()
cur.execute('USE my_database')

#url I'm scraping
url = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats::pts_per_g"

# url = "https://www.basketball-reference.com/playoffs/"
# collect html data
html = urlopen(url)
#create beautiful soup object from HTML
soup = BeautifulSoup(html, 'html.parser')

# collect info from table header 
headers = [th.getText() for th in soup.findAll('tr') 
[0].findAll('th')]
headers = headers[1:]

#get rows from table
rows = soup.findAll('tr')[2:]
rows_data = [[td.getText() for td in rows[i].findAll('td')] 
for i in range(len(rows))]
rows_data = rows_data[0:38]
cur.execute('INSERT INTO my_table (headers)', rows_data)
conn.commit()
print(conn)
cur.close()
conn.close()

#dataframe
player_stats = pd.DataFrame(rows_data, columns=headers)

#export to CSV
player_stats.to_csv("players_stats.csv", index=False, sep=";")