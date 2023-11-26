import json
import os

CACHE_FILE = 'llm_cache.json'

def cache_response(query, response):
    """
    Caches the response for a given query.
    :param query: str, the query that was sent to the LLM.
    :param response: str, the response received from the LLM.
    """
    cache = _load_cache()
    cache[query] = response
    _save_cache(cache)

def retrieve_cached_response(query):
    """
    Retrieves a cached response for a given query, if available.
    :param query: str, the query for which to retrieve the cached response.
    :return: str or None, the cached response if available, else None.
    """
    cache = _load_cache()
    return cache.get(query)

def _load_cache():
    """
    Loads the cache from a file.
    :return: dict, the cached data.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

def _save_cache(cache):
    """
    Saves the cache to a file.
    :param cache: dict, the cache data to be saved.
    """
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

# This can be used for testing the functions in this file.
if __name__ == "__main__":
    # Example usage and testing
    test_query = "What is the capital of France?"
    test_response = "The capital of France is Paris."

    print("Caching a response...")
    cache_response(test_query, test_response)

    print("Retrieving cached response...")
    cached_response = retrieve_cached_response(test_query)
    print("Cached Response:", cached_response)
