import os
from typing import Optional

class Config:
    """
    Configuration class for Resume Analyzer AI Agent
    """
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY: Optional[str] = os.getenv('OPENROUTER_API_KEY', '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')
    
    # Model Configuration
    LLM_MODEL: str = os.getenv('LLM_MODEL', 'openai/gpt-oss-120b:free')
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.3'))
    MAX_TOKENS: int = int(os.getenv('MAX_TOKENS', '1000'))
    REASONING_ENABLED: bool = os.getenv('REASONING_ENABLED', 'false').lower() == 'true'
    
    # Application Configuration
    APP_TITLE: str = "Resume Analyzer AI Agent"
    APP_ICON: str = "📄"
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that required configuration values are present
        """
        if not cls.OPENROUTER_API_KEY:
            print("Warning: OPENROUTER_API_KEY not found in environment variables.")
            print("Please set your OpenRouter API key to enable full LLM functionality.")
            print("Example: export OPENROUTER_API_KEY='your-api-key-here'")
            return False
        return True

# Create a global config instance
config = Config()