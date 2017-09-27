# Name Surname, email: Gonul AYCI, gonul.ayci@boun.edu.tr
# Location, Date: Bogazici University, Sep. 2017
# Description: This is a function to get profiles of Twitter users from their user ids.
             # There is limitation from Twitter
             # You can check it on from :
             # https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup
             # I use MongoDB collection. This document does not include connection of MongoDB.
             # If you have a trouble with sth about the coding part, feel free to contact with me from my email.

import json 


def get_profile(a):
    for i in range(a, a + 299): # rate limit: max 300 request
        userid = ids_collection.find().skip(i*100).limit(100) # to get max 100 user_ids (user_ids should comma seperated)
        str_user = ','.join([str(int_id['ids']) for int_id in userid])
    
        request = '{url}{user_id}'.format(url="https://api.twitter.com/1.1/users/lookup.json?user_id=", user_id=str_user) 
        response, data = client.request(request)
        profile = json.loads(data)
        
        for j in profile:
            profile_collection.insert_one(j)
            
if __name__ == '__main__':
    get_profile(0*300) # 0*300 gets the first 30 000 data, then you should continue 1*300, 2*300, ... respectively.
