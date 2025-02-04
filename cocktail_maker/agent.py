"""
cocktail_maker specialist agent
"""
import sys
import os
# Add the base directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from swarm import Agent
from agents.cocktail_maker.functions import make_cocktail_recommendation
from common.functions import case_resolved, escalate_to_human, reset_memory
def create_cocktail_maker_agent(triage_agent):
    """
    Create a cocktail_maker specialist agent
    """
    def transfer_to_triage():
        return triage_agent
    # Ensure function names are valid
    make_cocktail_recommendation.__name__ = "make_cocktail_recommendation"
    case_resolved.__name__ = "case_resolved"
    escalate_to_human.__name__ = "escalate_to_human"
    transfer_to_triage.__name__ = "transfer_to_triage"
    # Create a properly named reset function
    def reset_cocktail_maker():
        return reset_memory('cocktail_maker')
    reset_cocktail_maker.__name__ = "reset_cocktail_maker"
    return Agent(
        name="cocktail_maker Specialist",
        instructions="""You are a cocktail_maker specialist. Your job is to:
        1. Perform the primary function using the make_cocktail_recommendation function
        2. If the user requests, perform additional tasks
        3. If the task is completed, call case_resolved
        4. If assistance is needed, use escalate_to_human
        5. If transferring back to triage, use transfer_to_triage
        IMPORTANT: You can ONLY perform cocktail_maker related tasks. For any other requests,
        transfer the user back to triage using transfer_to_triage.""",
        functions=[
            make_cocktail_recommendation,
            case_resolved,
            escalate_to_human,
            transfer_to_triage,
            reset_cocktail_maker
        ]
    )