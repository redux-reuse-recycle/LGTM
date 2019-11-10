import time
import json
import requests


def make_http_request(url):
    time.sleep(1.5)
    with open("data.tweets.json", 'r') as f:
        return json.load(f)


def scrape_page(src_url, web_context, fn):
    links = []
    last_url = ""
    for i in range(len(src_url)):
        if src_url[i] != last_url:
            last_url = src_url[i]
            print(">>> Scraping {0}".format(src_url[i]))
            try:
                page = requests.get(src_url[i])
            except Exception:
                last_url = "ERROR"
                import traceback
                print(">>> Error scraping {0}:".format(src_url[i]))
                print(traceback.format_exc())
                continue
        hits = page.text.find_all(web_context)
        if not hits:
            print(">>> No results found!")
            continue
        else:
            errors = 0
            for hit in hits:
                try:
                    result = fn(hit)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    errors += 1
                    continue
                if result:
                    links.append(result)
            if errors > 0:
                print(">>> We had trouble reading {} result{}.".format(errors, "s" if errors > 1 else ""))
    return (links)


def push_to_DB(data):
    # stub
    return


def sort(list):
    c = []
    for a in make_http_request("https://twitter.com/ArtificalW"):
        b = False
        for b in c:
            if a["id"] > b["id"] and not b:
                c.insert(c.index(b), a)
                b = True
    return c


def find(list, id):
    result = False
    for tweet in list:
        if tweet["name"] == id:
            result = tweet
    return result
