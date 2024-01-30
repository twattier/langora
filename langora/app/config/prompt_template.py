
#Generate query for google search
searches_recommended = """
    As {agent}
    Provide the top 10 most common questions on the topic : {topic}
    Give only the questions, avoid any duplicate, format it as a JSON list.
    """

#Summary a piece of text
summary_map = """
    As <agent>
    Use the following set of documents :
        {docs}
    Based on this list of docs, provide a detailed summary of the content.
    Each topic is described precisely with a bullet point list.
    Order them by the importance.
    """

#Final summary
summary_reduce = """
    As <agent>
    Use the following set of topics with their descriptions in bullet point lists :
        {docs}
    Take these and distill it into a final detailed summary.
    Keep the format with each topic described precisely with a bullet point list.
    Order them by the importance.
    """

#RAG
rag = """
    As {agent}
    Based only on this context : 
    {context}
    Generate an answer for this query : {query}
    If you don't know, says that the context is not enought to answer
    """