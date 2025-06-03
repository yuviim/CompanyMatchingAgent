from tavily import TavilyClient
import os

def search_company_website(company_name):
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(
        query=company_name + " official site",
        search_depth="advanced",
        max_results=5
    )
    for r in results['results']:
        if "https://" in r['url']:
            return r['url']
    return None
