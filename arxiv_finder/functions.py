"""
Functions for the arxiv_finder agent
"""
import sys
import os
import requests
import time
import xml.etree.ElementTree as ET
# Add the parent directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from base.memory_manager import memory_manager
from agents.arxiv_finder.content import ARXIV_API_BASE_URL
def search_arxiv_papers(search_query, start=0, max_results=5, sortBy='relevance', sortOrder='descending'):
    """
    Searches the arXiv API for papers matching the search query.
    Args:
        search_query (str): The search query.
        start (int): The index of the first result.
        max_results (int): The maximum number of results to return.
        sortBy (str): The criterion to sort results ('relevance', 'lastUpdatedDate', 'submittedDate').
        sortOrder (str): The order of sorting ('ascending' or 'descending').
    Returns:
        list: A list of dictionaries containing paper details, or an error message.
    """
    try:
        params = {
            'search_query': search_query,
            'start': str(start),
            'max_results': str(max_results),
            'sortBy': sortBy,
            'sortOrder': sortOrder
        }
        response = requests.get(ARXIV_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        # Respect arXiv's rate limit
        time.sleep(3)
        # Parse the Atom XML response
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        root = ET.fromstring(response.content)
        papers = []
        for entry in root.findall('atom:entry', ns):
            paper = {}
            paper['id'] = entry.find('atom:id', ns).text
            paper['title'] = entry.find('atom:title', ns).text.strip()
            paper['summary'] = entry.find('atom:summary', ns).text.strip()
            paper['authors'] = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
            paper['published'] = entry.find('atom:published', ns).text
            paper['updated'] = entry.find('atom:updated', ns).text
            pdf_link = entry.find("atom:link[@title='pdf']", ns)
            paper['pdf_link'] = pdf_link.attrib['href'] if pdf_link is not None else None
            papers.append(paper)
        if not papers:
            return {"error": "No papers found for the query."}
        return papers
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
def get_paper_details(arxiv_id):
    """
    Retrieves the details of a paper given its arXiv ID.
    Args:
        arxiv_id (str): The arXiv ID of the paper.
    Returns:
        dict: A dictionary containing paper details, or an error message.
    """
    try:
        params = {
            'id_list': arxiv_id
        }
        response = requests.get(ARXIV_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        # Respect arXiv's rate limit
        time.sleep(3)
        # Parse the Atom XML response
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        root = ET.fromstring(response.content)
        entry = root.find('atom:entry', ns)
        if entry is None:
            return {"error": "Paper not found."}
        paper = {}
        paper['id'] = entry.find('atom:id', ns).text
        paper['title'] = entry.find('atom:title', ns).text.strip()
        paper['summary'] = entry.find('atom:summary', ns).text.strip()
        paper['authors'] = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        paper['published'] = entry.find('atom:published', ns).text
        paper['updated'] = entry.find('atom:updated', ns).text
        pdf_link = entry.find("atom:link[@title='pdf']", ns)
        paper['pdf_link'] = pdf_link.attrib['href'] if pdf_link is not None else None
        return paper
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}