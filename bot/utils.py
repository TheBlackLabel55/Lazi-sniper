"""
Utility functions for the sniper bot
"""

import time
from datetime import datetime
from typing import Optional
import ntplib
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


def get_accurate_time() -> datetime:
    """
    Get accurate time from NTP server to ensure precise timing.
    Falls back to system time if NTP is unavailable.
    
    Returns:
        datetime: Current time
    """
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org', timeout=2)
        return datetime.fromtimestamp(response.tx_time)
    except:
        # Fall back to system time
        return datetime.now()


def wait_until(target_time: datetime, pre_load_seconds: int = 5):
    """
    Wait until target time, with countdown display.
    Starts actual monitoring {pre_load_seconds} before target time.
    
    Args:
        target_time: When to start sniping
        pre_load_seconds: Start monitoring this many seconds early
    """
    start_time = target_time.timestamp() - pre_load_seconds
    
    while True:
        current_time = get_accurate_time()
        remaining = start_time - current_time.timestamp()
        
        if remaining <= 0:
            break
        
        if remaining > 60:
            print(f"{Fore.YELLOW}⏰ Waiting... {remaining/60:.1f} minutes until start", end='\r')
        else:
            print(f"{Fore.YELLOW}⏰ Waiting... {remaining:.1f} seconds until start", end='\r')
        
        time.sleep(min(1, remaining))
    
    print(f"\n{Fore.GREEN}🎯 Starting product monitoring!")


def calculate_latency(page) -> float:
    """
    Estimate network latency by measuring navigation time.
    
    Args:
        page: Playwright page object
        
    Returns:
        float: Estimated latency in seconds
    """
    try:
        start = time.time()
        page.goto("https://www.lazada.sg/favicon.ico", wait_until="domcontentloaded")
        latency = time.time() - start
        return latency
    except:
        return 0.15  # Default estimate: 150ms


def retry_on_failure(max_attempts: int = 3, delay: float = 0.5):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"{Fore.YELLOW}⚠️  Attempt {attempt + 1} failed, retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def log_success(message: str):
    """Print success message in green"""
    print(f"{Fore.GREEN}✅ {message}")


def log_error(message: str):
    """Print error message in red"""
    print(f"{Fore.RED}❌ {message}")


def log_info(message: str):
    """Print info message in cyan"""
    print(f"{Fore.CYAN}ℹ️  {message}")


def log_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠️  {message}")


def save_screenshot(page, filename: str = "error.png"):
    """
    Save screenshot for debugging.
    
    Args:
        page: Playwright page object
        filename: Filename to save screenshot
    """
    try:
        filepath = f"screenshots/{filename}"
        page.screenshot(path=filepath)
        log_info(f"Screenshot saved: {filepath}")
    except Exception as e:
        log_error(f"Failed to save screenshot: {e}")


def get_timestamp() -> str:
    """Get current timestamp as formatted string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


class Timer:
    """Simple timer for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        return self
    
    def stop(self):
        """Stop the timer"""
        self.end_time = time.time()
        return self
    
    def elapsed(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def __str__(self):
        return format_duration(self.elapsed())


def validate_url(url: str) -> bool:
    """
    Validate if URL is a valid Lazada product URL.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if valid Lazada URL
    """
    valid_patterns = [
        'lazada.sg/products/',
        'lazada.sg/catalog/',
    ]
    return any(pattern in url.lower() for pattern in valid_patterns)


def extract_product_id(url: str) -> Optional[str]:
    """
    Extract product ID from Lazada URL.
    
    Args:
        url: Lazada product URL
        
    Returns:
        str: Product ID if found, None otherwise
    """
    try:
        # Lazada URLs typically have format: /products/name-i12345678.html
        if '-i' in url:
            product_id = url.split('-i')[1].split('.')[0].split('?')[0]
            return product_id
    except:
        pass
    return None

