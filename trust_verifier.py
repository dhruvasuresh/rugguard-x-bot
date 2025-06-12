# trust_verifier.py
import tweepy
from typing import List, Dict, Any
from datetime import datetime

class TrustVerifier:
    def __init__(self, client: tweepy.Client):
        self.client = client
        self.trusted_accounts = TRUSTED_ACCOUNTS

    def is_vouched(self, user_id: str) -> Dict:
        """
        Check if a user is followed by trusted accounts
        Returns a dictionary with vouch status and details
        """
        try:
            # Get followers with comprehensive information
            followers = self.client.get_users_followers(
                user_id,
                max_results=1000,
                user_fields=[
                    "created_at",
                    "description",
                    "entities",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    "public_metrics",
                    "url",
                    "username",
                    "verified"
                ],
                expansions=["pinned_tweet_id"]
            )
            
            if not followers.data:
                return {
                    "vouched": False,
                    "vouch_count": 0,
                    "trusted_followers": []
                }
            
            # Check which trusted accounts follow this user
            trusted_followers = []
            for follower in followers.data:
                if follower.username in self.trusted_accounts:
                    trusted_followers.append(follower.username)
            
            vouch_count = len(trusted_followers)
            is_vouched = vouch_count >= 2  # Vouched if followed by at least 2 trusted accounts
            
            return {
                "vouched": is_vouched,
                "vouch_count": vouch_count,
                "trusted_followers": trusted_followers
            }
            
        except Exception as e:
            print(f"Error checking vouch status: {e}")
            return {
                "vouched": False,
                "vouch_count": 0,
                "trusted_followers": []
            }

    def listen_for_trigger(self) -> List[tweepy.Tweet]:
        try:
            # Enhanced tweet monitoring with comprehensive fields
            query = "@projectruggaurd -is:retweet"
            tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=[
                    "created_at",
                    "conversation_id",
                    "public_metrics",
                    "context_annotations",
                    "entities",
                    "author_id",
                    "in_reply_to_user_id",
                    "referenced_tweets",
                    "lang",
                    "source",
                    "possibly_sensitive"
                ],
                expansions=[
                    "author_id",
                    "referenced_tweets.id",
                    "in_reply_to_user_id",
                    "entities.mentions.username",
                    "attachments.media_keys"
                ],
                user_fields=[
                    "created_at",
                    "description",
                    "entities",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    "public_metrics",
                    "url",
                    "username",
                    "verified"
                ],
                media_fields=[
                    "duration_ms",
                    "height",
                    "media_key",
                    "preview_image_url",
                    "type",
                    "url",
                    "width",
                    "public_metrics"
                ],
                max_results=10
            )
            return tweets.data
        except Exception as e:
            print(f"Error listening for trigger: {e}")
            return []

    def analyze_user(self, user_id: str) -> Dict[str, Any]:
        try:
            # Get comprehensive user information
            user = self.client.get_user(
                id=user_id,
                user_fields=[
                    "created_at",
                    "description",
                    "entities",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    "public_metrics",
                    "url",
                    "username",
                    "verified"
                ],
                expansions=["pinned_tweet_id"]
            )
            
            # Get user's tweets with enhanced metrics
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=100,
                tweet_fields=[
                    "created_at",
                    "conversation_id",
                    "public_metrics",
                    "context_annotations",
                    "entities",
                    "in_reply_to_user_id",
                    "referenced_tweets",
                    "lang",
                    "source",
                    "possibly_sensitive"
                ],
                expansions=[
                    "referenced_tweets.id",
                    "in_reply_to_user_id",
                    "entities.mentions.username",
                    "attachments.media_keys"
                ],
                media_fields=[
                    "duration_ms",
                    "height",
                    "media_key",
                    "preview_image_url",
                    "type",
                    "url",
                    "width",
                    "public_metrics"
                ]
            )

            return {
                "user": user,
                "tweets": tweets
            }
        except Exception as e:
            print(f"Error analyzing user: {e}")
            return {}

    def reply_with_report(self, tweet_id: str, analysis: Dict[str, Any]) -> None:
        try:
            # Format the report from analysis data
            report = self._format_report(analysis)
            
            # Create tweet with enhanced features
            self.client.create_tweet(
                in_reply_to_tweet_id=tweet_id,
                text=report,
                user_auth=True,
                media_ids=[],  # Optional: Add media attachments
                poll_options=[],  # Optional: Add poll
                reply_settings='everyone'  # Control who can reply
            )
        except Exception as e:
            print(f"Error replying with report: {e}")

    def _format_report(self, analysis: Dict[str, Any]) -> str:
        """
        Format the analysis data into a readable report
        """
        if not analysis or "user" not in analysis:
            return "Error: Unable to generate report. Analysis data is incomplete."

        user_data = analysis["user"].data
        tweets_data = analysis.get("tweets", {}).data or []

        # Basic user information
        report = f"Trust Report for @{user_data.username}\n\n"
        
        # Account age
        account_age = (datetime.now() - user_data.created_at).days
        report += f"Account Age: {account_age} days\n"
        
        # Verification status
        if user_data.verified:
            report += "Status: Verified Account\n"
        
        # Follower metrics
        metrics = user_data.public_metrics
        report += f"Followers: {metrics.get('followers_count', 0):,}\n"
        report += f"Following: {metrics.get('following_count', 0):,}\n"
        
        # Tweet analysis
        if tweets_data:
            total_tweets = len(tweets_data)
            total_likes = sum(tweet.public_metrics.get('like_count', 0) for tweet in tweets_data)
            total_retweets = sum(tweet.public_metrics.get('retweet_count', 0) for tweet in tweets_data)
            
            report += f"\nTweet Analysis:\n"
            report += f"- Total Tweets Analyzed: {total_tweets}\n"
            report += f"- Average Likes: {total_likes/total_tweets:.1f}\n"
            report += f"- Average Retweets: {total_retweets/total_tweets:.1f}\n"
        
        # Trust indicators
        report += "\nTrust Indicators:\n"
        if account_age > 365:
            report += "- Account > 1 year old\n"
        elif account_age > 180:
            report += "- Account 6-12 months old\n"
        else:
            report += "- Account < 6 months old\n"
        
        # Bio analysis
        if user_data.description:
            report += f"\nBio Analysis:\n"
            report += f"- Length: {len(user_data.description)} characters\n"
            if 'http' in user_data.description.lower():
                report += "- Contains links\n"
            if any(ord(c) > 127 for c in user_data.description):
                report += "- Contains special characters\n"
        
        return report

