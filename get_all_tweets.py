import sys
import csv
import json
import tweepy
consumer_key = "rTsK5XvwvClIms8Ak4XI6ys60" # "your_consumer_key"
consumer_secret = "QlSRHRCk0O269I3s2R8OcrDhsTwlxWYVtfTAXymNUoMRPkozJh" #"your_consumer_secret"
access_key = "705105422546415616-R5QS46h8ryYEvFPkerzBMtkJ4ZArV9C"#"your_access_key"
access_secret = "FTCGIQq0WSvvSIB8mhs3itO6ngKjRXDabt8Kp1xN5mYwA"

def get_tweets(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api=tweepy.API(auth)
    alltweets = []
    number_of_tweets = 200
    tweets = api.user_timeline(screen_name = username, count = number_of_tweets)
    alltweets.extend(tweets)
    oldest = alltweets[-1].id - 1
    while len(tweets) > 0:
        print("getting tweets before %s" % (oldest))
        tweets = api.user_timeline(screen_name = username, count = number_of_tweets, max_id=oldest)
        alltweets.extend(tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
#    with open('%s_tweets.csv' % username, 'wb') as f:
#        writer = csv.writer(f)
#        writer.writerow(["id","created_at","text"])
#        writer.writerows(outtweets)
#    pass

#    tweets_for_csv = [[username,tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]
    print("writing to {0}_tweets.csv".format(username))
    with open ("{0}_tweets.csv".format(username), "w+") as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
#    tweets = tweepy.Cursor(api.user_timeline,id='StockMetrixApp').items()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        get_tweets(sys.argv[1])
    else:
        print("Error: enter one username")
