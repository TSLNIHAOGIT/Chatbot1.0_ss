import pymongo
from pymongo import MongoClient
import sys,os
ENV_PATH = '../ENV/'
sys.path.append(os.path.join(os.path.dirname(__file__), ENV_PATH))
from env import ENV
from LOG import Logger
import datetime as dt


class DB:
    def __init__(self,host=None,port=None,debug=False,id_increment=True,db=None,collection=None):
        """
        host: mongo db host, default to chatbotdb
        port: mongo db port, default to 27017
        debug: False - in debug, data will be inserted into different Collections
        id_increment: if the id is increased numerally. default to True
        db: database default to 'chatbotdb'
        collection: default to chat
        """
        self.log = Logger(self.__class__.__name__,level=ENV.DB_LOG_LEVEL.value).logger
        self.debug = debug
        self.id_increment=id_increment
        self._load_client(host,port)
        self._get_db(db)
        self._get_collection(collection)
        
    def _load_client(self,host=None,port=None):
        if host is None:
            host = 'chatbotdb'
        if port is None:
            port = 27017
        self.client = MongoClient(host,port)
        self.log.info('get mongodb client. host is:{}, port is: {}'.format(host,port))
            
    def _get_db(self,db=None):
        if db is None:
            db = 'chatbotdb'
        if self.debug:
            db = db + '_debug'
        self.db = self.client[db]
        self.log.info('mongodb database is: {}'.format(db))
        
            
    def _get_collection(self,collection=None):
        if collection is None:
            collection = 'chat'
        if self.debug:
            collection = collection + '_debug'
        self.collection = self.db[collection]
        self.log.info('mongodb collection is: {}'.format(collection))
        
    def drop_collection(self):
        textin = input('You are about to drop collection: {}. Please type in the name to confirm'.format(self.collection.name))
        if textin == self.collection.name:
            self.collection.drop()
            self.log.info('{} was dropped!'.format(self.collection.name))
            
    def drop_database(self):
        textin = input('You are about to drop database: {}. Please type in the name to confirm'.format(self.db.name))
        if textin == self.db.name:
            self.client.drop_database(self.db.name)
            self.log.info('DB {} was dropped!'.format(self.db.name))
            
    def insert(self,obj={}):
        obj.update({'lastUpdateDate':dt.datetime.utcnow()})
        if self.id_increment:
            obj.update({'_id':self.collection.count_documents(filter={})+1})
        insert_id = self.collection.insert_one(obj).inserted_id
        self.log.info('{} was inserted into collection: {}'.format(insert_id,self.collection.name))
        
    
        