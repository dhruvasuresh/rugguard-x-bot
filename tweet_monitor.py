# tweet_monitor.py
import tweepy
from typing import List, Dict, Any, Optional
import time
from datetime import datetime, timedelta
import random

class TweetMonitor:
    def __init__(self, client: tweepy.Client):
        self.client = client
        self.trigger_phrase = "riddle me this"
        self.target_account = "projectrugguard"
        self.last_check_time = datetime.now()
        self.processed_tweets = set()  # Keep track of processed tweets
        self.rate_limit_reset = None
        self.backoff_time = 60  # Start with 1 minute backoff
        self.max_backoff = 900  # Maximum 15 minutes backoff
        self.min_results = 10  # Twitter API minimum requirement
        self.last_api_call = datetime.now()
        self.min_api_interval = 2  # Minimum seconds between API calls

    def _handle_rate_limit(self, e: tweepy.errors.TooManyRequests) -> None:
        """Handle rate limit with exponential backoff"""
        if hasattr(e, 'reset_time'):
            self.rate_limit_reset = datetime.now() + timedelta(seconds=e.reset_time)
            wait_time = e.reset_time
        else:
            # If no reset time provided, use exponential backoff
            wait_time = min(self.backoff_time * 2, self.max_backoff)
            self.backoff_time = wait_time
            self.rate_limit_reset = datetime.now() + timedelta(seconds=wait_time)
        
        print(f"Rate limit hit. Waiting {wait_time} seconds before next check...")
        time.sleep(wait_time)
        self.backoff_time = max(60, self.backoff_time // 2)  # Reset backoff after successful wait
        self.last_api_call = datetime.now()  # Reset last API call time

    def _should_wait(self) -> bool:
        """Check if we should wait before making another API call"""
        # Check rate limit reset time
        if self.rate_limit_reset and datetime.now() < self.rate_limit_reset:
            wait_seconds = (self.rate_limit_reset - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"Rate limit: Waiting {int(wait_seconds)} seconds before next check...")
                time.sleep(min(wait_seconds, 60))  # Sleep in chunks of max 60 seconds
                return True

        # Check minimum interval between API calls
        time_since_last_call = (datetime.now() - self.last_api_call).total_seconds()
        if time_since_last_call < self.min_api_interval:
            sleep_time = self.min_api_interval - time_since_last_call
            time.sleep(sleep_time)
            return True

        return False

    def listen_for_trigger(self) -> List[Dict[str, Any]]:
        """
        Monitor tweets for trigger phrase with improved rate limit handling
        """
        if self._should_wait():
            return []

        try:
            # Get @projectrugguard's user ID
            user = self.client.get_user(username="projectrugguard")
            self.last_api_call = datetime.now()
            
            if not user.data:
                print("Could not find @projectrugguard user")
                return []
            
            user_id = user.data.id
            
            # Get recent tweets from @projectrugguard
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=self.min_results,
                tweet_fields=["conversation_id", "created_at"],
                exclude=["retweets", "replies"]
            )
            self.last_api_call = datetime.now()
            
            if not tweets.data:
                return []
            
            triggered_tweets = []
            
            for tweet in tweets.data:
                if tweet.id in self.processed_tweets:
                    continue
                
                try:
                    # Get replies to this tweet
                    replies = self.client.search_recent_tweets(
                        query=f"conversation_id:{tweet.conversation_id}",
                        tweet_fields=["referenced_tweets", "author_id", "conversation_id"],
                        max_results=self.min_results
                    )
                    self.last_api_call = datetime.now()
                    
                    if replies.data:
                        for reply in replies.data:
                            if "riddle me this" in reply.text.lower():
                                triggered_tweets.append({
                                    "tweet_id": tweet.id,
                                    "author_id": tweet.author_id,
                                    "conversation_id": tweet.conversation_id,
                                    "trigger_reply": reply
                                })
                                self.processed_tweets.add(tweet.id)
                    
                    # Clean up old processed tweets
                    if len(self.processed_tweets) > 100:
                        self.processed_tweets = set(list(self.processed_tweets)[-100:])
                    
                    # Add small random delay between API calls
                    time.sleep(random.uniform(2, 5))  # Increased delay to be more conservative
                    
                except tweepy.errors.TooManyRequests as e:
                    self._handle_rate_limit(e)
                    break
                except Exception as e:
                    print(f"Error processing tweet {tweet.id}: {e}")
                    continue
            
            return triggered_tweets
            
        except tweepy.errors.TooManyRequests as e:
            self._handle_rate_limit(e)
            return []
        except Exception as e:
            print(f"Error in listen_for_trigger: {e}")
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
                
            try:
                original_tweet = self.client.get_tweet(
                    reply_tweet.id,
                    user_fields=["id"]
                )
                return original_tweet.data.author_id if original_tweet.data else None
            except tweepy.errors.TooManyRequests as e:
                print(f"Rate limit exceeded. Waiting for {e.reset_time} seconds...")
                time.sleep(e.reset_time)
                return None
            
        except Exception as e:
            print(f"Error getting original author: {e}")
            return None
