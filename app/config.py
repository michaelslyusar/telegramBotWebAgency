"""
WWWizards Telegram Bot - Configuration Management
"""
from pathlib import Path
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Bot Configuration
    BOT_TOKEN: str = Field(..., description="Telegram bot token")

    MANAGER_CHAT_ID: str = Field('1', description="Manager's Telegram chat ID")
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_FILE: Optional[str] = Field(
        None, description="Path to Google Sheets credentials JSON file"
    )
    GOOGLE_SHEETS_SPREADSHEET_ID: Optional[str] = Field(
        ..., description="Google Sheets spreadsheet ID"
    )
    GOOGLE_SHEETS_WORKSHEET_NAME: str = Field(
        "Leads", description="Google Sheets worksheet name"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        ..., description="Database connection URL"
    )
    USE_GOOGLE_SHEETS: bool = Field(
        False, description="Use Google Sheets as primary storage"
    )
    
    # Application Settings
    DEBUG: bool = Field(False, description="Enable debug mode")
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    ENVIRONMENT: str = Field("development", description="Environment name")
    
    # Company Information
    COMPANY_NAME: str = Field("WWWizards", description="Company name")
    COMPANY_WEBSITE_RU: str = Field(
        "https://site.ru", description="Company website (Russian)"
    )
    COMPANY_WEBSITE_COM: str = Field(
        "https://site.com", description="Company website (International)"
    )
    COMPANY_EMAIL: str = Field(
        "info@wwwizards.com", description="Company email"
    )
    COMPANY_TELEGRAM: str = Field(
        "@wwwizards", description="Company Telegram handle"
    )
    
    # File Paths
    PDF_FAQ_PATH: str = Field(
        "./assets/faq.pdf", description="Path to FAQ PDF file"
    )


# Global settings instance
settings = Settings()

