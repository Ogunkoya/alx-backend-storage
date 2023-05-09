from pymongo import MongoClient

# Connect to the MongoDB instance
client = MongoClient()
db = client['logs']
collection = db['nginx']

# Get the number of documents in the collection
num_logs = collection.count_documents({})

# Print the number of logs
print(f"{num_logs} logs")

# Print the number of documents with each HTTP method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    num_docs = collection.count_documents({"method": method})
    print(f"{method}: {num_docs}")

# Print the number of documents with method=GET and path=/status
num_docs = collection.count_documents({"method": "GET", "path": "/status"})
print(f"GET /status: {num_docs}")

# Get the top 10 most present IPs
pipeline = [
    {"$group": {"_id": "$remote_addr", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
top_ips = list(collection.aggregate(pipeline))

# Print the top 10 most present IPs
print("Top 10 IPs:")
for i, ip in enumerate(top_ips, 1):
    print(f"{i}. {ip['_id']}: {ip['count']}")