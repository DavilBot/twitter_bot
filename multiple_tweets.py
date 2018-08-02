import sys
import json
import requests
import time
import urllib
import os.path
import os
import threading
import pandas as pd
from random import randint
import subprocess
from urllib.request import urlretrieve
import telegram
import tweepy
import re
TOKEN = "686702879:AAFS1SlBKg3BVozmdgnVrmctK0-cwkBgykI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(token = TOKEN)
class SubscriberBot():
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self,offset=None):
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def handle_updates(self, updates):
        for update in updates["result"]:
            print(update["message"])
            if 'text' in update["message"]:
                text = update["message"]["text"]
            elif 'document' in update["message"]:
                print(update['message']['document']['file_id'])
                path = bot.getFile(update['message']['document']['file_id'])
                print(path['file_path'])
                url = path['file_path']
                urlretrieve(url,os.path.abspath(str(update['message']['document']['file_name'])))
                text = ""
            else:
                continue
            chat = update["message"]["chat"]["id"]
            name = update["message"]["chat"]["first_name"]
            list_keys = []
            data = {}
            old_message = {}
            tick = []
            if(os.path.isfile('data.json') and os.path.isfile('Old_message.json')):
                with open('data.json', 'r') as fp:
                        data = json.load(fp)
                        if str(name) in data:
                            list_keys = data[str(name)]
                with open('Old_message.json', 'r') as r:
                        old_message = json.load(r)
                        if str(name) in old_message:
                            tick = old_message[str(name)]
            if text == "/start":
                self.send_message("Hello {}! Please type '/' to see all available commands.".format(name), chat)
            elif text == "/cancel":
                old_message[str(name)] = [""]
                with open("Old_message.json", 'w') as f:
                    json.dump(old_message, f)
                self.send_message("You cancelled action", chat)
            elif text == "/save_me" and list_keys != []:
                self.send_message("Your username already saved\nType '/' if you are in trouble", chat)
            elif text == "/save_me" and list_keys == []:
                old_message[str(name)] = [text]
                data[str(name)] = []
                with open("Old_message.json", "w") as fm:
                    json.dump(old_message, fm)
                with open('data.json', 'w') as fp:
                    json.dump(data, fp)
                self.send_message("Please enter using space like this consumerkey consumersecret accesstoken accesstokensecret of your twitter account\nPlease be careful\n"+
                                  "if you don't know or don't have these keys use this link https://chimpgroup.com/knowledgebase/twitter-api-keys/", chat)
            elif tick[0] == "/save_me" and list_keys == []:
                data[str(name)] = text.split()#list of data
                if len(text.split())==4 and len(data[str(name)][0])==25 and len(data[str(name)][1])==50 and len(data[str(name)][2])==50 and len(data[str(name)][3])==45:
                    with open('data.json', 'w') as fp:
                        json.dump(data, fp)
                    self.send_message("Your username is saved", chat)
                    old_message[str(name)] = [text]
                    with open('Old_message.json', 'w') as f:
                        json.dump(old_message, f)
                else:
                    self.send_message("Try again\nYou need to write exactly 4 things listed above using space", chat)
            elif text == "/delete_me":
                data[str(name)] = []
                with open("data.json", "w") as f:
                    json.dump(data,f)
                self.send_message("You are successfully deleted yourself!", chat)
            elif text == "/tweet":
                old_message[str(name)] = [text]
                with open("Old_message.json", "w") as f:
                    json.dump(old_message,f)
                self.send_message("Send your data in such format\n Ticker Company name signal in first message\n photo in another", chat)
            elif tick[0] == "/tweet":
                print(text)
                if text != '' and len(tick)<2 and len(text.split())==3:
                    temp_list = text.split()
                    df = pd.read_csv('sample_tweets.csv', sep = ';')
                    for index, row in df.iterrows():
                        if temp_list[2] in row['text']:
                            while(True):
                                n = randint(0,33)
                                if temp_list[2] in df['text'][n]:
                                    string = df['text'][n]
                                    for s in string.split():
                                        if '$' in s:
                                            string = string.replace(s,'$'+temp_list[0])
                                        if '/' in s:
                                            string = string.replace(s,'')
                                    string = string+' '+temp_list[1]+' company'
                                    break
                            tick.append(string)
                            old_message[str(name)] = tick
                            with open("Old_message.json", "w") as f:
                                json.dump(old_message,f)
                            self.send_message("Now send photo as a file", chat)
                            break
                        else:
                            self.send_message("Try again", chat)
                            break
                elif len(tick)!=1 and text=='':
                    cnf = {
                        "consumer_key" : data[str(name)][0],
                        "consumer_secret" : data[str(name)][1],
                        "access_token" : data[str(name)][2],
                        "access_token_secret" : data[str(name)][3]
                    }
                    api = self.get_api(cnf)
                    tweet = tick[1]
                    image = os.path.abspath(str(update['message']['document']['file_name']))
                    status = api.update_with_media(image, status=tweet)
                    self.send_message("I have posted your tweet",chat)
                    os.remove(str(update['message']['document']['file_name']))
                    old_message[str(name)] = [text]
                    with open("Old_message.json", "w") as f:
                        json.dump(old_message, f)
                else:
                    self.send_message("Read carefully the above instructions",chat)
            else:
                self.send_message("Type '/' to view commands", chat)

    def get_api(self, cnf):
        auth = tweepy.OAuthHandler(cnf['consumer_key'], cnf['consumer_secret'])
        auth.set_access_token(cnf['access_token'], cnf['access_token_secret'])
        return tweepy.API(auth)

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_url(url)

    def build_keyboard(self, items):
        keyboard = items#[[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def main(self):
        last_update_id = None
        self.__init__()
        while True:
            updates = self.get_updates(last_update_id)
            if "result" in updates:
                if len(updates["result"]) > 0:
                    last_update_id = self.get_last_update_id(updates) + 1
                    self.handle_updates(updates)
                time.sleep(0.5)


if __name__ == '__main__':
        obj = SubscriberBot()
        obj.main()

