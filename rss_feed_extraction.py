import requests
import feedparser
import pandas as pd
from datetime import datetime
  
# bbc time formate is not standard , so we have to transform it.
def normalize_date(entry): # entry is one item in xml file , it is in form of dictioanry
    if entry.get("published_parsed"): #Returns the value if the key exists, otherwise None . if return none then this block of code skip.
        return (datetime(*entry["published_parsed"][:6]))# datetime(2026, 1, 12, 19, 38, 53) = 2026-01-12 19:38:53 but it is datetime object
    return ""

# extract the categories fron the rss_link 
def extract_category_from_url(url):
    """ 
    we have to extract categroy of news from the provided input link.
    """
    # firstly remove protocol (http:// or https://) from url and also url is string
    if "://" in url:
        url = url.split("://", 1)[1] # split("based_on-this",number of times we have to split) retrun list then we take value at first index

    # Split path , it gives us list of strings
    parts = url.split("/") #split based on "/" return list

    # in bbc link category is at index 2 
    if len(parts)>=4 and parts[1]=="news":
        return parts[2]
    
    return "general"


#download RSS feed from a URL and converts it into a Python object.
def fetch_feed(url):
    headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0")}
    try:
        response = requests.get(url, headers=headers, timeout=20)# send http get request. 
        #responce contains status code, header, content(raw xml data)
        if response.status_code >= 400:# it handle server error
            print(f"http error {response.status_code} for {url}")
            return None, None # check status code if good responce the continue otherwise stop and raise error ,it prevent to parse bad responce.
        feed = feedparser.parse(response.content)
        return url, feed

    except Exception as e: # it handle pragamatical error like network conection , timeout , bad url formate etc 
        print(f"Error fetching {url}: {e}")
        return None, None


# fetch all feeds one by one remove duplicate articles link inside xml file also remove the dupplicate link providede by user.
def fetch_all_feeds(rss_urls):
    rss_urls = list(set(rss_urls)) # remove duplicate links which is provided by user
    all_data = []
    seen_links = set() # set using hashing so it lookup time complexity is O(1) , where as in list have sequantial processing then it is o(n)

    for url in rss_urls:
        feed_url, feed = fetch_feed(url)

        if feed is None or len(feed.entries) == 0: # feed.entries is a list of news 
            continue

        category = extract_category_from_url(feed_url)

        for entry in feed.entries: # entry is one news item and it is in dictionary formate
            link = entry.get("link", "")
            if link in seen_links:
                continue #skip that entry move to next

            seen_links.add(link)

            all_data.append({
                "Title": entry.get("title", ""),
                "Description": entry.get("summary", ""),
                "Category": category,
                "Published Time": normalize_date(entry),
                "Link": link
            })

    return all_data

# main function
def extract_rss_to_excel(rss_urls, output_file="rss_output.xlsx"):
    data = fetch_all_feeds(rss_urls)
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

    print(f"length of df:{len(df)}")
    print(f"output excel file:{output_file}")


if __name__=="__main__":
    rss_feed_links = ["https://feeds.bbci.co.uk/news/technology/rss.xml"]
    extract_rss_to_excel(rss_feed_links, "news_data.xlsx")