# Predefined list of trusted accounts
TRUSTED_ACCOUNTS = [
    # Major Solana DeFi Protocols
    "JupiterExchange",
    "RaydiumProtocol", 
    "orca_so",
    "KaminoFinance",
    "MeteoraAG",
    "saros_xyz",
    "DriftProtocol",
    "solendprotocol",
    "MarinadeFinance",
    "jito_labs",
    
    # NFT Projects and Marketplaces
    "MadLads",
    "MagicEden",
    "Lifinity_io",
    "SolanaMBS",
    "DegenApeAcademy",
    "okaybears",
    "famousfoxfed",
    "CetsOnCreck",
    "xNFT_Backpack",
    "tensor_hq",
    
    # Infrastructure and Core Projects
    "wormholecrypto",
    "helium",
    "PythNetwork",
    "solana",
    "solanalabs",
    "phantom",
    "solflare_wallet",
    "solanaexplorer",
    "solanabeach_io",
    "solanafm",
    
    # Additional DeFi and Trading Platforms
    "solanium_io",
    "staratlas",
    "grapeprotocol",
    "mangomarkets",
    "bonfida",
    "medianetwork_",
    "Saber_HQ",
    "StepFinance_",
    "tulipprotocol",
    "SunnyAggregator",
    
    # Notable KOLs and Founders
    "aeyakovenko",      # Anatoly Yakovenko (Solana founder)
    "rajgokal",         # Raj Gokal (Solana co-founder)
    "VinnyLingham",     # Vinny Lingham
    "TonyGuoga",        # Tony G
    "Austin_Federa",    # Austin Federa
    
    # Media and Community
    "Wordcel_xyz",
    "TrutsXYZ",
    "StellarSoulNFT",
    "superteam_xyz",
    "Bunkr_io",
    "candypay_xyz",
    "solanabridge",
    "solana_tourism",
    "MemeDaoSOL",
    
    # Superteam Regional Chapters
    "superteamIND",     # India
    "superteamVN",      # Vietnam
    "superteamDE",      # Germany
    "superteamUK",      # United Kingdom
    "superteamUAE",     # UAE
    "superteamNG",      # Nigeria
    "superteamBalkan",  # Balkans
    "superteamMY",      # Malaysia
    "superteamFR",      # France
    "superteamJP",      # Japan
    "superteamSG",      # Singapore
    "superteamCA",      # Canada
    "superteamTR",      # Turkey
    "superteamTH",      # Thailand
    "superteamPH",      # Philippines
    "superteamMX",      # Mexico
    "superteamBR",      # Brazil
]
