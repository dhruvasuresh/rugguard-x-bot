# trust_verifier.py
import tweepy
from typing import List, Dict

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
            # Get the user's followers
            followers = self.client.get_users_followers(
                user_id,
                max_results=1000  # Adjust based on API limits
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
