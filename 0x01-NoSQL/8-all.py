#!/usr/bin/env python3
"""
Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
        """ List all documents in Python """
        doc = mongo_collection.find()

        if doc.count() == 0:
            return []

        return doc
