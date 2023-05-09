from pymongo import MongoClient

# Connect to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# Select the logs database and the nginx collection
db = client.logs
collection = db.nginx

# Get the total number of documents in the collection
total_logs = collection.count_documents({})

# Get the number of documents with each method
get_logs = collection.count_documents({'method': 'GET'})
post_logs = collection.count_documents({'method': 'POST'})
put_logs = collection.count_documents({'method': 'PUT'})
patch_logs = collection.count_documents({'method': 'PATCH'})
delete_logs = collection.count_documents({'method': 'DELETE'})

# Get the number of documents with method=GET and path=/status
status_logs = collection.count_documents({'method': 'GET', 'path': '/status'})

# Print the stats
print(f"{total_logs} logs")
print(f"\t{get_logs}\tGET")
print(f"\t{post_logs}\tPOST")
print(f"\t{put_logs}\tPUT")
print(f"\t{patch_logs}\tPATCH")
print(f"\t{delete_logs}\tDELETE")
print(f"\t{status_logs}\tGET /status")