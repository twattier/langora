
#Generate query for google search
searches_recommended = """
    As {agent}
    Provide the top 10 most common questions on the topic : {topic}
    Give only the questions, avoid any duplicate, format it as a JSON list.
    """

#Generate query for google search
topics_suggested = """
    As {agent}
    Provide additional common presented topics related to this list of topics : {topics}
    Give only new topics short names, avoid any duplicate. Do not include the list of related topics.
    Format it as a JSON list.
    """

#Summary a piece of text
summary_map = """
    As <agent>
    Use the following set of documents :
        {docs}
    Based on this list of documents, provide a detailed summary of the content.
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
    Use the following set of documents : 
    {context}
    Based only on this list of documents, generate a full detailed and accurate answer for this query : 
    {query}    
    """