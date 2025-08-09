import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from logger.custom_logger import CustomLogger
# from langchain_openai import ChatOpenAI
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    def __init__(self):
        load_dotenv()
        self._validate_environment()
        self.config=load_config()
        log.info("Environment variables loaded successfully.",config_keys=list(self.config.keys()))


    def _validate_environment(self):
        """Validate that all required environment variables are set."""
        required_vars = [
            "GOOGLE_API_KEY",
            "GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k, v in self.api_keys.items() if not v]
        if missing:
            log.error(f"Missing environment variables",missing_vars=missing)
            raise DocumentPortalException("Missing environment variables",sys)
        log.info("All required environment variables are set.",api_keys=list(self.api_keys.keys()))
        

    def load_embeddings(self):
        try:
            log.info("Loading Google Generative AI embeddings.")
            model_name=self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Failed to load Google Generative AI embeddings.", error=str(e))
            raise DocumentPortalException("Failed to load Google Generative AI embeddings", sys)
        
        

    def load_llm(self):
        llm_block = self.config["llm"]
        log.info("Loading LLM configuration.")
        
        provider_key = os.getenv("LLM_PROVIDER", "groq")

        if provider_key not in llm_block:
            log.error(f"LLM provider '{provider_key}' not found in configuration.", provider=provider_key)
            raise DocumentPortalException(f"LLM provider '{provider_key}' not found in configuration", sys)

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature",0.2)
        max_tokens = llm_config.get("max_tokens",2048)

        log.info("LLM configuration loaded.", provider=provider, model_name=model_name,temperature=temperature, max_tokens=max_tokens)

        if provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens,
                api_key=self.api_keys["GOOGLE_API_KEY"]
            )
        elif provider == "groq":
            return ChatGroq(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=self.api_keys["GROQ_API_KEY"]
            )
        else:
            log.error(f"Unsupported LLM provider: {provider}", provider=provider)
            raise DocumentPortalException(f"Unsupported LLM provider: {provider}", sys)     


if __name__ == "__main__":
    loader = ModelLoader()

    embeddings = loader.load_embeddings()
    print("Embeddings loaded successfully:", embeddings)

    llm = loader.load_llm()
    print("LLM loaded successfully:", llm)

    result = llm.invoke("Hello, how are you?")
    print("LLM response:", result.content)
        