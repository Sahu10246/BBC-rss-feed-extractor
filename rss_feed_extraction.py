import requests
import feedparser
import pandas as pd
from datetime import datetime
  
def normalize_date(entry):
    """
    Normalize datetime information from an XML entry.

    Args:
        entry (dict): A single XML entry containing date information.

    Returns:
        str: Formatted datetime string in "YYYY-MM-DD HH:MM:SS" format,
        or an empty string if date information is missing.
    """
    published = entry.get("published_parsed")
    if not published:
        return ""

    date_time = datetime(*published[:6])
    return date_time.strftime("%Y-%m-%d %H:%M:%S")
 

def extract_category_from_url(url):
    """ 
    we have to extract categroy of news from the provided input link.
    """
    # firstly remove protocol (http:// or https://) from url and also url is string
    if "://" in url:
        url = url.split("://", 1)[1] 

    # Split path, it gives us list of strings
    parts = url.split("/") 

    # In bbc link, category is at index 2 
    if len(parts)>=4 and parts[1]=="news":
        return parts[2]
    
    return "general"


def fetch_feed(url):
    """
    Download an RSS feed from a URL and parse it into a Python object.

    Args:
        url (str): URL of the RSS feed.

    Returns:
        tuple[str | None, feedparser.FeedParserDict | None]:
        The feed URL and parsed feed object if successful,
        otherwise (None, None).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)

        # Handle HTTP error responses
        if response.status_code >= 400:
            print(f"HTTP error {response.status_code} for {url}")
            return None, None

        feed = feedparser.parse(response.content)
        return url, feed

    except requests.exceptions.RequestException as error:
        # Handle network-related errors (timeout, connection, bad URL)
        print(f"Error fetching {url}: {error}")
        return None, None


def fetch_all_feeds(rss_urls):
    """
    Fetch and process RSS feeds from multiple URLs.

    This function removes duplicate feed URLs provided by the user,
    fetches each feed, and removes duplicate article links across
    all feeds.

    Args:
        rss_urls (list[str]): List of RSS feed URLs.

    Returns:
        list[dict]: A list of processed news articles with metadata.
    """
    # Remove duplicate RSS URLs provided by the user
    rss_urls = list(set(rss_urls))

    all_data = []
    seen_links = set()  # Track unique article links for deduplication

    for url in rss_urls:
        feed_url, feed = fetch_feed(url)

        # Skip invalid or empty feeds
        if feed is None or not feed.entries:
            continue

        category = extract_category_from_url(feed_url)

        for entry in feed.entries:
            link = entry.get("link", "")

            # Skip duplicate articles
            if link in seen_links:
                continue

            seen_links.add(link)

            all_data.append(
                {
                    "Title": entry.get("title", ""),
                    "Description": entry.get("summary", ""),
                    "Category": category,
                    "Published Time": normalize_date(entry),
                    "Link": link,
                }
            )

    return all_data


def extract_rss_to_excel(rss_urls, output_file="rss_output.xlsx"):
    """
    Extract RSS feed data and save it to an Excel file.

    Args:
        rss_urls (list[str]): List of RSS feed URLs.
        output_file (str): Path to the output Excel file.

    Returns:
        dataframe
    """
    data = fetch_all_feeds(rss_urls)
    dataframe = pd.DataFrame(data)

    dataframe.to_excel(output_file, index=False)

    print(f"Length of DataFrame: {len(dataframe)}")
    print(f"Output Excel file: {output_file}")


if __name__ == "__main__":
    rss_feed_links = [
        "https://feeds.bbci.co.uk/news/technology/rss.xml"
    ]
    extract_rss_to_excel(rss_feed_links, "news_data.xlsx")



