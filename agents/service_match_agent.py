from crewai import Agent

service_match_agent = Agent(
    role="Service Matching Consultant",
    goal="Match company needs with our services and explain why each one is a fit.",
    backstory="Skilled in mapping business problems to our service offerings.",
    verbose=True,
    allow_delegation=False
)
