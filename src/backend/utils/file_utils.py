import os
import platform
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

def get_downloads_folder():
    """
    Detect the operating system and return the path to the user's Downloads folder.
    Verifies existence and write permissions. Falls back to user's home directory if Downloads 
    folder cannot be accessed.
    
    Returns:
        Path: Path to the Downloads folder or user's home directory as fallback
    """
    # Get user's home directory - works on all platforms
    home_dir = Path.home()
    
    # Determine OS and set Downloads path accordingly
    os_name = platform.system()
    if os_name == 'Windows':
        downloads_path = home_dir / 'Downloads'
        logger.info(f"Detected Windows OS. Downloads path: {downloads_path}")
    elif os_name == 'Darwin':  # macOS
        downloads_path = home_dir / 'Downloads'
        logger.info(f"Detected macOS. Downloads path: {downloads_path}")
    elif os_name == 'Linux':
        downloads_path = home_dir / 'Downloads'
        logger.info(f"Detected Linux OS. Downloads path: {downloads_path}")
    else:
        # For other or unknown OS, use home directory
        downloads_path = home_dir
        logger.warning(f"Unknown OS: {os_name}. Using home directory as default: {downloads_path}")
    
    # Verify if path exists
    if not downloads_path.exists():
        logger.warning(f"Downloads directory {downloads_path} does not exist. Using {home_dir} as fallback.")
        return home_dir
    
    # Verify write permissions
    if not os.access(downloads_path, os.W_OK):
        logger.warning(f"No write permission for Downloads directory {downloads_path}. Using {home_dir} as fallback.")
        return home_dir
    
    logger.info(f"Using Downloads directory: {downloads_path}")
    return downloads_path

