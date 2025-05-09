# 🐦 Kaito Yapper

A Python script to post random tweets from a `.txt` file at scheduled intervals using the Twitter API (via `tweepy`).

## 📦 Features

- Randomly selects and schedules tweets over a given time duration
- Ensures tweets do not exceed Twitter’s 280-character limit
- Avoids re-posting the same tweets
- Handles Twitter rate limits and retry logic
- Simple CLI interface for file selection and configuration

---

## ⚙️ Requirements

- Python 3.7+
- Twitter Developer Account
- A Bearer Token and OAuth 1.0a credentials
- `.env` file with your Twitter API credentials

---

## 🛠 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/TheWarley1/kaito-yapper.git
cd kaito-yapper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```


3. Create a `.env` file in the root folder and add your Twitter API credentials:

```bash
touch .env
```
```bash
API_KEY=your_api_key
API_SECRET=your_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```

4. Create a `replies.txt` file with your reply messages (one per line):


---

## 🧪 How to Run

Run the bot with:

```bash
python kaito-yapper.py
```
Or whatever you saved your script as.


##You will be prompted to:

1. Select a .txt file with your tweets

2. Enter how many tweets to post

3. Enter the duration (in minutes) to spread them over random intervals.



## 🧠 Notes
Already posted tweets are tracked in posted_tweets.json to avoid duplicates.

-If no .txt files are found, the script will exit.

-Tweets longer than 280 characters are skipped.

-Rate limits are respected, and retries are attempted on failure.



## 🧼 Resetting Posted Tweets
To clear posted history, delete posted_tweets.json:
```
rm posted_tweets.json
```

## 🧾 License
MIT License


