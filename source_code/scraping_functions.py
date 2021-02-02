# Import libraries we are going to use

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Import our url

url_population = "https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoodpop.htm"

### By applying libraries beautfulSoup and requests, we look for the wanted information.

response = requests.get(url_population)
soup = BeautifulSoup(response.text, 'html.parser')

population = soup('table', {"class": 'light_table right'})

# Cleaning the data obtained from the url, filtering by the corresponding tags ('tr','th')
data = population[0].find_all('tr')

# Definition of an empty list to obtain all the info contained in each row of data.
population2 = []
for row in data:
    population2.append([cell.text for cell in row.find_all()])

# Creation of new dataframe based on information in 'population2', bringing results on position [0] for each column and from position [1:] for others.
population_final = pd.DataFrame(population2)
population_final.columns = population_final.iloc[0]
population_final = population_final.iloc[1:]

# Now, we work to include in the empty cells the values we are looking for.
    
# We replace empty cells by "nan" using replace in the dataframe defined.
population_final = population_final.replace(r'^\s*$', np.nan, regex=True)

# Secondly, we define a string variable to substitute the name of some values for the correct ones in column 'Borough'.
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

# Application of the variable above in our dataframe.
population_final ["Borough"] = population_final["Borough"].apply(neighbourhood)

# Definition of new variable for each value we want to replace in the table.

bronx = population_final.loc[0:10].replace(np.nan,"Bronx")
brooklyn = population_final.loc[11:29].replace(np.nan,"Brooklyn")
manhattan = population_final.loc[30:39].replace(np.nan,"Manhattan")
queens = population_final.loc[40:53].replace(np.nan,"Queens")
staten_island = population_final.loc[54:56].replace(np.nan,"Staten Island")

# Concatenation of variable defined above in our Dataframe.
NYC_population = pd.concat([bronx, brooklyn, manhattan, queens, staten_island])

# Conversion of values in columns Females, Males and Total Population from string to float.

# Conversion of column Males by defining new variables
males_values = NYC_population['Males'].values
for i in range(len(males_values)):
    myVal = males_values[i].replace(",", "")
    males_values[i] = float(myVal)

# In the origiina dataframe, we replace the original values for the obtained.
NYC_population = NYC_population.replace(myVal) 

# Conversion of column Females by defining new variables
females_values = NYC_population['Females'].values
for i in range(len(females_values)):
    myValf = females_values[i].replace(",", "")
    females_values[i] = float(myValf)

# In the original Dataframe, we replace the original values for the obtained.
NYC_population = NYC_population.replace(myValf) 

 # Conversion of column Total Population by defining new variables
population_values = NYC_population['Total Population'].values
for p in range(len(population_values)):
    myValp = population_values[p].replace(",", "")
    population_values[p] = float(myValp)

# In the original Dataframe, We replace the original values for the obtained.
NYC_population = NYC_population.replace(myValp) 

# Renaming of a column.
NYC_population = NYC_population.rename(columns={'Total Population': 'population'})


# Final result
print (NYC_population)
