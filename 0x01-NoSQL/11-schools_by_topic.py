def schools_by_topic(mongo_collection, topic):
    schools = mongo_collection.find({'topics': {'$in': [topic]}})
    return [school['name'] for school in schools]