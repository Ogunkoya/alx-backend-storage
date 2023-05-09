def top_students(mongo_collection):
    # Use the MongoDB aggregation pipeline to group by student and calculate average score
    pipeline = [
        {'$unwind': '$scores'},
        {'$group': {'_id': '$student_id', 'averageScore': {'$avg': '$scores.score'}}},
        {'$lookup': {'from': 'students', 'localField': '_id', 'foreignField': '_id', 'as': 'student'}},
        {'$unwind': '$student'},
        {'$project': {'_id': 0, 'name': '$student.name', 'averageScore': 1}},
        {'$sort': {'averageScore': -1}}
    ]
    cursor = mongo_collection.aggregate(pipeline)
    
    # Convert the cursor to a list and return it
    return list(cursor)