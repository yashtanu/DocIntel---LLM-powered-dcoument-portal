import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY
import sys

class DocumentAnalyzer:
    """
    Analyzes document metadata and content.
    This class is responsible for extracting metadata from documents and analyzing their content.
    """
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.model_loader = ModelLoader()
            self.llm= self.model_loader.load_llm()

            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(
                self.llm, 
                self.parser)
            
            self.prompt = PROMPT_REGISTRY["document_analysis"]
            self.log.info("DocumentAnalyzer initialized successfully")

        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Failed to initialize DocumentAnalyzer", sys) 

  

    def analyze_metadata(self,document_text:str)-> dict:
        """
        Analyzes the metadata of a document.
        This method prepares the prompt and invokes the LLM to analyze the document metadata.
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta data analysis chain iniatited")

            response = chain.invoke({
                "format_instructions":self.parser.get_format_instructions(),
                "document_content":document_text
            })

            self.log.info("metadata extraction suyccesfull",keys=list(response.keys()))
            return response
        except Exception as e:
            self.log.error(f"Error analyzing metadata: {e}")
            raise DocumentPortalException("Failed to analyze metadata", e) from e
        
