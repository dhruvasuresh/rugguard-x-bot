# account_analyzer.py
import tweepy
from datetime import datetime
from typing import Dict, Any

class AccountAnalyzer:
    def __init__(self, client: tweepy.Client):
        self.client = client

    def analyze_user(self, user_id: str) -> Dict[str, Any]:
        """
        Analyze a Twitter user and return a comprehensive report
        """
        try:
            # Get user information
            user = self.client.get_user(
                id=user_id,
                user_fields=['created_at', 'description', 'public_metrics', 'verified']
            )
            
            if not user.data:
                return {"error": "User not found"}

            # Get recent tweets for analysis
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=100,
                tweet_fields=['public_metrics', 'created_at']
            )

            # Calculate account age
            account_age = datetime.now() - user.data.created_at
            account_age_days = account_age.days

            # Calculate engagement metrics
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            tweet_count = 0

            if tweets.data:
                for tweet in tweets.data:
                    metrics = tweet.public_metrics
                    total_likes += metrics.get('like_count', 0)
                    total_retweets += metrics.get('retweet_count', 0)
                    total_replies += metrics.get('reply_count', 0)
                    tweet_count += 1

            avg_likes = total_likes / tweet_count if tweet_count > 0 else 0
            avg_retweets = total_retweets / tweet_count if tweet_count > 0 else 0
            avg_replies = total_replies / tweet_count if tweet_count > 0 else 0

            # Calculate follower/following ratio
            metrics = user.data.public_metrics
            followers_count = metrics.get('followers_count', 0)
            following_count = metrics.get('following_count', 0)
            follower_ratio = followers_count / following_count if following_count > 0 else 0

            # Analyze bio content
            bio = user.data.description
            bio_length = len(bio)
            bio_has_links = 'http' in bio.lower()
            bio_has_emoji = any(ord(c) > 127 for c in bio)

            return {
                "username": user.data.username,
                "account_age_days": account_age_days,
                "verified": user.data.verified,
                "followers_count": followers_count,
                "following_count": following_count,
                "follower_ratio": round(follower_ratio, 2),
                "bio_length": bio_length,
                "bio_has_links": bio_has_links,
                "bio_has_emoji": bio_has_emoji,
                "avg_likes": round(avg_likes, 2),
                "avg_retweets": round(avg_retweets, 2),
                "avg_replies": round(avg_replies, 2),
                "tweet_count": tweet_count
            }

        except Exception as e:
            print(f"Error analyzing user: {e}")
            return {"error": str(e)}
