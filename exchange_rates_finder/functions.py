"""
Functions for the Exchange Rates Finder agent
"""
import sys
import os
import requests
# Add the parent directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from base.memory_manager import memory_manager
from agents.exchange_rates_finder.content import API_BASE_URL, FALLBACK_API_BASE_URL
def get_currency_list():
    """
    Retrieves the list of all available currencies.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/currencies.json")
        response.raise_for_status()
        currencies = response.json()
    except requests.RequestException:
        try:
            response = requests.get(f"{FALLBACK_API_BASE_URL}/currencies.json")
            response.raise_for_status()
            currencies = response.json()
        except requests.RequestException:
            return {"error": "Failed to retrieve currencies list from both primary and fallback APIs."}
    return currencies
def get_conversion_rate(base_currency, target_currency):
    """
    Retrieves the conversion rate between two currencies.
    """
    base_currency = base_currency.lower()
    target_currency = target_currency.lower()
    try:
        response = requests.get(f"{API_BASE_URL}/currencies/{base_currency}.json")
        response.raise_for_status()
        rates = response.json()
    except requests.RequestException:
        try:
            response = requests.get(f"{FALLBACK_API_BASE_URL}/currencies/{base_currency}.json")
            response.raise_for_status()
            rates = response.json()
        except requests.RequestException:
            return {"error": f"Failed to retrieve conversion rate for {base_currency.upper()} from both primary and fallback APIs."}
    rate = rates.get(base_currency, {}).get(target_currency)
    if rate:
        return rate
    else:
        return {"error": f"Conversion rate from {base_currency.upper()} to {target_currency.upper()} not found."}
def get_historical_rate(base_currency, target_currency, date):
    """
    Retrieves historical conversion rate between two currencies on a specific date.
    """
    base_currency = base_currency.lower()
    target_currency = target_currency.lower()
    try:
        response = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/{base_currency}.json")
        response.raise_for_status()
        rates = response.json()
    except requests.RequestException:
        try:
            response = requests.get(f"https://{date}.currency-api.pages.dev/v1/currencies/{base_currency}.json")
            response.raise_for_status()
            rates = response.json()
        except requests.RequestException:
            return {"error": f"Failed to retrieve historical conversion rate for {base_currency.upper()} on {date} from both primary and fallback APIs."}
    rate = rates.get(base_currency, {}).get(target_currency)
    if rate:
        return rate
    else:
        return {"error": f"Conversion rate from {base_currency.upper()} to {target_currency.upper()} on {date} not found."}