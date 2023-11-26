def format_query(query, context='', additional_params=None):
    """
    Prepares and formats a query for sending to the LLM API.
    :param query: str, the primary query or prompt for the LLM.
    :param context: str, any additional context or information to be included.
    :param additional_params: dict, any additional parameters to customize the query.
    :return: str, the formatted query.
    """
    formatted_query = f"{context}\n{query}" if context else query
    if additional_params:
        # Further formatting can be done here based on additional params.
        pass
    return formatted_query

# This can be used for testing the functions in this file.
if __name__ == "__main__":
    # Example usage and testing
    basic_query = "What is the capital of France?"
    formatted_query = format_query(basic_query)
    print("Formatted Query:", formatted_query)

    context_query = "Given the following context: Paris is a city in France. What is the capital of France?"
    context = "Context: Paris is a major city in Europe."
    formatted_query_with_context = format_query(context_query, context)
    print("Formatted Query with Context:", formatted_query_with_context)
