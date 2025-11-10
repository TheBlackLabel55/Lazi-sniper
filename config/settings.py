"""
Configuration settings for Lazada Sniper Bot
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Lazada Singapore URLs
LAZADA_BASE_URL = "https://www.lazada.sg"
LAZADA_CART_URL = f"{LAZADA_BASE_URL}/cart"
LAZADA_CHECKOUT_URL = f"{LAZADA_BASE_URL}/checkout"

# Browser settings
BROWSER_CONFIG = {
    "headless": False,  # Set to True for faster, invisible browser
    "slow_mo": 50,      # Milliseconds to slow down operations (for learning)
    "timeout": 30000,   # Default timeout in milliseconds
}

# Timing settings
TIMING_CONFIG = {
    "check_interval": 0.1,      # Seconds between availability checks
    "max_wait_time": 300,       # Maximum seconds to wait for product
    "pre_load_time": 60,        # Seconds before listing to start monitoring
}

# Bot behavior settings
BOT_CONFIG = {
    "auto_purchase": False,     # WARNING: Set to True to auto-complete purchase
    "max_retries": 3,           # Retry attempts for failed operations
    "screenshot_on_error": True, # Save screenshot when errors occur
}

# User credentials (DO NOT COMMIT REAL CREDENTIALS)
USER_CONFIG = {
    "email": os.getenv("LAZADA_EMAIL", ""),
    "password": os.getenv("LAZADA_PASSWORD", ""),
}

# Logging
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# Selectors (these may need to be updated as Lazada changes their website)
SELECTORS = {
    "add_to_cart_button": "button.add-to-cart-buy-now-btn",
    "buy_now_button": "button.buy-now-btn",
    "cart_icon": ".cart-icon",
    "checkout_button": "button[data-spm-anchor-id*='checkout']",
    "place_order_button": "button.next-btn",
}

# Notification settings
NOTIFICATION_CONFIG = {
    "enabled": True,
    "sound": True,
    "desktop": False,  # Desktop notifications (requires additional setup)
}

