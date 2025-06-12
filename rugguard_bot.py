# rugguard_bot.py
import tweepy
import time
import os
from dotenv import load_dotenv
from tweet_monitor import TweetMonitor
from account_analyzer import AccountAnalyzer
from trust_verifier import TrustVerifier
from report_generator import ReportGenerator

# Load environment variables
load_dotenv()

# Configuration from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Validate environment variables
required_vars = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "ACCESS_TOKEN": ACCESS_TOKEN,
    "ACCESS_TOKEN_SECRET": ACCESS_TOKEN_SECRET,
    "BEARER_TOKEN": BEARER_TOKEN
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    print("Error: Missing required environment variables:")
    for var in missing_vars:
        print(f"- {var}")
    print("\nPlease set these variables in your .env file")
    exit(1)

try:
    # Initialize Tweepy client (v2 for streaming and user lookup)
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True  # Automatically handle rate limits
    )

    # Test authentication
    client.get_me()
    print("Successfully authenticated with Twitter API")

    # Initialize bot components
    tweet_monitor = TweetMonitor(client)
    account_analyzer = AccountAnalyzer(client)
    trust_verifier = TrustVerifier(client)
    report_generator = ReportGenerator(client)

except tweepy.errors.Unauthorized as e:
    print("Error: Twitter API authentication failed")
    print("Please check your API credentials in the .env file")
    exit(1)
except Exception as e:
    print(f"Error initializing Twitter client: {e}")
    exit(1)

def main():
    print("Starting RUGGUARD Trust Bot...")
    while True:
        try:
            # Listen for replies mentioning @projectruggaurd with the phrase
            tweets = tweet_monitor.listen_for_trigger()
            for tweet in tweets:
                # Extract original tweet and author
                original_author_id = tweet_monitor.get_original_author_id(tweet)
                if not original_author_id:
                    continue

                # Analyze the original author
                analysis = account_analyzer.analyze_user(original_author_id)
                
                # Check if vouched by trusted accounts
                vouched = trust_verifier.is_vouched(original_author_id)
                analysis["vouched"] = vouched["vouched"]
                analysis["vouch_count"] = vouched["vouch_count"]
                analysis["trusted_followers"] = vouched["trusted_followers"]

                # Reply with the trustworthiness report
                report_generator.reply_with_report(tweet.id, analysis)
                
        except tweepy.errors.TooManyRequests as e:
            print(f"Rate limit exceeded. Waiting for {e.reset_time} seconds...")
            time.sleep(e.reset_time)
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main() 