import pymongo

class Database(object):
  URI = "mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net"
  DATABASE = 'annotations'
  COLLECTION = 'annotations'

  @staticmethod
  def initialize():
    client = pymongo.MongoClient(Database.URI)
    Database.DATABASE = client['annotations']

  @staticmethod
  def insert(collection, data):
    Database.DATABASE[collection].insert_one(data)



Database.initialize()

