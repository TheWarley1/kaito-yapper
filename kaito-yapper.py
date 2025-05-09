import time
import tweepy
import json
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta

# === Load environment variables ===
load_dotenv()

# === Twitter API Client ===
client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# === Helpers ===
def select_file():
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]
    if not txt_files:
        print("❌ No .txt files found in this folder.")
        return None
    print("📁 Available tweet files:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}. {file}")
    while True:
        try:
            choice = int(input("Select file number: "))
            if 1 <= choice <= len(txt_files):
                return txt_files[choice - 1]
        except ValueError:
            pass
        print("❌ Invalid choice. Try again.")

def load_tweets(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [t.strip() for t in f.read().split("\n\n") if t.strip()]

def check_tweet_length(tweet):
    return len(tweet) <= 280

def post_tweet(text, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            if not check_tweet_length(text):
                print(f"⚠️ Tweet too long ({len(text)}): {text[:50]}...")
                return False
            response = client.create_tweet(text=text)
            print(f"✅ Tweeted: {text[:60].replace(chr(10), ' ')}...")
            return True
        except tweepy.TooManyRequests as e:
            reset = int(e.response.headers.get("x-rate-limit-reset", time.time() + 900))
            wait = reset - int(time.time()) + random.randint(1, 5)
            print(f"🚫 Rate limit hit. Skipping tweet. Try again in {wait}s.")
            return False
        except tweepy.TweepyException as e:
            print(f"❌ Tweepy error: {e}")
            retries += 1
            time.sleep(2 ** retries + random.randint(1, 3))
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    return False

def load_posted():
    if os.path.exists("posted_tweets.json"):
        with open("posted_tweets.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_posted(posted_set):
    with open("posted_tweets.json", "w", encoding="utf-8") as f:
        json.dump(list(posted_set), f)

def post_random_tweets(tweets, count, duration_minutes):
    total_seconds = duration_minutes * 60
    posted = load_posted()

    # Filter out already posted tweets
    available = [t for t in tweets if t not in posted]
    if count > len(available):
        print(f"⚠️ Only {len(available)} unique tweets available.")
        count = len(available)

    selected = random.sample(available, count)
    delays = sorted([random.randint(0, total_seconds) for _ in range(count)])

    print(f"\n🗓 Scheduling {count} tweets over {duration_minutes} minutes.")
    start_time = datetime.now()

    for i, (delay, tweet) in enumerate(zip(delays, selected)):
        now = datetime.now()
        target = start_time + timedelta(seconds=delay)
        wait_time = (target - now).total_seconds()
        wait_time = max(0, wait_time)

        while wait_time > 0:
            mins, secs = divmod(int(wait_time), 60)
            print(f"\r⏱ Posting in {mins:02}:{secs:02}...", end="", flush=True)
            time.sleep(1)
            wait_time -= 1
        print("\r📤 Posting tweet...                     ")

        if post_tweet(tweet):
            posted.add(tweet)
            save_posted(posted)

# === Main ===
def main():
    print("=" * 50)
    print("🚀 Random Tweet Poster")
    print("=" * 50)

    file_path = select_file()
    if not file_path:
        return

    tweets = load_tweets(file_path)
    if not tweets:
        print("No tweets found.")
        return

    print(f"📝 Loaded {len(tweets)} tweets.")
    long_tweets = [t for t in tweets if not check_tweet_length(t)]
    if long_tweets:
        print(f"❌ {len(long_tweets)} tweets are too long:")
        for i, t in enumerate(long_tweets, 1):
            print(f"{i}: {len(t)} chars → {t[:60]}")
        return
    print("✅ All tweets are valid.")

    try:
        count = int(input("How many tweets to post? (e.g. 3): "))
        duration = int(input("Over how many minutes? (e.g. 60): "))
        post_random_tweets(tweets, count, duration)
    except ValueError:
        print("❌ Invalid input. Exiting.")

if __name__ == "__main__":
    main()
