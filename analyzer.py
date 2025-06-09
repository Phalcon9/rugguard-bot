import tweepy
import os
from datetime import datetime
from textblob import TextBlob
from trusted_accounts import check_trusted_followers

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def analyze_account(user_id):
    try:
        user = client.get_user(id=user_id, user_fields=["created_at", "description", "public_metrics"])
        if not user.data:
            return {"error": "User not found."}

        user_data = user.data
        created_at = user_data.created_at
        followers = user_data.public_metrics["followers_count"]
        following = user_data.public_metrics["following_count"]
        bio = user_data.description or ""

        age_days = (datetime.utcnow() - created_at).days
        follower_ratio = followers / following if following > 0 else followers

        # Bio analysis
        bio_length = len(bio)
        keywords = [kw for kw in ["solana", "rug", "nft", "dev", "crypto"] if kw in bio.lower()]

        # Recent tweet sentiment analysis
        tweets = client.get_users_tweets(id=user_id, max_results=10)
        sentiments = []
        if tweets.data:
            for tw in tweets.data:
                tb = TextBlob(tw.text)
                sentiments.append(tb.sentiment.polarity)

        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

        # Trusted follower check
        is_trusted = check_trusted_followers(client, user_id)

        return {
            "age_days": age_days,
            "followers": followers,
            "following": following,
            "follower_ratio": round(follower_ratio, 2),
            "bio_length": bio_length,
            "bio_keywords": keywords,
            "avg_sentiment": round(avg_sentiment, 3),
            "trusted_by_network": is_trusted
        }

    except Exception as e:
        return {"error": str(e)}
