# report_generator.py
import tweepy
from typing import Dict, Any

class ReportGenerator:
    def __init__(self, client: tweepy.Client):
        self.client = client

    def reply_with_report(self, tweet_id: str, analysis: Dict[str, Any]) -> None:
        """
        Format and post a trustworthiness report as a reply
        """
        try:
            if "error" in analysis:
                self.client.create_tweet(
                    in_reply_to_tweet_id=tweet_id,
                    text=f"Error analyzing account: {analysis['error']}"
                )
                return

            # Format the report
            report = self._format_report(analysis)
            
            # Post the reply
            self.client.create_tweet(
                in_reply_to_tweet_id=tweet_id,
                text=report
            )

        except Exception as e:
            print(f"Error posting reply: {e}")
            try:
                self.client.create_tweet(
                    in_reply_to_tweet_id=tweet_id,
                    text="Error generating trust report. Please try again later."
                )
            except:
                pass

    def _format_report(self, analysis: Dict[str, Any]) -> str:
        """
        Format the analysis into a readable report
        """
        # Trust indicators
        trust_indicators = []
        
        # Account age
        if analysis["account_age_days"] > 365:
            trust_indicators.append("Account > 1 year old")
        elif analysis["account_age_days"] > 180:
            trust_indicators.append("Account 6-12 months old")
        else:
            trust_indicators.append("Account < 6 months old")

        # Verification status
        if analysis["verified"]:
            trust_indicators.append("Verified account")

        # Follower ratio
        if analysis["follower_ratio"] > 1:
            trust_indicators.append("More followers than following")
        elif analysis["follower_ratio"] > 0.5:
            trust_indicators.append("Moderate follower ratio")
        else:
            trust_indicators.append("Low follower ratio")

        # Bio analysis
        if analysis["bio_has_links"]:
            trust_indicators.append("Bio contains links")
        if analysis["bio_has_emoji"]:
            trust_indicators.append("Bio contains emojis")

        # Engagement metrics
        if analysis["avg_likes"] > 10:
            trust_indicators.append("Good engagement (likes)")
        if analysis["avg_retweets"] > 5:
            trust_indicators.append("Good engagement (retweets)")

        # Vouch status
        if analysis.get("vouched", False):
            trust_indicators.append(f"Vouched by {analysis.get('vouch_count', 0)} trusted accounts")
            if analysis.get("trusted_followers"):
                trust_indicators.append(f"Trusted followers: {', '.join(analysis['trusted_followers'][:3])}")

        # Format the report
        report = f"Trust Report for @{analysis['username']}\n\n"
        report += "\n".join(trust_indicators)
        report += f"\n\nStats:"
        report += f"\n• {analysis['followers_count']:,} followers"
        report += f"\n• {analysis['following_count']:,} following"
        report += f"\n• {analysis['tweet_count']:,} tweets analyzed"
        report += f"\n• Account age: {analysis['account_age_days']} days"
        
        return report

