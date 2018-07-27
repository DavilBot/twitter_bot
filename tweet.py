import tweepy
import os
def get_api(cnf):
    auth = tweepy.OAuthHandler(cnf['consumer_key'], cnf['consumer_secret'])
    auth.set_access_token(cnf['access_token'], cnf['access_token_secret'])
    return tweepy.API(auth)
def main():
    cnf = {
        "consumer_key" : "OF1bZajxBLHMkeHBbiYsCjTUv",
        "consumer_secret" : "dbPal7XcilAQHkTxaACVzvlBtyqijgMxueD6xUJa8d7zQovplk",
        "access_token" : "705105422546415616-ZE9wEdEvYJ748JQKtdE0P9tBISoiuUt",
        "access_token_secret" : "Sa7D4ZGvgHXykDwxwjXefVFWa1I5FQCh2NM6k6KnHemnP"
    }
    api = get_api(cnf)
    image = os.path.abspath("tweet_image1.jpeg")
    tweet = "Hello world! \n http://www.leancrew.com/all-this/2012/01/tweeting-images/"
    status = api.update_with_media(image ,status=tweet)
if __name__ == "__main__":
    main()
