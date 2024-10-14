import requests
import random
import string
import time
import json
from colorama import Fore, Style, init
import threading
import ctypes

init(autoreset=True)


created_accounts = 0

lock = threading.Lock()

def generate_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_password(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def generate_email():
    return f"{generate_string(10)}@rteet.com"

def load_proxies():
    proxies = []
    try:
        with open("proxies.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    proxies.append(line)
    except FileNotFoundError:
        print(f"{Fore.RED}[X] proxies.txt not found.")
    return proxies

def get_random_proxy(proxies):
    proxy = random.choice(proxies)
    if proxy.count(':') == 1:
        return {
            "http": f"http://{proxy}",
            "http": f"http://{proxy}"
        }
    elif proxy.count(':') == 3:
        ip, port, username, password = proxy.split(':')
        return {
            "http": f"http://{username}:{password}@{ip}:{port}",
            "http": f"http://{username}:{password}@{ip}:{port}"
        }
    else:
        return None

def get_otp(email_user, email_domain, proxies=None):
    otp_code = None
    while not otp_code:
        time.sleep(5)
        try:
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_user}&domain={email_domain}"
            proxy = get_random_proxy(proxies) if proxies else None
            response = requests.get(url, proxies=proxy)
            messages = response.json()

            if messages:
                message_id = messages[0]['id']
                message_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_user}&domain={email_domain}&id={message_id}"
                message_response = requests.get(message_url, proxies=proxy)
                message_data = message_response.json()


                html_body = message_data['htmlBody']
                start_marker = '<div class="token">'
                end_marker = '</div>'

                start_index = html_body.find(start_marker)
                if start_index != -1:
                    start_index += len(start_marker)
                    end_index = html_body.find(end_marker, start_index)
                    if end_index != -1:
                        otp_code = html_body[start_index:end_index].strip()

                if otp_code and otp_code.isdigit() and len(otp_code) == 6:
                    return otp_code
                else:
                    otp_code = None

            print(f"{Fore.RED}[!] No OTP found, rechecking after 5 seconds")

        except Exception as e:
            print(f"{Fore.RED}[!] Error while checking OTP: {e}")

def signup_and_verify(proxies=None):
    global created_accounts

    email = generate_email()
    password = generate_password(8)
    email_user, email_domain = email.split('@')


    signup_url = "https://auth.janitorai.com/auth/v1/signup"
    signup_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jbXp4dHpvbW1wbnhreW5kZGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNzA3NDAsImV4cCI6MjA0Mzk0Njc0MH0.UfRPni4ga9Lmin8j0JjV5ouuK9bXp8tsqPJ8pMTDDAI",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jbXp4dHpvbW1wbnhreW5kZGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgzNzA3NDAsImV4cCI6MjA0Mzk0Njc0MH0.UfRPni4ga9Lmin8j0JjV5ouuK9bXp8tsqPJ8pMTDDAI",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "auth.janitorai.com",
        "Origin": "https://janitorai.com",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Client-Info": "supabase-ssr/0.5.1",
        "X-Supabase-Api-Version": "2024-01-01"
    }
    signup_payload = {
        "email": email,
        "password": password,
        "data": {},
        "gotrue_meta_security": {
            "captcha_token": ""
        },
        "code_challenge": "cCG4PIXOgT2fUPImrTIdTHtagbHa8k323S85aFlGasg",
        "code_challenge_method": "s256"
    }

    proxy = get_random_proxy(proxies) if proxies else None
    signup_response = requests.post(signup_url, headers=signup_headers, data=json.dumps(signup_payload), proxies=proxy)

    if signup_response.status_code == 200:
        print(f"{Fore.GREEN}[+] solved account: {Fore.LIGHTMAGENTA_EX}{email}:{password}")
        with open('accounts.txt', 'a') as acc_file:
            acc_file.write(f"{email}:{password}\n")
    else:
        print("Signup failed")
        print(signup_response.text)
        return


    otp_code = get_otp(email_user, email_domain, proxies)
    print(f"{Fore.YELLOW}[!] Received otp: {Fore.LIGHTMAGENTA_EX}{otp_code}")


    verify_url = "https://auth.janitorai.com/auth/v1/verify"
    verify_headers = signup_headers.copy()
    verify_payload = {
        "type": "email",
        "email": email,
        "token": otp_code,
        "options": {
            "captchaToken": ""
        },
        "gotrue_meta_security": {
            "captcha_token": ""
        }
    }

    verify_response = requests.post(verify_url, headers=verify_headers, data=json.dumps(verify_payload), proxies=proxy)

    if verify_response.status_code == 200:
        print(f"{Fore.GREEN}[*] verified {Fore.LIGHTMAGENTA_EX}{email}:{password}")

      
        response_data = verify_response.json()
        access_token = response_data.get('access_token')
        with open('token.txt', 'a') as token_file:
            token_file.write(f"{access_token}\n")

        with lock:
            created_accounts += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Made by Daap <3 Created accounts: {created_accounts}")
    else:
        print("Verification failed")
        print(verify_response.text)

if __name__ == "__main__":
    num_accounts = int(input(f"{Fore.BLUE}How many accounts to generate: "))
    num_threads = int(input(f"{Fore.BLUE}How many threads to use: "))

    use_proxies = input(f"{Fore.BLUE}Use proxies? (y/n): ").lower().strip() == 'y'
    proxies = load_proxies() if use_proxies else None

    threads = []
    for _ in range(num_accounts):
        t = threading.Thread(target=signup_and_verify, args=(proxies,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
