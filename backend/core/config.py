import os
from dotenv import load_dotenv

# Load environment variables from specific paths
# Try loading from root .env first
root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(root_env):
    load_dotenv(root_env)

class Config:
    """Application Configuration"""
    
    # CampX Portal Settings
    CAMPX_BASE_URL = os.getenv('CAMPX_BASE_URL')
    
    # Test Settings
    EX_HTN = os.getenv('EX_HTN')
    
    # Flask Settings
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Export Settings
    EXPORT_DIR = os.getenv('EXPORT_DIR', './exports')
    
    # Webdriver Settings
    HEADLESS_MODE = True
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        missing = []
        if not cls.CAMPX_BASE_URL:
            missing.append("CAMPX_BASE_URL")
            
        if missing:
            raise ValueError(f"Missing configuration variables: {', '.join(missing)}")

# Validate on import? Or let app call it.
# Let's let the app call it to avoid import errors during partial setup.
