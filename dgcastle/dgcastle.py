'''DGCastle: A disc golf statistics tracking tool'''
import os
import pymongo

from dgcastle.handlers.match_play import MatchPlay

class DGCastle(MatchPlay):
    def __init__(self, testDb=None):
        self.testDb = testDb

        # Setup the MongoDB client
        
        # Production database
        if os.environ.get('MONGODB_URI'): # pragma: no cover
            self.mongoClient = pymongo.MongoClient(os.environ['MONGODB_URI'])
            self.db = self.mongoClient.dgcastle
            print("Using production database!")
        else:
            self.mongoClient = pymongo.MongoClient()
            if not testDb:  # pragma: no cover
                self.mongoClient.dgcastle
            else:
                self.db = self.mongoClient[testDb]

    def __del__(self):
        if self.testDb and self.testDb != 'dgcastle':
            self.mongoClient.drop_database(self.testDb)
