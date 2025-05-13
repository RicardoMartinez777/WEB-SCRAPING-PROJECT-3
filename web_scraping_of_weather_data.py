# -*- coding: utf-8 -*-

# Import libraries
!pip install requests beautifulsoup4

!pip install requests

import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

# 1) Identify the webpage from which to extract the data.

# Weather page URL (change based on your location)
url = "https://weather.com/es-CO/tiempo/horario/l/34a7392f41bcf5cb4fc9994d7f0585a8443ec761294fca844b2803f8098b007f"

# 2) Use Requests and BeautifulSoup to fetch and parse the HTML.

# Make the request
response = requests.get(url)

if response.status_code == 200:
    print("Request successfully!")
    html = response.text
else:
    print(f"Wrong with the request: {response.status_code}")

#Parsear the  HTML
soup = BeautifulSoup(html, "html.parser")

# 3) Extract relevant information such as temperature, humidity, and weather

# Find html tags with soup.find
details_table = soup.find('ul', {'data-testid': 'DetailsTable'})

# Find html tags with soup.find
city_h = soup.find_all('div', class_ = 'LocationPageTitle--LocationPageTitle--UGFbm HourlyForecast--CardHeader--XKdku')

# Find html tags with soup.find
hour_h = soup.find("div", class_="HourlyForecast--timestamp--l3YIP")

# Find html tags with soup.find
day_h = soup.find("h2", id="currentDateId0")

city = city_h[0].span.text[1:]
hour= hour_h.text.strip()
day= day_h.text.strip()
weather_data = []  # List to store data

weather_data.insert(0, ("City", city))
weather_data.insert(1, ("Time", hour[16:21]))
weather_data.insert(2, ("Day", day))

if details_table:
    list_items = details_table.find_all('li', class_='DetailsTable--listItem---Ageh')

    for item in list_items:
        title_tag = item.find('span', {'class': 'DetailsTable--label--RGc1c'})
        value_tag = item.find('span', {'class': 'DetailsTable--value--pWEVz'})

        if title_tag and value_tag:
            title = title_tag.get_text(strip=True)
            value = value_tag.get_text(strip=True)
            weather_data.append((title, value))
else:
    print("Weather details table not found.")

for label, value in weather_data:
    print(f"{label}: {value}")

# Convert to DataFrame
weather = dict(weather_data)
df = pd.DataFrame(weather, index=[0])

# 4) Store the extracted data in an SQLite database.

# Connect or create the SQLite database
conn = sqlite3.connect('weather.db')

# Create a table (if it doesn't exist)
df.to_sql('weather_data', conn, if_exists='append', index=False)

# Close the connection
conn.close()

# Connect to the 'weather.db' database
conn = sqlite3.connect('weather.db')
# Create a cursor to execute SQL commands.
cursor = conn.cursor()

# SQL query that selects all records from the table named weather
cursor.execute('SELECT * FROM weather_data')
# This command retrieves all the results of the executed query.
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()