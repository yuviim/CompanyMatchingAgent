import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Clean up scripts and irrelevant tags
        for tag in soup(["script", "style", "noscript", "footer", "header"]):
            tag.decompose()

        # Extract <p> text only
        return ' '.join(p.get_text(strip=True) for p in soup.find_all('p'))
    except Exception as e:
        return f"Error scraping: {e}"
