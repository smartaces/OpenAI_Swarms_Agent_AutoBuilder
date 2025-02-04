"""
arxiv_finder specialist agent
"""
import sys
import os
# Add the base directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from swarm import Agent
from agents.arxiv_finder.functions import search_arxiv_papers, get_paper_details
from common.functions import case_resolved, escalate_to_human, reset_memory
def create_arxiv_finder_agent(triage_agent):
    """
    Create an arxiv_finder specialist agent
    """
    def transfer_to_triage():
        return triage_agent
    # Ensure function names are valid
    search_arxiv_papers.__name__ = "search_arxiv_papers"
    get_paper_details.__name__ = "get_paper_details"
    case_resolved.__name__ = "case_resolved"
    escalate_to_human.__name__ = "escalate_to_human"
    transfer_to_triage.__name__ = "transfer_to_triage"
    # Create a properly named reset function
    def reset_arxiv_finder():
        return reset_memory('arxiv_finder')
    reset_arxiv_finder.__name__ = "reset_arxiv_finder"
    return Agent(
        name="ArXiv Finder Specialist",
        instructions="""You are an ArXiv Finder specialist. Your job is to:
        1. Help the user search for research papers using the search_arxiv_papers(search_query, start=0, max_results=5, sortBy='relevance', sortOrder='descending') function.
        2. Provide details of a specific paper using the get_paper_details(arxiv_id) function.
        3. If the user requests, perform additional tasks within your domain.
        4. If the task is completed, call case_resolved.
        5. If assistance is needed, use escalate_to_human.
        6. If transferring back to triage, use transfer_to_triage.
        IMPORTANT: You can ONLY perform ArXiv Finder related tasks. For any other requests,
        transfer the user back to triage using transfer_to_triage.""",
        functions=[
            search_arxiv_papers,
            get_paper_details,
            case_resolved,
            escalate_to_human,
            transfer_to_triage,
            reset_arxiv_finder
        ]
    )