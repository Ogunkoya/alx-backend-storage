def update_topics(mongo_collection, name, topics):
    result = mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
    return result.modified_count