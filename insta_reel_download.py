import json
import os
import time
from playwright.sync_api import sync_playwright

import crediantials
COOKIE_FILE = "instagram_cookies.json"
def save_cookies(context):
    """Save browser cookies to a JSON file."""
    cookies = context.cookies()
    with open(COOKIE_FILE, "w", encoding="utf-8") as file:
        json.dump(cookies, file, indent=4)

def is_logged_in(page):
    """Check if user is logged in by visiting Instagram homepage."""
    page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
    time.sleep(3)

    # If login is required, return False
    if "login" in page.url or "challenge" in page.url:
        print("Cookies expired. Login required.")
        return False

    print("Session is active.")
    return True

def refresh_cookies(context, page):
    """Visit Instagram homepage to refresh session validity."""
    page.goto("https://www.instagram.com/", timeout=60000)
    time.sleep(5)  # Wait for page to load
    save_cookies(context)  # Save updated cookies
    print("Cookies refreshed to extend session.")

def load_cookies(context):
    """Load cookies from a JSON file if it exists."""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as file:
            cookies = json.load(file)
        context.add_cookies(cookies)


def login(username: str, password: str,page,context):

        page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
        time.sleep(4)  # Allow time for the page to load

        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.press("input[name='password']", "Enter")

        time.sleep(5.5)  # Allow time for login process
        page.goto("https://www.instagram.com/")
        time.sleep(5)
        save_cookies(context)
        print("Logged in successfully.")



def login_with_browser(username: str, password: str):
    with sync_playwright() as p:  # Ensure Playwright starts here
        # browser = p.chromium.launch(headless=False)  # Change to True if needed
        browser = p.chromium.launch(headless=True)  # Change to True if needed
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
        time.sleep(4)  # Allow time for the page to load

        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.press("input[name='password']", "Enter")

        time.sleep(5.5)
        page.screenshot(path=crediantials.screenshot_path)
        is_logged_in(page)
        browser.close()





def get_instagram_links(username: str, password: str, target_username: str,max_scrolls, max_attempts_without_new_links: int = 3):
    with sync_playwright() as p:  # Ensure Playwright starts here
        # browser = p.chromium.launch(headless=False)  # Change to True if needed
        browser = p.chromium.launch(headless=True)  # Change to True if needed
        context = browser.new_context()
        page = context.new_page()
        load_cookies(context)
        page = context.new_page()
        if not is_logged_in(page):
            login(username, password, page, context)

        refresh_cookies(context, page)


        instagram_url = f"https://www.instagram.com/{target_username}/reels/"
        time.sleep(5)
        page.goto(instagram_url, timeout=60000)
        time.sleep(5)  # Allow time for page to load

        links = set()
        attempts_without_new_links = 0
        while attempts_without_new_links < max_attempts_without_new_links:
            previous_count = len(links)
            hrefs = page.eval_on_selector_all("a[href]", "elements => elements.map(e => e.href)")
            for link in hrefs:
                if "/reel/" in link or "/p/" in link:
                    links.add(link)

            if max_scrolls is None:
                if len(links) == previous_count:
                    attempts_without_new_links += 1
                else:
                    attempts_without_new_links = 0
            else:
                max_attempts_without_new_links = max_scrolls
                attempts_without_new_links += 1


            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)  # Allow time for new content to load

        browser.close()
    return list(links)

def save_links_to_json(links, filename="instagram_links.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(links, file, indent=4)


if __name__ == "__main__":
    username = crediantials.USER  # Change this to your Instagram username
    password = crediantials.PWD  # Change this to your Instagram password
    login_with_browser(username,password)
    target_username = "tamannaahspeaks"  # Change this to the target username
    post_links = get_instagram_links(username, password, target_username, 3)
    save_links_to_json(post_links)
    print(f"Extracted {len(post_links)} links saved to instagram_links.json")
