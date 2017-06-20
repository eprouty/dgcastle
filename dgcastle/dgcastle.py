'''DGCastle: A disc golf statistics tracking tool'''
import os
import pymongo

from dgcastle.handlers.match_play import MatchPlay
from dgcastle.handlers.challonge import Challonge

class DGCastle(Challonge, MatchPlay):
    def __init__(self, testDb=None):
        super().__init__()

        self.testDb = testDb
        
        if os.environ.get('MONGODB_URI'): # pragma: no cover
            # Production database
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
