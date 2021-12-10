import requests
from requests.api import request

# This is the http address for the local machine we are running on
BASE_URI = "http://127.0.0.1:5000/"

RESOURCE_URI = "player/"

# player data to be added to database
data = [
    {"name": "Austin Ahlers", "team": "Broncos", "age": 21, "position": "DE"},
    {"name": "Carson Ahlers", "team": "Broncos", "age": 13, "position": "WR"},
    {"name": "Cooper Ahlers", "team": "Cheifs", "age": 11, "position": "QB"},
    {"name": "Matthew Ahlers", "team": "Cowboys", "age": 49, "position": "DT"},
    {"name": "John Doe", "team": "Washington Football Team", "age": 34, "position": "RB"},
]


# PUT requests to add players to database
# and print statements for seeing the responses from our API
for i in range(len(data)):
    response = requests.put(BASE_URI + RESOURCE_URI + str(i), data[i])
    print(response.json())


response = requests.get(BASE_URI + RESOURCE_URI + "20")
print(response.json())

"""
# Here we get the response from the API when we send a get request using the whole URL
#response = requests.get(BASE_URI + RESOURCE_URI)
response = requests.put(BASE_URI + RESOURCE_URI)
print("Player Created")
print(response.json())

response = requests.delete(BASE_URI + RESOURCE_URI)
print("Player Deleted")
print(response)
"""