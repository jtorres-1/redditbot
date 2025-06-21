# JobBot Reddit Outreach Bot (Replit-ready)

from dotenv import load_dotenv
import os
import praw
import time
import random
import sqlite3
from flask import Flask
from threading import Thread

# === LOAD ENV ===
load_dotenv()

# === CONFIG ===
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

SUBREDDITS = [
    'jobsearchhacks', 'GetEmployed', 'resumes', 'WorkOnline', 'jobs', 'jobbit',
    'cscareerquestions', 'digitalnomad', 'freelance', 'recruitinghell',
    'forhire', 'slavelabour', 'techjobs', 'hiring', 'jobopenings', 'antiwork',
    'careerquestions', 'WorkReform', 'remotework', 'onlineincome',
    'jobhunting', 'learnprogramming', 'cscareerquestionsEU', 'jobsearch',
    'jobhuntingEU', 'jobsearchEU', 'jobsearchCA', 'jobsearchAU', 'jobsearchNZ',
    'jobsearchUK', 'jobsearchNZ', 'jobsearchIE', 'jobsearchSG', 'jobsearchIN',
    'jobsearchPH', 'jobsearchMY', 'jobsearchHK', 'jobsearchTW', 'interviews'
]

KEYWORDS = [
    'resume', 'job', 'application', 'apply', 'cv', 'cover letter', 'work',
    'ghosted', 'interview', 'linkedin', 'indeed', 'hiring', 'automate',
    'tired of applying', 'how to apply'
]

DM_MESSAGES = [
    "Yo I built a bot that applies to 50+ jobs/day. Made sales. Try it 👉 https://linktr.ee/jtxcode",
    "Auto applies to jobs while I sleep. Real results. Check it 👉 https://linktr.ee/jtxcode",
    "Built a job hunter bot. Gets interviews. Simple setup. Demo: https://linktr.ee/jtxcode",
    "I was tired of getting ghosted. This bot finally got me replies 🔥 https://linktr.ee/jtxcode",
    "Applying manually? Don’t. This bot does it for you. No BS 👉 https://linktr.ee/jtxcode",
    "Yo I got tired of applying to jobs every damn day. Built this bot → https://linktr.ee/jtxcode. It literally got me interviews in 48 hrs.",
    "Dead serious — this AI bot helped me go from 0 to interviews while I was sleeping. Setup took 3 mins. https://linktr.ee/jtxcode",
    "Don’t waste time applying manually — this changed everything. Try it → https://linktr.ee/jtxcode"
]

# === PRAW SETUP ===
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD,
                     user_agent=REDDIT_USER_AGENT)

# === DATABASE SETUP ===
conn = sqlite3.connect('messaged_users.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT)')
conn.commit()


def already_messaged(username):
    c.execute("SELECT 1 FROM users WHERE username = ?", (username, ))
    return c.fetchone() is not None


def log_user(username):
    c.execute("INSERT INTO users (username) VALUES (?)", (username, ))
    conn.commit()
    with open("dm_log.txt", "a") as f:
        f.write(f"Messaged u/{username} at {time.ctime()}\n")


# === KEEP ALIVE ===
app = Flask('')


@app.route('/')
def home():
    return "JobBot Outreach is alive!"


def run_flask():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run_flask)
    t.start()


keep_alive()

# === MAIN LOOP ===
while True:
    for sub in SUBREDDITS:
        print(f"Scanning r/{sub}...")
        for comment in reddit.subreddit(sub).comments(limit=50):
            body = comment.body.lower()
            if any(keyword in body for keyword in KEYWORDS):
                user = str(comment.author)
                if not already_messaged(user):
                    try:
                        message = random.choice(DM_MESSAGES)
                        reddit.redditor(user).message(
                            subject="AutoApply Bot 💼", message=message)
                        print(f"[✅] Messaged u/{user}")
                        log_user(user)
                        time.sleep(random.randint(30, 60))
                    except Exception as e:
                        print(f"[❌] Failed to message u/{user}: {e}")
                        time.sleep(10)
        time.sleep(10)
    time.sleep(180)
