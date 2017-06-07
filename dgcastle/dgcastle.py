'''DGCastle: A disc golf statistics tracking tool'''
import collections
import pymongo

from dgcastle.handlers.match_play import MatchPlay

class DGCastle(MatchPlay):
    def __init__(self, testDb=None):
        self.testDb = testDb

        # Setup the MongoDB client
        self.mongoClient = pymongo.MongoClient()
        if not testDb:
            # Production database
            self.db = self.mongoClient.dgcastle
        else:
            self.db = self.mongoClient[testDb]

    def __del__(self):
        if self.testDb and self.testDb != 'dgcastle':
            self.mongoClient.drop_database(self.testDb)
