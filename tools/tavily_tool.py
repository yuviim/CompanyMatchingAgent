from crewai.tools.base_tool import BaseTool
from tavily import TavilyClient
import os

class TavilySearchTool(BaseTool):
    name: str = "Tavily Web Search Tool"
    description: str = "Searches the web using Tavily"

    def _run(self, query: str) -> str:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query, search_depth="advanced", max_results=5)
        return "\n".join(r["url"] for r in results["results"])
