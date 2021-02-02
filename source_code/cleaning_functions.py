import numpy as numpy
import pandas as pd
import requests

# Import our dataset

airbnb_NYC = pd.read_csv("../data/AB_NYC_2019.csv", encoding = "ISO-8859-1")

# Print our dataset to compare cleaning results

print (airbnb_NYC)

# Cleaning functions that have been used

airbnb_NYC = airbnb_NYC.drop(['name','latitude','longitude','host_name','calculated_host_listings_count','last_review'], axis = 1)

# Neighborhood grouping by name.

airbnb_NYC.neighbourhood_group.unique()

airbnb_NYC.loc[airbnb_NYC["neighbourhood_group"] == "Brooklyn", "neighbourhood_group"] = "Brooklyn"
airbnb_NYC.loc[airbnb_NYC["neighbourhood_group"] == "Manhattan", "neighbourhood_group"] = "Manhattan"
airbnb_NYC.loc[airbnb_NYC["neighbourhood_group"] == "Bronx", "neighbourhood_group"] = "Bronx"
airbnb_NYC.loc[airbnb_NYC["neighbourhood_group"] == "Queens", "neighbourhood_group"] = "Queens"
airbnb_NYC.loc[airbnb_NYC["neighbourhood_group"] == "Staten Island", "neighbourhood_group"] = "Staten Island"
airbnb_NYC["neighbourhood_group"].value_counts()

# Definition of a variable to replace the name of some cells values.

def neighbourhood (neighbourhood_group):
    if neighbourhood_group == "Brooklyn":
        return "Brooklyn" 
    elif neighbourhood_group == "Manhattan":
        return "Manhattan" 
    elif neighbourhood_group == "Bronx":
        return "Bronx"
    elif neighbourhood_group == "Queens":
        return "Queens" 
    elif neighbourhood_group == "Staten Island":
        return "Staten Island" 
    else:
        return "other" 

# Application of defined conditions in our dataframe.

airbnb_NYC ["neighbourhood_group"] = airbnb_NYC["neighbourhood_group"].apply(neighbourhood)


# Reset our indiex.

airbnb_NYC_2019 = airbnb_NYC.reset_index(drop=True)

# Final result

print (airbnb_NYC_2019)
