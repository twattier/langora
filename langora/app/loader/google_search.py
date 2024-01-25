from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

def _top10_results(query):
    return search.results(query, 10)

def google_search(query):    
    tool = Tool(
        name="Google Search Snippets",
        description="Search Google for recent results.",
        func=_top10_results
    )
    return tool.run(query)
