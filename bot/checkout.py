"""
Checkout Manager
================

Handles checkout process automation.
This is the FINAL component in the sniper workflow.

⚠️  WARNING: This automates the purchase process!
Only use with AUTO_PURCHASE=True if you're absolutely sure!
"""

import time
from typing import Optional, Dict
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout

from .utils import (
    log_success, log_error, log_info, log_warning,
    Timer, save_screenshot, get_timestamp
)


class CheckoutManager:
    """
    Manages checkout and purchase process.
    
    Usage:
        checkout = CheckoutManager(page, auto_purchase=False)
        checkout.proceed_to_checkout()
        checkout.complete_purchase()  # Only if auto_purchase=True
    """
    
    def __init__(self, page: Page, auto_purchase: bool = False):
        """
        Initialize checkout manager.
        
        Args:
            page: Playwright page object
            auto_purchase: If True, automatically complete purchase (DANGEROUS!)
        """
        self.page = page
        self.auto_purchase = auto_purchase
        self.timer = Timer()
        
        if auto_purchase:
            log_warning("⚠️  AUTO-PURCHASE IS ENABLED! Bot will complete purchases!")
        
        # Checkout button selectors
        self.checkout_selectors = [
            'button:has-text("Proceed to Checkout")',
            'button:has-text("Checkout")',
            'button:has-text("CHECK OUT")',
            '.checkout-button',
            '[class*="checkout-btn"]',
            'button[data-spm*="checkout"]',
        ]
        
        # Place Order button selectors
        self.place_order_selectors = [
            'button:has-text("Place Order")',
            'button:has-text("PLACE ORDER")',
            'button:has-text("Confirm Order")',
            '.place-order-btn',
            '[class*="place-order"]',
            'button.next-btn',
        ]
        
        # Payment method selectors
        self.payment_selectors = {
            'cod': 'text=Cash on Delivery',
            'credit_card': 'text=Credit/Debit Card',
            'online_banking': 'text=Online Banking',
        }
    
    def proceed_to_checkout(self) -> bool:
        """
        Navigate from cart to checkout page.
        
        Returns:
            bool: True if successful
        """
        self.timer.start()
        log_info(f"[{get_timestamp()}] Proceeding to checkout...")
        
        try:
            # Make sure we're on cart page
            if '/cart' not in self.page.url:
                self.page.goto("https://www.lazada.sg/cart", wait_until="domcontentloaded")
            
            # Find and click checkout button
            checkout_button = None
            for selector in self.checkout_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.count() > 0:
                        checkout_button = button
                        break
                except:
                    continue
            
            if not checkout_button:
                log_error("Checkout button not found!")
                save_screenshot(self.page, f"checkout_error_{int(time.time())}.png")
                return False
            
            # Click checkout button
            checkout_button.click(force=True)
            
            # Wait for checkout page to load
            self.page.wait_for_load_state("domcontentloaded")
            
            elapsed = self.timer.elapsed()
            log_success(f"[{get_timestamp()}] Reached checkout page in {elapsed*1000:.0f}ms!")
            
            return True
            
        except Exception as e:
            log_error(f"Failed to proceed to checkout: {e}")
            save_screenshot(self.page, f"checkout_error_{int(time.time())}.png")
            return False
    
    def verify_shipping_address(self) -> bool:
        """
        Verify that shipping address is set.
        
        Returns:
            bool: True if address is set
        """
        try:
            # Look for address information
            address_selectors = [
                '.delivery-address',
                '[class*="address"]',
                'text=/.*Street.*/',
                'text=/.*Postal Code.*/',
            ]
            
            for selector in address_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        log_success("Shipping address found")
                        return True
                except:
                    continue
            
            log_warning("No shipping address found - may need to set one")
            return False
            
        except Exception as e:
            log_warning(f"Error verifying address: {e}")
            return False
    
    def select_payment_method(self, method: str = 'cod') -> bool:
        """
        Select payment method.
        
        Args:
            method: Payment method ('cod', 'credit_card', 'online_banking')
            
        Returns:
            bool: True if successful
        """
        try:
            log_info(f"Selecting payment method: {method}")
            
            if method not in self.payment_selectors:
                log_warning(f"Unknown payment method: {method}, using COD")
                method = 'cod'
            
            selector = self.payment_selectors[method]
            payment_option = self.page.locator(selector).first
            
            if payment_option.count() > 0:
                payment_option.click()
                log_success(f"Selected {method}")
                return True
            else:
                log_warning(f"Payment method {method} not found")
                return False
                
        except Exception as e:
            log_error(f"Failed to select payment method: {e}")
            return False
    
    def get_order_summary(self) -> Dict:
        """
        Extract order summary information.
        
        Returns:
            dict: Order details (subtotal, shipping, total)
        """
        summary = {
            'subtotal': None,
            'shipping': None,
            'discount': None,
            'total': None,
            'items': []
        }
        
        try:
            # Get total price (most important!)
            total_selectors = [
                '.order-total',
                '[class*="total-price"]',
                'text=/Total.*SGD/',
            ]
            
            for selector in total_selectors:
                try:
                    total_elem = self.page.locator(selector).first
                    if total_elem.count() > 0:
                        summary['total'] = total_elem.inner_text()
                        break
                except:
                    continue
            
            if summary['total']:
                log_info(f"Order total: {summary['total']}")
            
        except Exception as e:
            log_warning(f"Error getting order summary: {e}")
        
        return summary
    
    def complete_purchase(self) -> bool:
        """
        Complete the purchase by clicking Place Order.
        
        ⚠️  WARNING: This will actually place an order!
        Only runs if auto_purchase=True
        
        Returns:
            bool: True if successful
        """
        if not self.auto_purchase:
            log_warning("⚠️  AUTO_PURCHASE is disabled. Not placing order.")
            log_info("💡 Set auto_purchase=True to enable automatic purchase")
            log_info("📋 Order is ready - you can complete manually!")
            return False
        
        log_warning("⚠️  ATTEMPTING TO PLACE ORDER!")
        log_warning("⚠️  This will complete a real purchase!")
        
        # Safety pause
        log_info("⏸️  5 second safety pause... (Ctrl+C to abort)")
        time.sleep(5)
        
        try:
            # Show order summary one last time
            summary = self.get_order_summary()
            if summary['total']:
                log_warning(f"💰 ORDER TOTAL: {summary['total']}")
            
            # Find Place Order button
            place_order_button = None
            for selector in self.place_order_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.count() > 0:
                        place_order_button = button
                        break
                except:
                    continue
            
            if not place_order_button:
                log_error("Place Order button not found!")
                save_screenshot(self.page, f"place_order_error_{int(time.time())}.png")
                return False
            
            # Click Place Order
            log_warning("🛒 Clicking Place Order...")
            place_order_button.click(force=True)
            
            # Wait for confirmation
            time.sleep(3)
            
            # Check for success indicators
            success_indicators = [
                'text=Order Placed',
                'text=Thank you for your order',
                'text=Order confirmed',
                '.order-success',
            ]
            
            for selector in success_indicators:
                if self.page.locator(selector).count() > 0:
                    log_success("✅ ORDER PLACED SUCCESSFULLY!")
                    save_screenshot(self.page, f"order_success_{int(time.time())}.png")
                    return True
            
            log_warning("Order submitted but confirmation unclear")
            save_screenshot(self.page, f"order_status_{int(time.time())}.png")
            return True
            
        except Exception as e:
            log_error(f"Failed to place order: {e}")
            save_screenshot(self.page, f"place_order_error_{int(time.time())}.png")
            return False
    
    def handle_otp(self, timeout: float = 60) -> bool:
        """
        Handle OTP/2FA verification.
        This requires manual user input.
        
        Args:
            timeout: Seconds to wait for OTP
            
        Returns:
            bool: True if OTP handled successfully
        """
        log_warning("⚠️  OTP/2FA required!")
        log_info(f"Please enter OTP in the browser (waiting {timeout}s)")
        
        try:
            # Wait for OTP page to disappear or success page
            start = time.time()
            while time.time() - start < timeout:
                # Check if we've moved past OTP
                if 'otp' not in self.page.url.lower():
                    log_success("OTP verification completed")
                    return True
                
                time.sleep(1)
            
            log_warning("OTP timeout - verification not completed")
            return False
            
        except Exception as e:
            log_error(f"Error handling OTP: {e}")
            return False
    
    def take_confirmation_screenshot(self, filename: str = None):
        """
        Take screenshot of confirmation page.
        
        Args:
            filename: Custom filename (optional)
        """
        if not filename:
            filename = f"order_confirmation_{int(time.time())}.png"
        
        save_screenshot(self.page, filename)
        log_success(f"Confirmation screenshot saved: {filename}")

