"""
Configuration management for BA Engine Orchestrator
Loads settings from environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # Gemini API Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"  # Latest, fast, powerful free model
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "[ERROR] GEMINI_API_KEY not set! "
                "Please add it to .env file"
            )
        print("[OK] Configuration loaded successfully")


# Validate config on import
Config.validate()
