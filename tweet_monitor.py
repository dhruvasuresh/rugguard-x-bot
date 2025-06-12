# tweet_monitor.py
import tweepy
from typing import List, Optional

class TweetMonitor:
    def __init__(self, client: tweepy.Client):
        self.client = client
        self.trigger_phrase = "@projectruggaurd riddle me this"

    def listen_for_trigger(self) -> List[tweepy.Tweet]:
        """
        Monitor Twitter for replies containing the trigger phrase
        Returns a list of matching tweets
        """
        try:
            # Use Twitter API to fetch recent mentions of @projectruggaurd
            query = "@projectruggaurd -is:retweet"
            tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=["referenced_tweets", "author_id"],
                max_results=10
            )
            
            if not tweets.data:
                return []
            
            # Filter tweets containing the trigger phrase
            matching_tweets = [
                tweet for tweet in tweets.data
                if self.trigger_phrase.lower() in tweet.text.lower()
            ]
            return matching_tweets
            
        except Exception as e:
            print(f"Error monitoring tweets: {e}")
            return []

    def get_original_author_id(self, tweet: tweepy.Tweet) -> Optional[str]:
        """
        Get the ID of the original tweet's author
        Returns None if the original tweet cannot be found
        """
        try:
            # Get the original tweet being replied to
            if not hasattr(tweet, 'referenced_tweets') or not tweet.referenced_tweets:
                return None
                
            reply_tweet = next(
                (ref for ref in tweet.referenced_tweets if ref.type == 'replied_to'),
                None
            )
            
            if not reply_tweet:
                return None
                
            original_tweet = self.client.get_tweet(
                reply_tweet.id,
                user_fields=["id"]
            )
            return original_tweet.data.author_id if original_tweet.data else None
            
        except Exception as e:
            print(f"Error getting original author: {e}")
            return None
