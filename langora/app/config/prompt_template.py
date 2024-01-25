
#Generate query for google search
knowledge_recommendations = """
    As {agent}
    Provide the top 10 most common questions on the topics : {topics}
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