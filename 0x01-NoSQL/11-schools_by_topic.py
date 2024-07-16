#!/usr/bin/env python3
""" MongoDB Operations with Python """


def schools_by_topic(mongo_collection, topic):
    """ returns the list of school having a specific topic """
    docu = mongo_collection.find({"topics": topic})
    docs = [d for d in docu]
    return docs
