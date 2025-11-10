"""
Product Monitor
===============

Monitors a Lazada product page and detects when it becomes available.
This is the FIRST component that runs in the sniper bot.
"""

import time
from datetime import datetime
from typing import Optional, Callable
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout

from .utils import log_success, log_error, log_info, log_warning, Timer, get_timestamp


class ProductMonitor:
    """
    Monitors a product page for availability.
    
    Usage:
        monitor = ProductMonitor(page, check_interval=0.05)
        is_available = monitor.wait_for_availability(max_wait=300)
    """
    
    def __init__(self, page: Page, check_interval: float = 0.1):
        """
        Initialize product monitor.
        
        Args:
            page: Playwright page object
            check_interval: Seconds between checks (lower = faster, higher = less CPU)
        """
        self.page = page
        self.check_interval = check_interval
        self.timer = Timer()
        
        # Possible selectors for Add to Cart button
        self.add_to_cart_selectors = [
            'button.add-to-cart-buy-now-btn',
            'button[class*="add-to-cart"]',
            'button:has-text("Add to Cart")',
            'button:has-text("ADD TO CART")',
            '.pdp-button-add-to-cart',
            '[data-spm-anchor-id*="cart"]',
        ]
        
        # Possible selectors for Buy Now button
        self.buy_now_selectors = [
            'button.buy-now-btn',
            'button[class*="buy-now"]',
            'button:has-text("Buy Now")',
            'button:has-text("BUY NOW")',
            '.pdp-button-buy-now',
        ]
        
        # Selectors for out-of-stock indicators
        self.out_of_stock_selectors = [
            'text=Out of Stock',
            'text=Currently Unavailable',
            'text=Sold Out',
            '.pdp-product-not-available',
        ]
    
    def is_product_available(self) -> bool:
        """
        Check if product is currently available for purchase.
        
        Returns:
            bool: True if Add to Cart or Buy Now button is clickable
        """
        try:
            # Method 1: Check if Add to Cart button exists and is enabled
            for selector in self.add_to_cart_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.count() > 0:
                        # Check if button is enabled (not disabled)
                        is_disabled = button.get_attribute('disabled')
                        if not is_disabled:
                            log_success(f"[{get_timestamp()}] Product available! (found: {selector})")
                            return True
                except:
                    continue
            
            # Method 2: Check Buy Now button
            for selector in self.buy_now_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.count() > 0:
                        is_disabled = button.get_attribute('disabled')
                        if not is_disabled:
                            log_success(f"[{get_timestamp()}] Product available! (found: {selector})")
                            return True
                except:
                    continue
            
            # Method 3: Check if out of stock message is NOT present
            for selector in self.out_of_stock_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        return False
                except:
                    continue
            
            return False
            
        except Exception as e:
            log_warning(f"Error checking availability: {e}")
            return False
    
    def wait_for_availability(
        self, 
        max_wait: float = 300,
        on_check: Optional[Callable] = None
    ) -> bool:
        """
        Wait for product to become available.
        
        Args:
            max_wait: Maximum seconds to wait
            on_check: Optional callback function called on each check
            
        Returns:
            bool: True if product became available, False if timeout
        """
        log_info(f"Starting product monitoring (checking every {self.check_interval}s)")
        log_info(f"Maximum wait time: {max_wait}s")
        
        self.timer.start()
        checks = 0
        
        while self.timer.elapsed() < max_wait:
            checks += 1
            
            # Check if available
            if self.is_product_available():
                log_success(f"Product available after {self.timer} ({checks} checks)")
                return True
            
            # Call callback if provided
            if on_check:
                on_check(checks, self.timer.elapsed())
            
            # Log progress every 100 checks
            if checks % 100 == 0:
                elapsed = self.timer.elapsed()
                rate = checks / elapsed if elapsed > 0 else 0
                log_info(f"Check #{checks} ({rate:.1f} checks/sec, {elapsed:.1f}s elapsed)")
            
            # Wait before next check
            time.sleep(self.check_interval)
        
        log_error(f"Timeout after {self.timer} ({checks} checks)")
        return False
    
    def continuous_monitor(
        self,
        callback: Callable,
        check_interval: Optional[float] = None
    ):
        """
        Continuously monitor and call callback when available.
        This runs indefinitely until callback returns False.
        
        Args:
            callback: Function to call when product becomes available
            check_interval: Override default check interval
        """
        interval = check_interval or self.check_interval
        log_info("Starting continuous monitoring (Ctrl+C to stop)")
        
        try:
            while True:
                if self.is_product_available():
                    # Call callback and check if we should continue
                    should_continue = callback()
                    if not should_continue:
                        break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            log_warning("Monitoring stopped by user")
    
    def refresh_page(self):
        """Refresh the product page"""
        try:
            log_info("Refreshing page...")
            self.page.reload(wait_until="domcontentloaded")
            log_success("Page refreshed")
        except Exception as e:
            log_error(f"Failed to refresh page: {e}")
    
    def get_product_info(self) -> dict:
        """
        Extract product information from page.
        
        Returns:
            dict: Product info (title, price, availability)
        """
        info = {
            'title': None,
            'price': None,
            'original_price': None,
            'discount': None,
            'available': False,
        }
        
        try:
            # Get product title
            title_selectors = [
                'h1.pdp-mod-product-badge-title',
                '.pdp-product-title',
                'h1[class*="title"]',
            ]
            for selector in title_selectors:
                try:
                    title = self.page.locator(selector).first.inner_text()
                    if title:
                        info['title'] = title.strip()
                        break
                except:
                    continue
            
            # Get price
            price_selectors = [
                '.pdp-price',
                'span[class*="price"]',
                '.price-current',
            ]
            for selector in price_selectors:
                try:
                    price = self.page.locator(selector).first.inner_text()
                    if price:
                        info['price'] = price.strip()
                        break
                except:
                    continue
            
            # Check availability
            info['available'] = self.is_product_available()
            
        except Exception as e:
            log_warning(f"Error extracting product info: {e}")
        
        return info
    
    def pre_load(self, url: str):
        """
        Pre-load product page before monitoring starts.
        
        Args:
            url: Product URL to load
        """
        log_info(f"Pre-loading product page...")
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            log_success("Product page loaded")
            
            # Get and display product info
            info = self.get_product_info()
            if info['title']:
                log_info(f"Product: {info['title']}")
            if info['price']:
                log_info(f"Price: {info['price']}")
            
        except Exception as e:
            log_error(f"Failed to load product page: {e}")
            raise

