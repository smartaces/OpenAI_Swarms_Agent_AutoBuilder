"""
Knock knock jokes specialist agent
"""
import sys
import os

# Add the parent directory to the Python path
sys.path.append('/content/swarm/examples/magic')

from swarm import Agent
from agents.knock_knock.functions import tell_knock_joke
from common.functions import case_resolved, escalate_to_human, reset_memory

def create_knock_knock_agent(triage_agent):
    """
    Create a knock knock jokes specialist agent
    """
    def transfer_to_triage():
        return triage_agent

    # Ensure function names are valid
    tell_knock_joke.__name__ = "tell_knock_knock_joke"
    case_resolved.__name__ = "case_resolved"
    escalate_to_human.__name__ = "escalate_to_human"
    transfer_to_triage.__name__ = "transfer_to_triage"

    # Create a properly named reset function
    def reset_knock_knock():
        return reset_memory('knock_knock')
    reset_knock_knock.__name__ = "reset_knock_knock"

    return Agent(
        name="Knock Knock Jokes Specialist",
        instructions="""You are a knock knock joke specialist. Your job is to:
        1. Get a new knock knock joke using tell_knock_knock_joke
        2. Present the setup ("Knock knock!")
        3. Wait for the user to say "who's there?"
        4. Present the "who" part and wait for the user's response
        5. Deliver the punchline
        6. If they want another joke, tell another one
        7. If they want a different type of joke, use transfer_to_triage
        8. If they're done, call case_resolved

        IMPORTANT: You can ONLY tell knock knock jokes. For any other requests,
        transfer the user back to triage using transfer_to_triage.""",
        functions=[
            tell_knock_joke,
            case_resolved,
            escalate_to_human,
            transfer_to_triage,
            reset_knock_knock
        ]
    )
