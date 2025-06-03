# agents/company_research_agent.py

from crewai import Agent
from tools.tavily_tool import TavilySearchTool  # ✅ Local import

company_research_agent = Agent(
    role="Company Research Agent",
    goal="Extract products, services, partnerships, and pain points from a company's website.",
    backstory="Specialist in researching companies online using Tavily and summarizing key information.",
    tools=[TavilySearchTool()],
    verbose=True,
    allow_delegation=False
)
