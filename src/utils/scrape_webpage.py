import trafilatura
import urllib.parse

def scrape_webpage(url):
    try:
        # decode DuckDuckGo uddg links if needed
        if "duckduckgo.com/l/?" in url:
            url = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["uddg"][0]
        downloaded = trafilatura.fetch_url(url=url)
        if not downloaded:
            return None
        return trafilatura.extract(downloaded, include_formatting=True, include_links=True)
    except Exception as e:
        print("Scrape error:", e)
        return None