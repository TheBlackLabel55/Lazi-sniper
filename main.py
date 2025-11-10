"""
Lazada Listing Sniper Bot - Main Entry Point
=============================================

This is the main script that ties all components together.

⚠️  IMPORTANT:
- For EDUCATIONAL purposes only
- May violate Lazada's Terms of Service
- Use at your own risk
- Test with non-critical items first
- Set AUTO_PURCHASE=False for safety (manual completion)

Usage:
    python main.py
"""

import sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

from config.settings import BROWSER_CONFIG, BOT_CONFIG, LAZADA_BASE_URL
from bot import ProductMonitor, CartManager, CheckoutManager
from bot.utils import (
    log_success, log_error, log_info, log_warning,
    wait_until, get_accurate_time, validate_url, Timer
)


class LazadaSniper:
    """
    Main sniper bot class that orchestrates all components.
    """
    
    def __init__(
        self,
        product_url: str,
        listing_time: datetime,
        auto_purchase: bool = False,
        headless: bool = False
    ):
        """
        Initialize the sniper bot.
        
        Args:
            product_url: URL of the product to snipe
            listing_time: When the product becomes available
            auto_purchase: If True, automatically complete purchase (DANGEROUS!)
            headless: If True, run browser in background
        """
        if not validate_url(product_url):
            raise ValueError(f"Invalid Lazada URL: {product_url}")
        
        self.product_url = product_url
        self.listing_time = listing_time
        self.auto_purchase = auto_purchase
        self.headless = headless
        
        self.browser = None
        self.page = None
        self.monitor = None
        self.cart = None
        self.checkout = None
        
        self.overall_timer = Timer()
    
    def setup(self):
        """Setup browser and components"""
        log_info("🚀 Initializing Lazada Sniper Bot...")
        log_info(f"📍 Target: {self.product_url}")
        log_info(f"⏰ Listing time: {self.listing_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if listing time is in the future
        current_time = get_accurate_time()
        if self.listing_time <= current_time:
            log_warning("⚠️  Listing time is in the past! Starting immediately...")
        else:
            time_until = (self.listing_time - current_time).total_seconds()
            log_info(f"⏳ Time until listing: {time_until/60:.1f} minutes")
        
        # Launch browser
        log_info("🌐 Launching browser...")
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            slow_mo=BROWSER_CONFIG.get('slow_mo', 0)
        )
        
        # Create page
        self.page = self.browser.new_page()
        self.page.set_default_timeout(BROWSER_CONFIG['timeout'])
        
        # Initialize components
        self.monitor = ProductMonitor(self.page, check_interval=0.05)
        self.cart = CartManager(self.page)
        self.checkout = CheckoutManager(self.page, auto_purchase=self.auto_purchase)
        
        log_success("✅ Setup complete!")
    
    def pre_load(self):
        """Pre-load the product page"""
        log_info("📄 Pre-loading product page...")
        
        try:
            self.monitor.pre_load(self.product_url)
            
            # Get product info
            info = self.monitor.get_product_info()
            
            print("\n" + "="*60)
            print("📦 PRODUCT INFORMATION")
            print("="*60)
            if info['title']:
                print(f"Title: {info['title']}")
            if info['price']:
                print(f"Price: {info['price']}")
            print(f"Currently Available: {info['available']}")
            print("="*60 + "\n")
            
        except Exception as e:
            log_error(f"Failed to pre-load: {e}")
            raise
    
    def wait_for_listing_time(self):
        """Wait until listing time"""
        current_time = get_accurate_time()
        
        if self.listing_time > current_time:
            log_info("⏰ Waiting for listing time...")
            wait_until(self.listing_time, pre_load_seconds=5)
        else:
            log_info("🎯 Starting immediately (listing time already passed)")
    
    def monitor_and_snipe(self) -> bool:
        """Monitor for availability and snipe immediately"""
        log_info("👀 Starting product monitoring...")
        log_info("⚡ Will attempt to add to cart the instant it's available!")
        
        # Check if already available
        if self.monitor.is_product_available():
            log_success("Product already available!")
            return True
        
        # Monitor for availability
        max_wait = 300  # 5 minutes max
        is_available = self.monitor.wait_for_availability(max_wait=max_wait)
        
        return is_available
    
    def add_to_cart(self) -> bool:
        """Add product to cart"""
        log_info("🛒 Adding to cart...")
        
        # Try to add to cart with retry
        success = self.cart.add_to_cart_with_retry(use_buy_now=False)
        
        if not success:
            log_error("Failed to add to cart!")
            return False
        
        # Verify it's in cart
        log_info("✓ Verifying item in cart...")
        if not self.cart.verify_in_cart():
            log_warning("Could not verify item in cart, but continuing...")
        
        return True
    
    def process_checkout(self) -> bool:
        """Process checkout"""
        log_info("💳 Processing checkout...")
        
        # Go to cart first
        if not self.cart.go_to_cart():
            log_error("Failed to navigate to cart!")
            return False
        
        # Proceed to checkout
        if not self.checkout.proceed_to_checkout():
            log_error("Failed to proceed to checkout!")
            return False
        
        # Verify shipping address
        self.checkout.verify_shipping_address()
        
        # Get order summary
        summary = self.checkout.get_order_summary()
        
        if summary['total']:
            print("\n" + "="*60)
            print("💰 ORDER SUMMARY")
            print("="*60)
            print(f"Total: {summary['total']}")
            print("="*60 + "\n")
        
        # Complete purchase (if auto_purchase enabled)
        if self.auto_purchase:
            log_warning("⚠️  Auto-purchase is ENABLED!")
            return self.checkout.complete_purchase()
        else:
            log_info("✅ Ready to checkout!")
            log_info("💡 AUTO_PURCHASE is disabled - complete purchase manually")
            log_info("🖱️  Click 'Place Order' button in the browser when ready")
            return True
    
    def run(self):
        """Main execution flow"""
        try:
            self.overall_timer.start()
            
            # Setup
            self.setup()
            
            # Pre-load product page
            self.pre_load()
            
            # Wait for listing time
            self.wait_for_listing_time()
            
            # Monitor and snipe
            if not self.monitor_and_snipe():
                log_error("❌ Failed to detect product availability!")
                return False
            
            # Add to cart
            if not self.add_to_cart():
                log_error("❌ Failed to add to cart!")
                return False
            
            # Process checkout
            if not self.process_checkout():
                log_error("❌ Failed to process checkout!")
                return False
            
            # Success!
            elapsed = self.overall_timer.elapsed()
            print("\n" + "="*60)
            print("🎉 SNIPER BOT COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"⏱️  Total time: {elapsed:.2f} seconds")
            print("="*60 + "\n")
            
            if not self.auto_purchase:
                log_info("Browser will stay open - complete purchase manually")
                log_info("Press Ctrl+C when done")
                try:
                    while True:
                        pass  # Keep browser open
                except KeyboardInterrupt:
                    log_info("Closing browser...")
            
            return True
            
        except KeyboardInterrupt:
            log_warning("\n⚠️  Interrupted by user")
            return False
            
        except Exception as e:
            log_error(f"❌ Critical error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            if self.browser:
                self.browser.close()
                log_info("Browser closed")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.browser:
            try:
                self.browser.close()
            except:
                pass


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  LAZADA LISTING SNIPER BOT")
    print("="*60)
    print("\n⚠️  DISCLAIMER:")
    print("This bot is for EDUCATIONAL purposes only!")
    print("Using automation may violate Lazada's Terms of Service.")
    print("Use at your own risk!\n")
    print("="*60 + "\n")
    
    # ============================================
    # CONFIGURATION - EDIT THESE VALUES
    # ============================================
    
    # Product URL
    PRODUCT_URL = "https://www.lazada.sg/products/your-product-url-here"
    
    # Listing time (when product becomes available)
    # Format: datetime(year, month, day, hour, minute, second)
    # Example: 2024 December 25, 12:00:00 PM
    LISTING_TIME = datetime(2024, 12, 25, 12, 0, 0)
    
    # Or list 5 minutes from now for testing:
    # LISTING_TIME = datetime.now() + timedelta(minutes=5)
    
    # Auto-purchase setting (DANGEROUS - will complete purchase!)
    AUTO_PURCHASE = False  # Set to True to automatically complete purchase
    
    # Headless mode (run browser in background)
    HEADLESS = False  # Set to True to hide browser
    
    # ============================================
    # END CONFIGURATION
    # ============================================
    
    # Validate configuration
    if "your-product-url-here" in PRODUCT_URL:
        log_error("❌ Please set PRODUCT_URL in main.py!")
        log_info("💡 Edit main.py and set the product URL")
        sys.exit(1)
    
    # Confirm auto-purchase
    if AUTO_PURCHASE:
        log_warning("⚠️  AUTO_PURCHASE IS ENABLED!")
        log_warning("⚠️  This will automatically complete the purchase!")
        response = input("Are you sure? Type 'YES' to continue: ")
        if response != "YES":
            log_info("Cancelled by user")
            sys.exit(0)
    
    # Create and run sniper
    sniper = LazadaSniper(
        product_url=PRODUCT_URL,
        listing_time=LISTING_TIME,
        auto_purchase=AUTO_PURCHASE,
        headless=HEADLESS
    )
    
    try:
        success = sniper.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log_warning("\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()

