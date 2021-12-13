import requests
from requests.api import request

# This is the http address for the local machine we are running on
BASE_URI = "http://127.0.0.1:5000/"

# URI extensions for the different resources
TEAM_RESOURCE_URI = "team/"
PLAYER_RESOURCE_URI = "player/"
STAFF_RESOURCE_URI = "staff/"

# team data to be added to database
team_data = [
    {"name": "Broncos", "owner": "The Bowlen Family", "year_formed": 1960},
    {"name": "Cheifs", "owner": "Clark Hunt", "year_formed": 1960},
    {"name": "Chargers", "owner": "Dean Spanos", "year_formed": 1960},
    {"name": "Raiders", "owner": "Mark Davis", "year_formed": 1960}
]

# player data to be added to database
player_data = [
    {"name": "Austin Ahlers", "team": "Broncos", "age": 21, "height": 73, "weight": 205, "position": "DE"},
    {"name": "Carson Ahlers", "team": "Broncos", "age": 13, "height": 73, "weight": 205, "position": "WR"},
    {"name": "Cooper Ahlers", "team": "Cheifs", "age": 11, "height": 73, "weight": 205, "position": "QB"},
    {"name": "Matthew Ahlers", "team": "Chargers", "age": 49, "height": 73, "weight": 205, "position": "DT"},
    {"name": "John Doe", "team": "Free Agent", "age": 34, "height": 73, "weight": 205, "position": "RB"}
]

staff_data = [
    {"name": "Vic Fangio", "team": "Broncos", "position": "Head Coach", "years_on_team": 4},
    {"name": "Andy Reid", "team": "Cheifs", "position": "Head Coach", "years_on_team": 6},
    {"name": "Jon Gruden's Replacement", "team": "Raiders", "position": "Head Coach", "years_on_team": 1},
    {"name": "Jack Del Rio", "team": "Chargers", "position": "Head Coach", "years_on_team": 3},
    {"name": "John Smith", "team": "Broncos", "position": "Athletic Director", "years_on_team": 40},
    {"name": "Mark Zuckerberg", "team": "Broncos", "position": "Personal Trainer", "years_on_team": 32},
    {"name": "Bill Gates", "team": "Chargers", "position": "General Manager", "years_on_team": 16},
    {"name": "Mark Cuban", "team": "Raiders", "position": "General Manager", "years_on_team": 7}
]

# The following code tests all of the currently implemented functionality for the team and player tables
#   Add in the team data (PUT Requests)
#   Add in the player data (PUT Requests)
#   Patch Austin Ahlers (PATCH Player request)
#   Patch the Broncos (PATCH Team request)
#   Deleting a current player
#   Deleting a fake player
#   Deleting a current team
#   Deleting a fake team
#   Getting a nonexistant team
#   Getting an existing team
#   Getting an existant player
#   Getting a nonexistant player

for i in range(len(team_data)):
    response = requests.put(BASE_URI + TEAM_RESOURCE_URI + str(i), team_data[i])
    print(response.json())

for i in range(len(player_data)):
    response = requests.put(BASE_URI + PLAYER_RESOURCE_URI + str(i), player_data[i])
    print(response.json())

for i in range(len(staff_data)):
    response = requests.put(BASE_URI + STAFF_RESOURCE_URI + str(i), staff_data[i])
    print(response.json())

austin_patch = {
    "name": "Austin J Ahlers",
    "team": "Chargers",
    "age": 20,
    "weight": 207,
    "height": 14,
    "position": "QB"
}

response = requests.patch(BASE_URI + PLAYER_RESOURCE_URI + "0", austin_patch)
print(response.json())

broncos_patch_data = {
    "name": "Denver Broncos",
    "owner": "The Ahlers Family"
    }

response = requests.patch(BASE_URI + TEAM_RESOURCE_URI + "0", broncos_patch_data)
print(response.json())

response = requests.delete(BASE_URI + PLAYER_RESOURCE_URI + "4")
print(response)

response = requests.delete(BASE_URI + PLAYER_RESOURCE_URI + "40")
print(response)

response = requests.delete(BASE_URI + TEAM_RESOURCE_URI + "0")
print(response)

response = requests.delete(BASE_URI + TEAM_RESOURCE_URI + "10")
print(response)

response = requests.get(BASE_URI + TEAM_RESOURCE_URI + "0")
print(response.json())

response = requests.get(BASE_URI + TEAM_RESOURCE_URI + "1")
print(response.json())

response = requests.get(BASE_URI + PLAYER_RESOURCE_URI + "1")
print(response.json())

response = requests.get(BASE_URI + PLAYER_RESOURCE_URI + "20")
print(response.json())

# The following are the complete set of operation on the staff records
#   Getting an existant staff member
#   Getting an nonexistant staff member
#   Patching an existant staff member
#   Patching an nonexistant staff member
#   Deleting an existant staff member
#   Deleting an nonexistant staff member
response = requests.get(BASE_URI + STAFF_RESOURCE_URI + "2")
print(response.json())

response = requests.get(BASE_URI + STAFF_RESOURCE_URI + "51")
print(response.json())

mark_cuban_patch = {
    "name": "Mark H Cuban",
    "team": "Chargers",
    "position": "Head of NFT's",
    "years_on_team": 39
}

response = requests.patch(BASE_URI + STAFF_RESOURCE_URI + "7", mark_cuban_patch)
print(response.json())

response = requests.patch(BASE_URI + STAFF_RESOURCE_URI+ "20", mark_cuban_patch)
print(response.json())

response = requests.delete(BASE_URI + STAFF_RESOURCE_URI + "6")
print(response)

response = requests.delete(BASE_URI + STAFF_RESOURCE_URI + "40")
print(response)