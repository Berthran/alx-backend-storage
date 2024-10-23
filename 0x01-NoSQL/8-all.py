#!/usr/bin/env python3
'''
Lists all documents in a collection
'''


def list_all(mongo_collection):
    '''
    returns all documents in a collection
    '''
    docCount = mongo_collection.count_documents({})
    if docCount == 0:
        return []
    return list(mongo_collection.find())


if __name__ == "__main__":
    pass
