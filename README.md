# Project RUGGUARD Twitter Bot

A Twitter bot that analyzes account trustworthiness when triggered by the phrase "@projectrugguard riddle me this" in a reply. The bot is specifically designed for the Solana ecosystem to help users assess the trustworthiness of token projects and accounts.

## How It Works

### Trigger Mechanism
1. The bot monitors Twitter for replies containing "@projectrugguard riddle me this"
2. When found, it identifies the original tweet being replied to
3. The bot then analyzes the original tweet's author (not the person who replied)

### Analysis Process
The bot performs a comprehensive analysis of the original tweet's author:

1. **Account Age Analysis**
   - Calculates account age in days
   - Flags accounts less than 6 months old
   - Highlights accounts older than 1 year

2. **Follower Analysis**
   - Calculates follower/following ratio
   - Identifies accounts with more followers than following
   - Flags accounts with suspicious follower ratios

3. **Bio Analysis**
   - Checks bio length
   - Identifies presence of links
   - Detects emoji usage
   - Analyzes content for suspicious patterns

4. **Engagement Analysis**
   - Calculates average likes per tweet
   - Calculates average retweets per tweet
   - Calculates average replies per tweet
   - Analyzes engagement patterns

5. **Trusted Account Verification**
   - Checks if the account is followed by trusted Solana ecosystem accounts
   - Considers an account "vouched" if followed by at least 2 trusted accounts
   - Lists the trusted accounts that follow the analyzed account

### Trust Report
The bot generates a detailed trust report including:
- Account age status
- Verification status
- Follower ratio analysis
- Bio content analysis
- Engagement metrics
- Trusted account vouches
- Comprehensive statistics

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Twitter Developer Account with API access
- Required API credentials:
  - API Key
  - API Secret
  - Access Token
  - Access Token Secret
  - Bearer Token

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-rugguard-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Twitter API credentials:
   ```
   API_KEY=your_api_key
   API_SECRET=your_api_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   BEARER_TOKEN=your_bearer_token
   ```

4. Run the bot:
   ```bash
   python rugguard_bot.py
   ```

## Project Structure

```
project-rugguard-bot/
├── rugguard_bot.py      # Main bot logic and entry point
├── tweet_monitor.py     # Twitter stream monitoring
├── account_analyzer.py  # Account analysis logic
├── trust_verifier.py    # Trust verification system
├── report_generator.py  # Report generation and posting
├── requirements.txt     # Project dependencies
└── .env                # Environment variables (create this)
```

### Key Components

1. **rugguard_bot.py**
   - Initializes Twitter API client
   - Manages environment variables
   - Coordinates bot components
   - Handles rate limiting and errors
   - Provides detailed timing logs for operations

2. **tweet_monitor.py**
   - Monitors Twitter for trigger phrases
   - Identifies original tweet authors
   - Manages tweet stream processing
   - Implements sophisticated rate limit handling
   - Maintains minimum API call intervals

3. **account_analyzer.py**
   - Performs comprehensive account analysis
   - Calculates trust metrics
   - Generates analysis data

4. **trust_verifier.py**
   - Maintains list of trusted Solana ecosystem accounts
   - Checks account vouching status
   - Manages trusted account relationships

5. **report_generator.py**
   - Formats analysis results
   - Generates trust reports
   - Posts replies to trigger tweets

## Trusted Accounts

The bot maintains a comprehensive list of trusted accounts from the Solana ecosystem, including:
- Major DeFi Protocols
- NFT Projects and Marketplaces
- Infrastructure and Core Projects
- Notable KOLs and Founders
- Media and Community accounts
- Superteam Regional Chapters

An account is considered "vouched" if it is followed by at least 2 trusted accounts from this list.

## Error Handling

The bot includes robust error handling for:
- API rate limits
- Authentication issues
- Network errors
- Invalid responses
- Missing data

## Rate Limiting

The bot implements sophisticated rate limit handling:
- Minimum 2-second interval between API calls
- Exponential backoff (starting at 60 seconds, max 15 minutes)
- Automatic rate limit detection and handling
- Random delays (2-5 seconds) between tweet processing
- Twitter API v2 requirements compliance (minimum 10 tweets per request)
- Detailed timing logs for monitoring performance

## Operation Timing

The bot provides detailed timing logs for each operation:
- Trigger tweet detection
- Account analysis start
- Trust verification
- Report generation and posting
- Rate limit handling and delays

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

