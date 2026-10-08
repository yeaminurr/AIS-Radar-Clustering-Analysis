from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string if needed

# Define the database and collection
db = client['viz_project']
collection = db['ais']

# Load the JSON file
with open('26_2023_01_tracks_ais_simplified_2_wid.json', 'r') as file:
    data = json.load(file)  # This will load the JSON file into a Python list or dictionary

# Insert the JSON data into the collection
if isinstance(data, list):  # If the JSON file contains an array of documents
    collection.insert_many(data)
else:  # If the JSON file contains a single document
    collection.insert_one(data)

print("AIS Data imported successfully!")

collection = db['radar']

# Load the JSON file
with open('26_2023_01_tracks_radar_simplified_with_husdroff.json', 'r') as file:
    data = json.load(file)  # This will load the JSON file into a Python list or dictionary

# Insert the JSON data into the collection
if isinstance(data, list):  # If the JSON file contains an array of documents
    collection.insert_many(data)
else:  # If the JSON file contains a single document
    collection.insert_one(data)

print("Radar Data imported successfully!")