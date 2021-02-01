# Import libraries we are going to use

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Import our url

url_population = "https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoodpop.htm"

response = requests.get(url_population)
soup = BeautifulSoup(response.text, 'html.parser')
population = soup('table', {"class": 'light_table right'})

# Cleaning the data obtained from the url
data = population[0].find_all('tr')

population2 = []
for row in data:
    population2.append([cell.text for cell in row.find_all()])

population_final = pd.DataFrame(population2)
population_final.columns = population_final.iloc[0]
population_final = population_final.iloc[1:]

# Now, we work to include in the empty cells the values we are looking for.
    
    # We replace empty cells by "nan"
population_final = population_final.replace(r'^\s*$', np.nan, regex=True)

    # Secondly, we define a function to substitute the name of some values for the correct ones.
def neighbourhood (Borough):
    if Borough == "Kings (Brooklyn)":
        return "Brooklyn" 
    elif Borough == "New York (Manhattan)":
        return "Manhattan" 
    elif Borough == "Bronx":
        return "Bronx"
    elif Borough == "Queens":
        return "Queens" 
    elif Borough == "Richmond (Staten Island)":
        return "Staten Island"

population_final ["Borough"] = population_final["Borough"].apply(neighbourhood)

    # Finaly, we define new dataframes for each value we want to include in the table and we apply a concatante.

bronx = population_final.loc[0:10].replace(np.nan,"Bronx")
brooklyn = population_final.loc[11:29].replace(np.nan,"Brooklyn")
manhattan = population_final.loc[30:39].replace(np.nan,"Manhattan")
queens = population_final.loc[40:53].replace(np.nan,"Queens")
staten_island = population_final.loc[54:56].replace(np.nan,"Staten Island")

NYC_population = pd.concat([bronx, brooklyn, manhattan, queens, staten_island])

# Final result
print (NYC_population)
