#!/usr/bin/env python3
def list_all(mongo_collection):
    '''
    Function that lists all documents in a collection
    Arg:
        mongo_collection
    '''

    cursor = mongo_collection.find({})
    documents = []
    for document in cursor:
        documents.append(document)
    return documents