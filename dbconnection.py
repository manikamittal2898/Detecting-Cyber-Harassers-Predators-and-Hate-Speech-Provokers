#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system(' python -m pip install pymongo')


# In[84]:


import pymongo
from pymongo import MongoClient

class mongoConnect2:
    
    db_url ="mongodb://localhost:27017/?readPreference=primary&ssl=false"
    
    db_name = "error-logs"
    
    collection_name = "col"

    

    

    def __init__(self):
        try:
            self.Client = MongoClient(self.db_url, maxPoolSize=100)
            
            print('Connection established!')
        except Exception as e:
            print('Connection failed due to an error! Error: ',e)


    def push_to_db(self, username, val ):
        collection = self.Client[self.db_name][self.collection_name]
        x=0
        y="Not Flagged"
        # collection.createIndex( { "user_name": 1 }, { unique: true } )
        # try:
#         print("in try")
#         print(collection.find_one({"username":username},{'_id': 0, "score": 1}))
        if (bool(collection.find_one({"username":username},{'_id': 0, "score": 1}))):
            x = collection.find({"username":username},{'_id': 0, "score": 1}).next()['score']
            y = collection.find({"username":username},{'_id': 0, "status":1}).next()['status']
#         else:
#             x=0
#             y="Not Flagged"
#         if (collection.find({'username': username})):
#             x =collection.find({'username': username})
            # y = collection.find({},{'_id': 0,'username': 0, "score": 0, "status":1})
#             print("in if")
        print(x)
        print(y)

        
        query = { "username": username }

        update_val = {
#           "$set": {
            "username": username,
            
            "score": x+val,
            "status":y
          }
#         }
        collection.replace_one( query, update_val, upsert=True )
        print('Successfully pushed the documents!')
        score_new = collection.find({},{'username': 0, "score": 1, "status":0})
#         check_threshold(username,score_new )
        # except:
        #     print('Connection Error')


    def check_threshold(self, username ):
    #         try:
        threshold=6
        collection = self.Client[self.db_name][self.collection_name]
        score= collection.find_one({"username":username},{'_id': 0, "score": 1})['score']
        print(score)
        if score>= threshold:
            query = { "username": username }

            update_val = {
                            "$set": {
                      "username": username,

                      "score": score,
                      "status":"Flagged"
                            }
                  }
            collection.update_one( query, update_val )
            print("Profile has been flagged")
        else:
            print("Profile is not flagged yet")
    #         except:
    #             print('Connection Error')


# In[85]:


mc = mongoConnect2()
# print(getattr(mc,"push_to_db"))
mc.push_to_db("Munnu",0)
mc.check_threshold("Manika@2898")

