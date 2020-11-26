import os
import tweepy
import csv
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_TOKEN_SECRET")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

guadalajara_box = [-103.484165,20.545649,-103.199704,20.795536]
mexico_box = [-108.03,18.79,-98.45,25.93]

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


class MyStreamListener(tweepy.StreamListener):
    file = None
    writer = None
    count = 0

    def __init__(self, file):
        super().__init__()
        self.file = file
        self.writer = csv.writer(file, delimiter=';')
        self.writer.writerow(["text", "created", "retweets"])

    def on_status(self, status):
        # Si el tweet no es reply, se toma en cuenta
        if status.in_reply_to_status_id is None:
            self.count += 1
            print(f"write {self.count} - {status.created_at}")
            self.writer.writerow([status.text, status.created_at, status.retweet_count])
            if self.count >= 1000:
                self.file.close()
                exit()


with open("file.csv", "w") as file:
    myStreamListener = MyStreamListener(file)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(locations=mexico_box)
