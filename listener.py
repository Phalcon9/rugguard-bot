# listener.py

import os
import tweepy
from dotenv import load_dotenv
from analyzer import analyze_account

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

class RugGuardStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Filter: only process tweets that mention the trigger
        if "riddle me this" in tweet.text.lower():
            print(f"Trigger detected in tweet: {tweet.text}")

            # Check if it's a reply to another tweet
            if tweet.referenced_tweets and tweet.referenced_tweets[0].type == "replied_to":
                original_tweet_id = tweet.referenced_tweets[0].id
                print(f"Fetching original tweet ID: {original_tweet_id}")

                # Use client to fetch the original tweet's author
                client = tweepy.Client(bearer_token=BEARER_TOKEN)
                original_tweet = client.get_tweet(original_tweet_id, tweet_fields=["author_id"])

                if original_tweet.data:
                    original_author_id = original_tweet.data["author_id"]
                    print(f"Original author's user ID: {original_author_id}")

                    # Run analysis on the original author
                    report = analyze_account(original_author_id)
                    print("🔍 Trust Report:", report)
                    # ToDo: pass this to replier module

                else:
                    print("❌ Could not fetch original tweet data.")
            else:
                print("❌ The trigger is not a reply to another tweet.")


def listen_for_triggers():
    print("🔍 Starting RugGuard bot listener...")
    stream = RugGuardStream(BEARER_TOKEN)

    # Clear old rules if any
    rules = stream.get_rules().data
    if rules:
        ids = [rule.id for rule in rules]
        stream.delete_rules(ids)

    # Add rule to monitor mentions of @projectrugguard
    stream.add_rules(tweepy.StreamRule("@projectrugguard"))

    # Start streaming
    stream.filter(tweet_fields=["author_id", "in_reply_to_user_id", "referenced_tweets"])
