import requests
from bs4 import BeautifulSoup

def load_services():
    my_company_url = "https://maveric-systems.com/" 
    try:
        response = requests.get(my_company_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"⚠️ Error loading company site: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "noscript", "svg", "img", "footer", "header"]):
        tag.decompose()

    # Extract raw text
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Optional: Filter only lines mentioning services/solutions
    keywords = ["service", "solution", "offering", "capability", "consulting"]
    filtered = [
        line for line in lines
        if any(k.lower() in line.lower() for k in keywords)
    ]

    return "\n".join(filtered or lines[:40])  # Return filtered or fallback to first 40 lines
