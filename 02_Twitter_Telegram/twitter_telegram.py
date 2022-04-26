import tweepy
import os
from dotenv import load_dotenv
from datetime import date
import requests

load_dotenv()


class TwitterForwarder:
    TWITTER_STATUS_URL = "https://twitter.com/twitter/statuses/"
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    def __init__(self):
        self.twitter_client = tweepy.Client(os.getenv("TWITTER_BEARER_TOKEN"))
        self.telegram_api_url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}"

    def run(self):
        twitt_url = self._get_twitt_url()
        if twitt_url:
            self._send_telegram_message(twitt_url)

    def _get_twitt_url(self):
        query = self._build_twitter_query()
        tweets = self.twitter_client.search_recent_tweets(query=query)

        if tweets.data:
            tweet = tweets.data[0]
            return f"{self.TWITTER_STATUS_URL}{tweet.id}"

        return None

    def _send_telegram_message(self, message: str):
        params = {"chat_id": self.TELEGRAM_CHAT_ID, "text": message}
        requests.get(f"{self.telegram_api_url}/sendMessage", params=params)

    def _get_today_as_str(self):
        today = date.today()
        return date.strftime(today, "%d/%m/%y")

    def _build_twitter_query(self):
        today_str = self._get_today_as_str()
        return f"from:angelmartin_nc -is:retweet has:media (Informativo matinal para ahorrar tiempo {today_str})"


if __name__ == "__main__":
    TwitterForwarder().run()
