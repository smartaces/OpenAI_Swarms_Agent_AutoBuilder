"""
Exchange Rates Finder specialist agent
"""
import sys
import os
# Add the base directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from swarm import Agent
from agents.exchange_rates_finder.functions import get_currency_list, get_conversion_rate, get_historical_rate
from common.functions import case_resolved, escalate_to_human, reset_memory
def create_exchange_rates_finder_agent(triage_agent):
    """
    Create an Exchange Rates Finder specialist agent
    """
    def transfer_to_triage():
        return triage_agent
    # Ensure function names are valid
    get_currency_list.__name__ = "get_currency_list"
    get_conversion_rate.__name__ = "get_conversion_rate"
    get_historical_rate.__name__ = "get_historical_rate"
    case_resolved.__name__ = "case_resolved"
    escalate_to_human.__name__ = "escalate_to_human"
    transfer_to_triage.__name__ = "transfer_to_triage"
    # Create a properly named reset function
    def reset_exchange_rates_finder():
        return reset_memory('exchange_rates_finder')
    reset_exchange_rates_finder.__name__ = "reset_exchange_rates_finder"
    return Agent(
        name="Exchange Rates Finder Specialist",
        instructions="""You are an Exchange Rates Finder specialist. Your job is to:
        1. Retrieve the list of all available currencies using the get_currency_list function.
        2. Get the conversion rate between two currencies using the get_conversion_rate(base_currency, target_currency) function.
        3. Get historical conversion rates using the get_historical_rate(base_currency, target_currency, date) function.
        4. If the user requests, perform additional tasks.
        5. If the task is completed, call case_resolved.
        6. If assistance is needed, use escalate_to_human.
        7. If transferring back to triage, use transfer_to_triage.
        IMPORTANT: You can ONLY perform Exchange Rates Finder related tasks. For any other requests,
        transfer the user back to triage using transfer_to_triage.""",
        functions=[
            get_currency_list,
            get_conversion_rate,
            get_historical_rate,
            case_resolved,
            escalate_to_human,
            transfer_to_triage,
            reset_exchange_rates_finder
        ]
    )