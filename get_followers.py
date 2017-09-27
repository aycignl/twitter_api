# Name Surname, email: Gonul AYCI, gonul.ayci@boun.edu.tr
# Location, Date: Bogazici University, Sep. 2017
# Description: This is a function to get followers of Twitter users from their the search query.
             # There is limitation from Twitter
             # You can check it on from :
             # https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
             # I use MongoDB collection. This document does not include connection of MongoDB.
             # If you have a trouble with sth about the coding part, feel free to contact with me from my email.

import json 
import time


QUERY = 'arduino'

ENDPOINTS = {
    'followers': 'https://api.twitter.com/1.1/followers/ids.json',
}

next_cursor = -1

def get_followers(username, cursor=-1, nested_count=0):
    if nested_count > 14: # rate limit: max 15 requests in 15 mins
        return []

    params = {
        'screen_name': username,
        'cursor': cursor
    }

    response = requests.get(ENDPOINTS['followers'], auth=auth, params=params)
    
    data = response.json()

    arduino_collection.insert_one(data)

    next_cursor = data['next_cursor']
    
    return data['ids'] + get_followers(username, data['next_cursor'], nested_count+1)

then = time.time()

if __name__ == '__main__':
    diff = 0
    while diff < (16*60):
        diff = time.time() - then # in seconds
        
        sleep_time = 16*60 - diff
        if sleep_time > 0:
            time.sleep(sleep_time)
