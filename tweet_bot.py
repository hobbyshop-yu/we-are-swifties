#!/usr/bin/env python3
"""
We are Swifties - Twitter Auto Tweet Bot
1日3回ランダムに曲紹介ツイートを投稿する

使い方:
  1. .env ファイルにX APIキーを設定
  2. pip install tweepy python-dotenv
  3. python tweet_bot.py        # 1回投稿
  4. python tweet_bot.py --setup # Windows Task Scheduler登録
"""
import os, re, json, random, sys, argparse, subprocess, io
from datetime import datetime, timedelta
from pathlib import Path

# Windows cp932対策: stdoutをutf-8に
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- 設定 ---
SCRIPT_DIR = Path(__file__).parent
TWEETS_FILE = SCRIPT_DIR / "tweets_all_songs.md"
POSTED_FILE = SCRIPT_DIR / "tweet_bot_posted.json"
LOG_FILE = SCRIPT_DIR / "tweet_bot.log"

def log(msg):
    """ログ出力"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

def load_tweets():
    """tweets_all_songs.md からツイートを読み込む"""
    with open(TWEETS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tweets = []
    # パターン: ### タイトル\n\n```\nツイート本文\n```
    pattern = r'### (.+?)\n\n```\n(.*?)\n```'
    for m in re.finditer(pattern, content, re.DOTALL):
        title = m.group(1).strip()
        body = m.group(2).strip()
        tweets.append({"title": title, "body": body})
    
    return tweets

def load_posted():
    """投稿済みリストを読み込む"""
    if POSTED_FILE.exists():
        with open(POSTED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"posted": [], "history": []}

def save_posted(data):
    """投稿済みリストを保存"""
    with open(POSTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def pick_tweet(tweets, posted_data):
    """未投稿のツイートからランダムに1つ選ぶ"""
    posted_titles = set(posted_data["posted"])
    available = [t for t in tweets if t["title"] not in posted_titles]
    
    if not available:
        # 全曲投稿済み → リセットして最初から
        log("全219曲投稿完了！リセットして最初からスタート。")
        posted_data["posted"] = []
        posted_data["cycle"] = posted_data.get("cycle", 0) + 1
        save_posted(posted_data)
        available = tweets
    
    return random.choice(available)

def post_tweet(tweet_body):
    """X APIでツイートを投稿"""
    try:
        from dotenv import load_dotenv
        import tweepy
    except ImportError:
        log("ERROR: pip install tweepy python-dotenv を実行してください")
        return False
    
    # .env読み込み
    env_path = SCRIPT_DIR / ".env"
    if not env_path.exists():
        log(f"ERROR: .envファイルが見つかりません: {env_path}")
        return False
    
    load_dotenv(env_path)
    
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_SECRET")
    bearer_token = os.getenv("X_BEARER_TOKEN")
    
    if not all([api_key, api_secret, access_token, access_secret]):
        log("ERROR: .envにAPIキーが設定されていません")
        return False
    
    try:
        # v2 API (tweepy v4+)
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        response = client.create_tweet(text=tweet_body)
        tweet_id = response.data['id']
        log(f"投稿成功! Tweet ID: {tweet_id}")
        return True
    except Exception as e:
        log(f"ERROR: 投稿失敗 - {e}")
        return False

def do_tweet():
    """メイン処理: 1回投稿"""
    tweets = load_tweets()
    if not tweets:
        log("ERROR: ツイートが読み込めませんでした")
        return
    
    posted_data = load_posted()
    tweet = pick_tweet(tweets, posted_data)
    
    remaining = len(tweets) - len(posted_data["posted"])
    log(f"選曲: {tweet['title']} (残り{remaining}曲)")
    log(f"本文:\n{tweet['body']}")
    
    # 投稿
    success = post_tweet(tweet["body"])
    
    if success:
        posted_data["posted"].append(tweet["title"])
        posted_data["history"].append({
            "title": tweet["title"],
            "time": datetime.now().isoformat(),
            "cycle": posted_data.get("cycle", 1)
        })
        save_posted(posted_data)
        log(f"記録更新: {len(posted_data['posted'])}/{len(tweets)}曲投稿済み")

def setup_task_scheduler():
    """Windows Task Schedulerに登録（1日3回: 7:00, 12:30, 20:00）"""
    python_path = sys.executable
    script_path = str(Path(__file__).resolve())
    task_name = "WeAreSwifties_TweetBot"
    
    # 既存タスクを削除
    subprocess.run(
        f'schtasks /delete /tn "{task_name}_morning" /f',
        shell=True, capture_output=True
    )
    subprocess.run(
        f'schtasks /delete /tn "{task_name}_lunch" /f',
        shell=True, capture_output=True
    )
    subprocess.run(
        f'schtasks /delete /tn "{task_name}_night" /f',
        shell=True, capture_output=True
    )
    
    times = [
        ("morning", "07:00"),
        ("lunch", "12:30"),
        ("night", "20:00"),
    ]
    
    for suffix, time in times:
        name = f"{task_name}_{suffix}"
        cmd = (
            f'schtasks /create /tn "{name}" /tr '
            f'"\"{python_path}\" \"{script_path}\"" '
            f'/sc daily /st {time} /f'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            log(f"タスク登録成功: {name} ({time})")
        else:
            log(f"タスク登録失敗: {name} - {result.stderr}")

def dry_run():
    """テスト実行（実際には投稿しない）"""
    tweets = load_tweets()
    posted_data = load_posted()
    tweet = pick_tweet(tweets, posted_data)
    
    remaining = len(tweets) - len(posted_data["posted"])
    print(f"\n{'='*50}")
    print(f"🐦 DRY RUN（テスト実行）")
    print(f"{'='*50}")
    print(f"選曲: {tweet['title']}")
    print(f"残り: {remaining}/{len(tweets)}曲")
    print(f"{'='*50}")
    print(tweet["body"])
    print(f"{'='*50}\n")

def show_stats():
    """統計表示"""
    tweets = load_tweets()
    posted_data = load_posted()
    total = len(tweets)
    posted = len(posted_data["posted"])
    remaining = total - posted
    cycle = posted_data.get("cycle", 1)
    
    print(f"\n📊 Tweet Bot 統計")
    print(f"{'='*40}")
    print(f"総曲数:       {total}曲")
    print(f"投稿済み:     {posted}曲")
    print(f"残り:         {remaining}曲")
    print(f"サイクル:     第{cycle}周")
    print(f"残り日数:     約{remaining // 3}日")
    
    if posted_data.get("history"):
        last = posted_data["history"][-1]
        print(f"最終投稿:     {last['time'][:16]} - {last['title']}")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="We are Swifties Tweet Bot")
    parser.add_argument("--setup", action="store_true", help="Windows Task Scheduler登録")
    parser.add_argument("--dry", action="store_true", help="テスト実行（投稿しない）")
    parser.add_argument("--stats", action="store_true", help="統計表示")
    args = parser.parse_args()
    
    if args.setup:
        setup_task_scheduler()
    elif args.dry:
        dry_run()
    elif args.stats:
        show_stats()
    else:
        do_tweet()
