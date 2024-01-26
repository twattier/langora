import json

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.prompts.prompt import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.llm import LLMChain

from config.env import Config
from config import prompt_template as template
from utils.functions import list_to_string
from db.dbvector import DbVector

class ServiceModel():

    def __init__(self, db:DbVector) -> None:        
        self.db = db
        self.model = None

    def init_model(self):
        if Config.USE_OPENAI:            
            from llm.model_openai import ModelOpenAI
            self.model = ModelOpenAI()
        else:
            from llm.model_local import ModelLocal
            self.model = ModelLocal()            
        self.model.init_model()

    # ---------------------------------------------------------------------------
    # Prompt
    # ---------------------------------------------------------------------------
        
    def submit_prompt(self, prompt:str):
        return self.model.llm(prompt)

    def get_topic_searches_recommended(self, topic_name:str):        
        prompt = PromptTemplate.from_template(template.searches_recommended)
        knowledge = self.db.select_knowledge()        
        result = self.submit_prompt(prompt.format(agent=knowledge.agent, topic=topic_name))
        try:
            list = json.loads(result)
        except:
            print("LLM Error : incorrect generated JSON")
            return []
        return list

    # ---------------------------------------------------------------------------
    # Summarize
    # ---------------------------------------------------------------------------

    def summarize(self, doc):

        # Map        
        map_prompt = PromptTemplate.from_template(template.summary_map.replace('<agent>', self.model.agent))
        map_chain = LLMChain(llm=self.model.llm, prompt=map_prompt)

        # Reduce
        reduce_prompt = PromptTemplate.from_template(template.summary_reduce.replace('<agent>', self.model.agent))
        reduce_chain = LLMChain(llm=self.model.llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=3800,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents([doc])

        return map_reduce_chain.run(split_docs)
