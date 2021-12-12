import requests
from requests.api import request

# This is the http address for the local machine we are running on
BASE_URI = "http://127.0.0.1:5000/"

# URI extensions for the different resources
TEAM_RESOURCE_URI = "team/"
PLAYER_RESOURCE_URI = "player/"

# team data to be added to database
team_data = [
    {"name": "Broncos", "owner": "The Bowlen Family", "year_formed": 1960},
    {"name": "Cheifs", "owner": "Clark Hunt", "year_formed": 1960},
    {"name": "Chargers", "owner": "Dean Spanos", "year_formed": 1960},
    {"name": "Raiders", "owner": "Mark Davis", "year_formed": 1960}
]

# player data to be added to database
player_data = [
    {"name": "Austin Ahlers", "team": "Broncos", "age": 21, "position": "DE"},
    {"name": "Carson Ahlers", "team": "Broncos", "age": 13, "position": "WR"},
    {"name": "Cooper Ahlers", "team": "Cheifs", "age": 11, "position": "QB"},
    {"name": "Matthew Ahlers", "team": "Chargers", "age": 49, "position": "DT"},
    {"name": "John Doe", "team": "Free Agent", "age": 34, "position": "RB"},
]

# PUT requests to add teams to database
# and print statements for seeing the responses from our API
for i in range(len(team_data)):
    response = requests.put(BASE_URI + TEAM_RESOURCE_URI + str(i), team_data[i])
    print(response.json())

# PUT requests to add players to database
# and print statements for seeing the responses from our API
for i in range(len(player_data)):
    response = requests.put(BASE_URI + PLAYER_RESOURCE_URI + str(i), player_data[i])
    print(response.json())

broncos_patch_data = {
    "name": "Denver Sports Team",
    "owner": "The Ahlers Family"
    }

response = requests.patch(BASE_URI + TEAM_RESOURCE_URI + "0", broncos_patch_data)
print(response.json())

"""
responee = requests.delete(BASE_URI + PLAYER_RESOURCE_URI + "4")
print(response)

responee = requests.delete(BASE_URI + PLAYER_RESOURCE_URI + "2")
print(response)
"""

responee = requests.delete(BASE_URI + TEAM_RESOURCE_URI + "0")
print(response)

"""
response = requests.get(BASE_URI + TEAM_RESOURCE_URI + "0")
print(response.json())

"""

"""
response = requests.delete(BASE_URI + PLAYER_RESOURCE_URI + "2")
print(response)

response = requests.get(BASE_URI + PLAYER_RESOURCE_URI + "20")
print(response.json())

cooper_patch = {
    "name": "Cooper Matthew Ahlers",
    "position": "TE", 
    "team": "Broncos"
}

response = requests.patch(BASE_URI + PLAYER_RESOURCE_URI + "2", cooper_patch)
print(response.json())

# Here we get the response from the API when we send a get request using the whole URL
#response = requests.get(BASE_URI + RESOURCE_URI)
response = requests.put(BASE_URI + RESOURCE_URI)
print("Player Created")
print(response.json())

response = requests.delete(BASE_URI + RESOURCE_URI)
print("Player Deleted")
print(response)
"""