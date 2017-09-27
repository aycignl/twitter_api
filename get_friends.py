# Name Surname, email: Gonul AYCI, gonul.ayci@boun.edu.tr
# Location, Date: Bogazici University, Sep. 2017
# Description: This is a function to get friends of Twitter users from their user ids
             # There is limitation from Twitter
             # You can check it on from :
             # https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
             # I use MongoDB collection. This document does not include connection of MongoDB.
             # If you have a trouble with sth about the coding part, feel free to contact with me from my email.

import json 
import time


def get_friends():
    for i in user_collection.find():
        next_cursor = -1
        friends = []
        userid = i['unique_ids']
        
        while True:
            url = "https://api.twitter.com/1.1/friends/ids.json?cursor=" + str(next_cursor) + "&user_id=" + str(userid)

            try:
                response, data = client.request(url)
            except TimeoutError:
                print "TimeoutError, waiting 5 seconds to retry..."
                time.sleep(5)
            except Exception as e:
                print "Some other exception happened. ", e
                print "Waiting 30 seconds to retry..."
                time.sleep(30)
            
            if response.status == 200:
                parsed_data = json.loads(data)
                friends = friends + list(parsed_data['ids'])
                next_cursor = parsed_data.get('next_cursor')
                if next_cursor == 0:
                    break
            elif response.status == 429:
                print float(response['x-rate-limit-reset']) - time.time()
                time.sleep(max(float(response['x-rate-limit-reset']) - time.time(), 0))
            elif response.status >= 400 and response.status < 500:
                print 'User %s is skipped because of status %d' % (str(userid), response.status)
                break
            else:
                print 'Got status: %d trying again...' % response.status
                time.sleep(3)
                continue

        friend_string = ','.join([str(friend) for friend in friends])
    
        d = {"user_id" : userid, "friend_ids" : friend_string}
    
        friend_collection.insert_one(d)
        
if __name__ == '__main__':
    get_friends()
