import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    @staticmethod
    def _norm(value: str | None) -> str | None:
        if value is None:
            return ""
        return value.strip().strip('"').strip("'")
    
    LLM_KEY: str = _norm(os.getenv("OPENAI_API_KEY"))
    LLM_BASE_URL: str = _norm(os.getenv("LLM_BASE_URL"))
    EMBEDDING_KEY: str = _norm(os.getenv("OPENAI_API_KEY"))
    EMBEDDING_MODEL: str = _norm(os.getenv("EMBEDDING_MODEL"))
    LLM_TEMPERATURE: float = float(_norm(os.getenv("LLM_TEMPERATURE")))
    LLM_MODEL: str = _norm(os.getenv("LLM_MODEL"))

    @property
    def api_key(self) -> str:
        return self.LLM_KEY
    
    @property
    def base_url(self) -> str:
        if self.LLM_BASE_URL:
            return self.LLM_BASE_URL
        
        model_lower = self.LLM_MODEL.lower()
        if "deepseek" in model_lower:
            return "https://mkp-api.fptcloud.com/v1"
        elif "gpt" in model_lower or "openai" in model_lower:
            return "https://mkp-api.fptcloud.com/v1"
        elif "claude" in model_lower:
            return "https://api.anthropic.com"
        elif "gemini" in model_lower:
            return "https://generativelanguage.googleapis.com"
        elif "qwen" in model_lower:
            return "https://mkp-api.fptcloud.com/v1" 
        
        return None
    

settings = Settings()