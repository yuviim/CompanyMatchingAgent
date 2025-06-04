import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from crewai import Crew, Task
from agents.company_research_agent import company_research_agent
from agents.service_match_agent import service_match_agent
from utils.web_search import search_company_website
from utils.scrapper import extract_text_from_url
from utils.service_loader import load_services
from dotenv import load_dotenv

def run_pipeline(company_name):
    load_dotenv()

    # Step 1: Find and scrape website
    website = search_company_website(company_name)
    company_data = extract_text_from_url(website)

    # Step 2: Load internal services
    services = load_services()

    # Step 3: Research task – summarize company info
    research_task = Task(
        description=f"""
        Analyze the following content about the company and extract their:
        - Products
        - Services
        - Partnerships
        - Pain points
        
        Company Content:\n{company_data}
        """,
        expected_output="A concise introduction of the company, followed by a bullet list of offerings, partnerships, and key challenges.",
        agent=company_research_agent
    )

    # Step 4: Matching task – suggest what we can offer with detailed justification
    match_task = Task(
        description=f"""
        Based on the research findings and the list of services we offer below,
        recommend relevant services we can provide to this company.

        For each recommended service, please provide:

        1. Current Company’s Issue: Describe the company's pain points or challenges.
        2. Our Potential Solution: Which of our services address that issue.
        3. Justification: Why this solution is a good fit and how it benefits the company.

        Our Services:\n{services}
        """,
        expected_output="""
        A structured match report that clearly outlines for each service:
        - Current Company’s Issue
        - Our Potential Solution
        - Justification for the recommendation
        """,
        agent=service_match_agent,
        context=[research_task]
    )

    # Step 5: Crew setup and execution
    crew = Crew(
        agents=[company_research_agent, service_match_agent],
        tasks=[research_task, match_task],
        verbose=True
    )

    results = crew.kickoff()

    return {
        "company_intro": research_task.output,
        "matching_report": match_task.output,
        "full_summary": results
    }

# CLI usage
if __name__ == "__main__":
    print("🔍 Starting Company Match Agent...\n")
    company = input("🏢 Enter company name: ").strip()

    if not company:
        print("❗ No company name provided. Exiting.")
    else:
        result = run_pipeline(company)
        print("\n📘 Company Introduction:\n")
        print(result["company_intro"])
        print("\n📊 Match Report:\n")
        print(result["matching_report"])
