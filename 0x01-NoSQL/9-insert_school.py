#!/us/bin/env python3
'''
Insert a new document to a collection
'''


def insert_school(mongo_collection, **kwargs):
    '''
    Returns the new _id attribute of the docu
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id


if __name__ == "__main__":
    pass
