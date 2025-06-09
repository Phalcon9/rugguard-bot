# trusted_accounts.py

import requests

TRUST_LIST_URL = "https://raw.githubusercontent.com/devsyrem/turst-list/main/list"


def fetch_trusted_accounts():
    try:
        response = requests.get(TRUST_LIST_URL)
        response.raise_for_status()
        usernames = [line.strip().lower() for line in response.text.splitlines() if line.strip() and not line.startswith("#")]
        return usernames
    except Exception as e:
        print(f"❌ Failed to fetch trusted accounts list: {e}")
        return []


def check_trusted_followers(client, target_user_id):
    trusted_accounts = fetch_trusted_accounts()
    match_count = 0

    for username in trusted_accounts:
        try:
            user = client.get_user(username=username)
            follower = client.get_users_following(id=user.data.id, max_results=1000)
            if follower.data:
                followed_ids = [f.id for f in follower.data]
                if target_user_id in followed_ids:
                    match_count += 1
        except Exception as e:
            print(f"⚠️ Skipping {username}: {e}")

        if match_count >= 3:
            break

    return match_count >= 3
