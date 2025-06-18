import requests
import concurrent.futures
from googlesearch import search
from bs4 import BeautifulSoup
import time
import sys
import os
import json

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] Install colorama for colored output: pip install colorama")

def banner():
    print(Fore.CYAN + """
========================================
             BLACK PT TOOL
         Public Profile Finder
========================================
""" + Fore.GREEN + "Credit: Black Panther | IG: @blackpanther2x\n")

def check_follow():
    print(Fore.YELLOW + "Follow my Instagram first to use this tool!")
    print(Fore.GREEN + "Instagram: https://instagram.com/blackpanther2x\n")
    confirm = input(Fore.CYAN + "Type 'followed' after following to continue: ").strip().lower()
    if confirm == "followed":
        print(Fore.YELLOW + "[+] Opening Instagram profile in your phone browser...")
        os.system("termux-open-url https://instagram.com/blackpanther2x")
        time.sleep(2)
    else:
        print(Fore.RED + "[!] You must follow the Instagram and type 'followed' to proceed. Exiting...")
        sys.exit(0)

def loading_animation(text="Loading"):
    for _ in range(3):
        sys.stdout.write("\r" + Fore.YELLOW + text + ".")
        sys.stdout.flush()
        time.sleep(0.4)
        sys.stdout.write("\r" + Fore.YELLOW + text + "..")
        sys.stdout.flush()
        time.sleep(0.4)
        sys.stdout.write("\r" + Fore.YELLOW + text + "...")
        sys.stdout.flush()
        time.sleep(0.4)
        sys.stdout.write("\r" + Fore.YELLOW + text + "   ")
        sys.stdout.flush()

def save_results_json(username, profiles):
    with open(f"{username}_profiles.json", "w") as f:
        json.dump({"username": username, "profiles": profiles}, f, indent=4)
    print(Fore.GREEN + f"[+] Results saved to {username}_profiles.json")

def public_profile_search(username):
    print(Fore.CYAN + f"[+] Searching for public profiles of: {username}")

    sites = [
        "https://github.com/{}",
        "https://twitter.com/{}",
        "https://instagram.com/{}",
        "https://facebook.com/{}",
        "https://www.youtube.com/@{}",
        "https://www.pinterest.com/{}",
        "https://www.reddit.com/user/{}",
        "https://www.tumblr.com/{}",
        "https://medium.com/@{}",
        "https://www.deviantart.com/{}",
        "https://www.tiktok.com/@{}",
        "https://www.snapchat.com/add/{}",
        "https://www.quora.com/profile/{}",
        "https://www.soundcloud.com/{}",
        "https://www.behance.net/{}",
        "https://www.dribbble.com/{}"
    ]

    found_profiles = []

    def check_site(site):
        url = site.format(username)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] Found: {url}")
                found_profiles.append(url)
            elif response.status_code == 404:
                print(Fore.RED + f"[-] Not Found: {url}")
            else:
                print(Fore.YELLOW + f"[?] Unknown Response ({response.status_code}): {url}")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] Error accessing {url} - {e}")

    loading_animation("[+] Checking Profiles")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_site, sites)

    if found_profiles:
        with open(f"{username}_profiles.txt", "w") as f:
            for profile in found_profiles:
                f.write(profile + "\n")
        print(Fore.GREEN + f"\n[+] Results saved to {username}_profiles.txt")
        save_results_json(username, found_profiles)

    print("\n" + Fore.CYAN + "[+] Performing Google Search...")
    loading_animation("[+] Google Searching")

    query = f"{username} site:linkedin.com OR site:facebook.com OR site:instagram.com OR site:twitter.com"
    google_results = []

    try:
        for result in search(query, num_results=10):
            print(Fore.MAGENTA + f"[Google] {result}")
            google_results.append(result)
    except Exception as e:
        print(Fore.RED + f"[!] Google Search Error: {e}")

    print("\n" + Fore.CYAN + "[+] Attempting to scrape basic profile details:")
    for url in google_results[:5]:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "No Title"
            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and "content" in meta_tag.attrs:
                meta_desc = meta_tag["content"]
            print(Fore.BLUE + f"URL: {url}")
            print(Fore.YELLOW + f"Title: {title}")
            print(Fore.LIGHTBLACK_EX + f"Description: {meta_desc}\n")
        except Exception as e:
            print(Fore.RED + f"[!] Error scraping {url} - {e}")

if __name__ == "__main__":
    banner()
    check_follow()
    username = ""
    while not username.strip():
        username = input(Fore.GREEN + "Enter username or email to search across platforms: ").strip()
        if not username:
            print(Fore.RED + "[!] Please enter a valid username or email.")
    public_profile_search(username)