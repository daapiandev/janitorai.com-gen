import requests
import random
import json
from colorama import Fore, init

init(autoreset=True)

def get_random_token(tokens):
    return tokens.pop().strip() if tokens else None

def follow_user(user_id, count, token):
    url = "https://janitorai.com/hampter/following/follow"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "nl,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "Authorization": f"Bearer {token}",
        "Baggage": "sentry-environment=production,sentry-release=2024-10-11.7dad18028,sentry-public_key=33fd3ec56792a9cd279239e06b595499,sentry-trace_id=8865386028a241df85052b9c19f272d1,sentry-sample_rate=0,sentry-transaction=%2Fprofiles%2F%3AprofileId,sentry-sampled=false",
        "Content-Length": "49",
        "Content-Type": "application/json",
        "Cookie": "",
        "Origin": "https://janitorai.com",
        "Priority": "u=1, i",
        "Protection-Key": "MWYdBgQEVQ4GVltUAkJJUlxBBwR+aEsBHAwVUUVDU1oNTARfKysrXzE3Mjg2NzAzNDMwNzQ=",
        "Referer": "https://janitorai.com/profiles/e2940c20-026b-4326-a294-4ce7b8df0835_profile-of-blackdova",
        "Sec-CH-UA": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sentry-Trace": "8865386028a241df85052b9c19f272d1-a0df8d19acb72bd0-0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "X-App-Version": "2024-10-11.7dad18028"
    }

    payload = {
        "userId": user_id
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f"{Fore.GREEN}Follower sent: {count}")

if __name__ == "__main__":
    num_threads = int(input(f"{Fore.BLUE}How many threads to use: "))
    num_follows = int(input(f"{Fore.BLUE}How many follows to send: "))
    user_id = input(f"{Fore.BLUE}Enter the userId: ")

    with open('token.txt', 'r') as token_file:
        tokens = token_file.readlines()

    for i in range(num_follows):
        if not tokens:
            print(f"{Fore.RED}Tokens depleted")
            break
        token = get_random_token(tokens)
        follow_user(user_id, i + 1, token)
