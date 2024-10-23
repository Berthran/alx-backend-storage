#!/usr/bin/env python3
'''
changes all topics of a school document based on a name
'''


def update_topics(mongo_collection, name, topics):
    '''
    Returns nothing
    '''
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}})


if __name__ == "__main__":
    pass
