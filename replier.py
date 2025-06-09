import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Auth for v1.1 endpoint (needed to post tweets)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def post_trust_reply(trigger_tweet_id, report):
    if "error" in report:
        text = "⚠️ Could not analyze the account. Please try again later."
    else:
        text = (
            f"🔍 Trust Report:\n"
            f"• Account Age: {report['age_days']} days\n"
            f"• F/F Ratio: {report['follower_ratio']}\n"
            f"• Bio Keywords: {', '.join(report['bio_keywords']) or 'None'}\n"
            f"• Sentiment: {report['avg_sentiment']}\n"
            f"• Trusted by Network: {'Yes ✅' if report['trusted_by_network'] else 'No ❌'}\n"
            f"\n🛡️ Verdict: {'✅ Trustworthy' if report['trusted_by_network'] or (report['follower_ratio'] > 2 and report['avg_sentiment'] > 0) else '⚠️ Caution'}"
        )

    try:
        api.update_status(status=text, in_reply_to_status_id=trigger_tweet_id, auto_populate_reply_metadata=True)
        print("✅ Reply posted successfully.")
    except Exception as e:
        print(f"❌ Failed to post reply: {e}")
