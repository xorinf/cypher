import logging
import sys
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance with consistent formatting
    """
    logger = logging.getLogger(name)
    
    # Only configure if handlers haven't been added
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler
        logger.addHandler(console_handler)
        
        # Optional: Add file handler if directory exists
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        if os.path.exists(log_dir):
            file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
    return logger
