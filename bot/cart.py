"""
Cart Manager
============

Handles adding products to cart and managing cart operations.
This is the SECOND component in the sniper workflow.
"""

import time
from typing import Optional, List
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout

from .utils import (
    log_success, log_error, log_info, log_warning, 
    Timer, retry_on_failure, save_screenshot, get_timestamp
)


class CartManager:
    """
    Manages cart operations for the sniper bot.
    
    Usage:
        cart = CartManager(page)
        success = cart.add_to_cart_fast()
        cart.go_to_cart()
    """
    
    def __init__(self, page: Page):
        """
        Initialize cart manager.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.timer = Timer()
        
        # Add to Cart button selectors (priority order)
        self.add_to_cart_selectors = [
            'button.add-to-cart-buy-now-btn',
            'button[class*="add-to-cart"]',
            'button:has-text("Add to Cart")',
            'button:has-text("ADD TO CART")',
            '.pdp-button-add-to-cart',
            '[data-spm-anchor-id*="cart"]',
        ]
        
        # Buy Now button selectors
        self.buy_now_selectors = [
            'button.buy-now-btn',
            'button[class*="buy-now"]',
            'button:has-text("Buy Now")',
            'button:has-text("BUY NOW")',
            '.pdp-button-buy-now',
        ]
        
        # Cart-related selectors
        self.cart_icon_selector = '.cart-icon, [class*="cart-icon"], a[href*="/cart"]'
        self.cart_count_selector = '.cart-num, [class*="cart-num"], .cart-count'
        
        # Success indicators
        self.success_indicators = [
            'text=Added to Cart',
            'text=Item added',
            'text=Successfully added',
            '.success-message',
        ]
    
    def find_add_to_cart_button(self):
        """
        Find the Add to Cart button using multiple selectors.
        
        Returns:
            Locator: The button locator if found, None otherwise
        """
        for selector in self.add_to_cart_selectors:
            try:
                button = self.page.locator(selector).first
                if button.count() > 0:
                    return button
            except:
                continue
        return None
    
    def find_buy_now_button(self):
        """
        Find the Buy Now button using multiple selectors.
        
        Returns:
            Locator: The button locator if found, None otherwise
        """
        for selector in self.buy_now_selectors:
            try:
                button = self.page.locator(selector).first
                if button.count() > 0:
                    return button
            except:
                continue
        return None
    
    def add_to_cart_fast(self, use_buy_now: bool = False) -> bool:
        """
        Add product to cart as fast as possible.
        Uses force=True to skip animations and visibility checks.
        
        Args:
            use_buy_now: If True, click Buy Now instead of Add to Cart
            
        Returns:
            bool: True if successful
        """
        self.timer.start()
        log_info(f"[{get_timestamp()}] Attempting to add to cart...")
        
        try:
            if use_buy_now:
                button = self.find_buy_now_button()
                button_type = "Buy Now"
            else:
                button = self.find_add_to_cart_button()
                button_type = "Add to Cart"
            
            if not button:
                log_error(f"{button_type} button not found!")
                save_screenshot(self.page, f"cart_error_{int(time.time())}.png")
                return False
            
            # Click with force=True for maximum speed
            button.click(force=True, timeout=5000)
            
            elapsed = self.timer.elapsed()
            log_success(f"[{get_timestamp()}] Clicked {button_type} in {elapsed*1000:.0f}ms!")
            
            # Handle any popups/modals quickly
            self._handle_cart_modal()
            
            return True
            
        except Exception as e:
            log_error(f"Failed to add to cart: {e}")
            save_screenshot(self.page, f"cart_error_{int(time.time())}.png")
            return False
    
    def _handle_cart_modal(self):
        """
        Handle cart confirmation modals/popups.
        Some sites show a modal after adding to cart.
        """
        try:
            # Common modal close buttons
            modal_close_selectors = [
                'button:has-text("Continue Shopping")',
                'button:has-text("Close")',
                '.modal-close',
                '[class*="close-button"]',
            ]
            
            # Wait briefly for modal
            time.sleep(0.3)
            
            for selector in modal_close_selectors:
                try:
                    close_btn = self.page.locator(selector).first
                    if close_btn.count() > 0:
                        close_btn.click(timeout=1000)
                        log_info("Closed cart modal")
                        return
                except:
                    continue
                    
        except:
            pass  # No modal or already closed
    
    @retry_on_failure(max_attempts=3)
    def add_to_cart_with_retry(self, use_buy_now: bool = False) -> bool:
        """
        Add to cart with automatic retry on failure.
        
        Args:
            use_buy_now: If True, use Buy Now instead
            
        Returns:
            bool: True if successful
        """
        return self.add_to_cart_fast(use_buy_now=use_buy_now)
    
    def verify_in_cart(self) -> bool:
        """
        Verify that item was successfully added to cart.
        
        Returns:
            bool: True if item is in cart
        """
        try:
            # Method 1: Check cart count
            cart_count = self.page.locator(self.cart_count_selector).first
            if cart_count.count() > 0:
                count_text = cart_count.inner_text()
                if count_text and int(count_text) > 0:
                    log_success(f"Cart contains {count_text} item(s)")
                    return True
            
            # Method 2: Check for success message
            for selector in self.success_indicators:
                if self.page.locator(selector).count() > 0:
                    log_success("Found success indicator")
                    return True
            
            # Method 3: Navigate to cart and check
            return self._check_cart_page()
            
        except Exception as e:
            log_warning(f"Error verifying cart: {e}")
            return False
    
    def _check_cart_page(self) -> bool:
        """Check cart by navigating to cart page"""
        try:
            current_url = self.page.url
            self.page.goto("https://www.lazada.sg/cart", wait_until="domcontentloaded")
            
            # Check if cart has items
            empty_indicators = [
                'text=Your shopping cart is empty',
                'text=No items',
                '.empty-cart',
            ]
            
            for selector in empty_indicators:
                if self.page.locator(selector).count() > 0:
                    log_warning("Cart is empty")
                    return False
            
            log_success("Items found in cart")
            return True
            
        except Exception as e:
            log_error(f"Error checking cart page: {e}")
            return False
    
    def go_to_cart(self) -> bool:
        """
        Navigate to cart page.
        
        Returns:
            bool: True if successful
        """
        try:
            log_info("Navigating to cart...")
            
            # Try clicking cart icon first
            try:
                cart_icon = self.page.locator(self.cart_icon_selector).first
                if cart_icon.count() > 0:
                    cart_icon.click()
                    self.page.wait_for_load_state("domcontentloaded")
                    log_success("Navigated to cart via icon")
                    return True
            except:
                pass
            
            # Fall back to direct URL
            self.page.goto("https://www.lazada.sg/cart", wait_until="domcontentloaded")
            log_success("Navigated to cart via URL")
            return True
            
        except Exception as e:
            log_error(f"Failed to navigate to cart: {e}")
            return False
    
    def get_cart_items(self) -> List[dict]:
        """
        Get list of items currently in cart.
        
        Returns:
            List[dict]: List of cart items with details
        """
        items = []
        
        try:
            # Common cart item container selectors
            item_selectors = [
                '.cart-item',
                '[class*="cart-item"]',
                '.item-container',
            ]
            
            for selector in item_selectors:
                try:
                    item_elements = self.page.locator(selector).all()
                    
                    if item_elements:
                        for elem in item_elements:
                            item_info = {
                                'name': None,
                                'price': None,
                                'quantity': None,
                            }
                            
                            try:
                                # Extract item details
                                item_info['name'] = elem.locator('.item-title, [class*="title"]').first.inner_text()
                                item_info['price'] = elem.locator('.item-price, [class*="price"]').first.inner_text()
                                item_info['quantity'] = elem.locator('input[type="number"]').first.input_value()
                            except:
                                pass
                            
                            items.append(item_info)
                        
                        if items:
                            break
                            
                except:
                    continue
            
            log_info(f"Found {len(items)} item(s) in cart")
            
        except Exception as e:
            log_warning(f"Error getting cart items: {e}")
        
        return items
    
    def clear_cart(self) -> bool:
        """
        Clear all items from cart.
        WARNING: This will remove ALL items!
        
        Returns:
            bool: True if successful
        """
        try:
            log_warning("Clearing cart...")
            
            # Go to cart first
            self.go_to_cart()
            
            # Find and click delete buttons
            delete_selectors = [
                'button:has-text("Delete")',
                'button:has-text("Remove")',
                '.delete-btn',
                '[class*="delete"]',
            ]
            
            for selector in delete_selectors:
                try:
                    buttons = self.page.locator(selector).all()
                    for button in buttons:
                        try:
                            button.click()
                            time.sleep(0.5)
                        except:
                            pass
                except:
                    continue
            
            log_success("Cart cleared")
            return True
            
        except Exception as e:
            log_error(f"Failed to clear cart: {e}")
            return False

