import hashlib
from datetime import datetime
# import redis
from pymongo import MongoClient



class MongoManager(object):

    def __init__(self, server_ip='localhost', client=None):
        print(server_ip)
        self.client = MongoClient(server_ip, 27017) if client is None else client
        # self.redis_client = redis.StrictRedis(host=server_ip, port=6379, db=0)
        self.mongo_db = self.client.flask_database

    # def check_query(self, query):
    #     num = self.redis_client.get(query)
    #     return True if num is not None else False

    def save_query(self, query, prediction):
        # self.redis_client.set(query, 1)
        self.mongo_db.query.insert({
            '_id': hashlib.md5(query.encode('utf-8')).hexdigest(),
            'query': query,
            'time': datetime.utcnow(),
            'prediction': [prediction]
        })

    def update_dup_query(self, dup_id, prediction):
        # self.redis_client.set(query, 1)
        # db.collection.update({"name": "test"}, {"$set": {"age": 33}})
        #即database.collection
        self.mongo_db.query.update(
            {'_id':dup_id},
            {'$push':{'prediction':prediction}}

            # '_id': hashlib.md5(query.encode('utf-8')).hexdigest(),
            # 'time': datetime.utcnow(),
            # 'prediction': prediction
        )

    def get_result(self, query):
        id = hashlib.md5(query.encode('utf-8')).hexdigest()
        result = self.mongo_db.query.find_one({'_id': id})
        return result['prediction']

    def clear(self):
        self.mongo_db.query.drop()