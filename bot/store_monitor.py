"""
Store Monitor
=============

Monitors a Lazada store page for new products matching keywords.
This is useful when you don't have a direct product URL yet.
"""

import time
from typing import List, Optional
from playwright.sync_api import Page

from .utils import log_success, log_error, log_info, log_warning, Timer, get_timestamp


class StoreMonitor:
    """
    Monitors a Lazada store page for new products.
    
    Usage:
        monitor = StoreMonitor(page, store_url, product_keywords)
        product_url = monitor.wait_for_product(max_wait=300)
    """
    
    def __init__(
        self, 
        page: Page, 
        store_url: str, 
        product_keywords: List[str],
        check_interval: float = 2.0
    ):
        """
        Initialize store monitor.
        
        Args:
            page: Playwright page object
            store_url: URL of the store to monitor
            product_keywords: List of keywords to match (e.g., ["iPhone", "15", "Pro"])
            check_interval: Seconds between checks (slower than product monitor)
        """
        self.page = page
        self.store_url = store_url
        self.product_keywords = [kw.lower() for kw in product_keywords]
        self.check_interval = check_interval
        self.timer = Timer()
        self.seen_products = set()  # Track products we've already seen
        
        log_info(f"Store Monitor initialized for: {store_url}")
        log_info(f"Searching for keywords: {product_keywords}")
        
        # Selectors for product listings on store page
        self.product_item_selectors = [
            '.Bm3ON',  # Lazada's current product card class
            '[data-item-id]',
            '.item-card',
            '[class*="item"]',
            '.product-item',
        ]
        
        self.product_link_selector = 'a[href*="/products/"]'
        self.product_title_selectors = [
            '.RfADt',  # Lazada's current title class
            '.title',
            '[class*="title"]',
            '.name',
            '[class*="name"]',
            'img[alt]',  # Fallback to image alt text
        ]
    
    def load_store_page(self):
        """Load the store page"""
        try:
            log_info(f"Loading store page...")
            self.page.goto(self.store_url, wait_until="domcontentloaded")
            time.sleep(2)  # Wait for products to load
            log_success("Store page loaded")
        except Exception as e:
            log_error(f"Failed to load store page: {e}")
            raise
    
    def get_all_products(self) -> List[dict]:
        """
        Get all products currently visible on the store page.
        
        Returns:
            List of dicts with 'title', 'url', 'id'
        """
        products = []
        
        try:
            # Find all product items
            for selector in self.product_item_selectors:
                try:
                    items = self.page.locator(selector).all()
                    
                    if len(items) > 0:
                        log_info(f"Found {len(items)} product elements using: {selector}")
                        
                        for item in items:
                            try:
                                # Get product link
                                link = item.locator(self.product_link_selector).first
                                if link.count() == 0:
                                    continue
                                
                                url = link.get_attribute('href')
                                if not url:
                                    continue
                                
                                # Make URL absolute
                                if url.startswith('/'):
                                    url = f"https://www.lazada.sg{url}"
                                
                                # Get product title - try multiple methods
                                title = None
                                
                                # Method 1: Try title selectors
                                for title_sel in self.product_title_selectors:
                                    try:
                                        title_elem = item.locator(title_sel).first
                                        if title_elem.count() > 0:
                                            if title_sel == 'img[alt]':
                                                title = title_elem.get_attribute('alt')
                                            else:
                                                title = title_elem.inner_text().strip()
                                            if title:
                                                break
                                    except:
                                        continue
                                
                                # Method 2: Try getting from link itself
                                if not title:
                                    try:
                                        title = link.inner_text().strip()
                                    except:
                                        pass
                                
                                # Extract product ID from URL
                                product_id = self._extract_product_id(url)
                                
                                if product_id and title:
                                    products.append({
                                        'id': product_id,
                                        'title': title,
                                        'url': url
                                    })
                            except Exception as e:
                                continue
                        
                        if products:
                            break  # Found products, don't try other selectors
                            
                except Exception as e:
                    continue
        
        except Exception as e:
            log_warning(f"Error getting products: {e}")
        
        return products
    
    def _extract_product_id(self, url: str) -> Optional[str]:
        """Extract product ID from URL"""
        try:
            if '-i' in url:
                return url.split('-i')[1].split('.')[0].split('?')[0]
        except:
            pass
        return url  # Use full URL as ID if can't extract
    
    def matches_keywords(self, title: str) -> bool:
        """
        Check if product title matches ANY of the keyword sets.
        
        Args:
            title: Product title to check
            
        Returns:
            bool: True if any keyword found in title
        """
        title_lower = title.lower()
        
        # Check if ANY keyword matches (more flexible for Pokemon products)
        matches = any(keyword in title_lower for keyword in self.product_keywords)
        
        return matches
    
    def find_matching_product(self) -> Optional[dict]:
        """
        Find a product that matches the keywords.
        
        Returns:
            dict with product info if found, None otherwise
        """
        products = self.get_all_products()
        
        log_info(f"Checking {len(products)} products...")
        
        for product in products:
            # Skip if we've already seen this product
            if product['id'] in self.seen_products:
                continue
            
            # Check if matches keywords
            if self.matches_keywords(product['title']):
                log_success(f"[{get_timestamp()}] ✨ FOUND MATCH!")
                log_success(f"Product: {product['title']}")
                log_info(f"URL: {product['url']}")
                return product
        
        return None
    
    def wait_for_product(self, max_wait: float = 300, initial_scan_only: bool = False) -> Optional[str]:
        """
        Wait for a matching product to appear.
        
        Args:
            max_wait: Maximum seconds to wait
            initial_scan_only: If True, only scan once without monitoring
            
        Returns:
            str: Product URL if found, None if timeout
        """
        log_info("=" * 60)
        log_info("🔍 STORE MONITORING ACTIVE")
        log_info("=" * 60)
        log_info(f"Keywords: {self.product_keywords}")
        log_info(f"Check interval: {self.check_interval}s")
        log_info("=" * 60)
        
        self.timer.start()
        checks = 0
        
        if not initial_scan_only:
            # Initial scan to populate seen_products
            log_info("\n📋 Initial scan - identifying existing products...")
            initial_products = self.get_all_products()
            for p in initial_products:
                self.seen_products.add(p['id'])
            log_info(f"Found {len(initial_products)} existing products")
            log_info("(These will be ignored - only NEW products will trigger)")
            log_info("\n👀 Now monitoring for NEW products...\n")
        
        while self.timer.elapsed() < max_wait:
            checks += 1
            
            # Refresh the page to get latest products
            if checks > 1:  # Skip refresh on first check
                try:
                    log_info(f"🔄 Refreshing store page...")
                    self.page.reload(wait_until="domcontentloaded")
                    time.sleep(2)  # Wait for products to load
                except Exception as e:
                    log_warning(f"Refresh failed: {e}")
            
            # Look for matching product
            product = self.find_matching_product()
            
            if product:
                elapsed = self.timer.elapsed()
                log_success("=" * 60)
                log_success(f"🎯 PRODUCT FOUND after {elapsed:.1f}s ({checks} checks)")
                log_success("=" * 60)
                return product['url']
            
            if initial_scan_only:
                log_warning("No matching products found in initial scan")
                return None
            
            # Log progress
            elapsed = self.timer.elapsed()
            log_info(f"Check #{checks} at {elapsed:.1f}s - No new matches yet...")
            
            # Wait before next check
            time.sleep(self.check_interval)
        
        log_error(f"⏰ Timeout after {self.timer} ({checks} checks)")
        return None
    
    def scan_current_products(self) -> List[dict]:
        """
        Just scan and return current products without monitoring.
        Useful for testing.
        
        Returns:
            List of matching products
        """
        products = self.get_all_products()
        matching = []
        
        for product in products:
            if self.matches_keywords(product['title']):
                matching.append(product)
        
        return matching

