"""
Lazada Store Sniper - Pokemon Trading Card Game Edition
========================================================

Monitors the Pokemon Store on Lazada Singapore for new TCG products.

Store URL: https://www.lazada.sg/shop/pokemon-store-online-singapore
Target: Pokemon Trading Card Game products

⚠️  EDUCATIONAL PURPOSES ONLY
May violate Terms of Service - Use at your own risk!
"""

import sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

from config.settings import BROWSER_CONFIG
from bot import ProductMonitor, CartManager, CheckoutManager, StoreMonitor
from bot.utils import (
    log_success, log_error, log_info, log_warning,
    wait_until, get_accurate_time, Timer
)


class LazadaStoreSniper:
    """
    Sniper bot that monitors a store for new products.
    """
    
    def __init__(
        self,
        store_url: str,
        product_keywords: list,
        listing_time: datetime,
        auto_purchase: bool = False,
        headless: bool = False,
        check_interval: float = 2.0
    ):
        """
        Initialize store sniper.
        
        Args:
            store_url: URL of the store to monitor
            product_keywords: Keywords to match (ANY keyword triggers a match)
            listing_time: When to start monitoring
            auto_purchase: Auto-complete purchase
            headless: Run in background
            check_interval: Seconds between store page refreshes
        """
        self.store_url = store_url
        self.product_keywords = product_keywords
        self.listing_time = listing_time
        self.auto_purchase = auto_purchase
        self.headless = headless
        self.check_interval = check_interval
        
        self.browser = None
        self.page = None
        self.store_monitor = None
        self.product_monitor = None
        self.cart = None
        self.checkout = None
        
        self.overall_timer = Timer()
    
    def setup(self):
        """Setup browser and components"""
        print("\n" + "="*60)
        print("🚀 LAZADA STORE SNIPER BOT")
        print("="*60)
        log_info(f"📍 Store: {self.store_url}")
        log_info(f"🔍 Keywords: {', '.join(self.product_keywords)}")
        log_info(f"⏰ Start time: {self.listing_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_info(f"🔄 Check interval: {self.check_interval}s")
        print("="*60)
        
        # Check timing
        current_time = get_accurate_time()
        if self.listing_time <= current_time:
            log_warning("⚠️  Start time is in the past - starting immediately!")
        else:
            time_until = (self.listing_time - current_time).total_seconds()
            log_info(f"⏳ Time until start: {time_until/60:.1f} minutes")
        
        # Launch browser
        log_info("\n🌐 Launching browser...")
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            slow_mo=BROWSER_CONFIG.get('slow_mo', 0)
        )
        
        self.page = self.browser.new_page()
        self.page.set_default_timeout(BROWSER_CONFIG['timeout'])
        
        # Initialize store monitor
        self.store_monitor = StoreMonitor(
            self.page, 
            self.store_url, 
            self.product_keywords,
            check_interval=self.check_interval
        )
        
        log_success("✅ Setup complete!\n")
    
    def wait_for_listing_time(self):
        """Wait until listing time"""
        current_time = get_accurate_time()
        
        if self.listing_time > current_time:
            log_info("⏰ Waiting for start time...")
            wait_until(self.listing_time, pre_load_seconds=5)
        else:
            log_info("🎯 Starting immediately (start time already passed)")
    
    def find_product(self) -> str:
        """
        Monitor store and find product URL.
        
        Returns:
            str: Product URL
        """
        log_info("🔍 Starting store monitoring...\n")
        
        # Load store page
        self.store_monitor.load_store_page()
        
        # Wait for matching product
        product_url = self.store_monitor.wait_for_product(max_wait=300)
        
        if not product_url:
            raise Exception("❌ Product not found within timeout!")
        
        return product_url
    
    def snipe_product(self, product_url: str) -> bool:
        """
        Snipe the found product.
        
        Args:
            product_url: URL of product to snipe
            
        Returns:
            bool: Success
        """
        print("\n" + "="*60)
        log_info(f"🎯 SNIPING PRODUCT")
        log_info(f"📍 URL: {product_url}")
        print("="*60 + "\n")
        
        # Navigate to product page
        log_info("📄 Loading product page...")
        self.page.goto(product_url, wait_until="domcontentloaded")
        
        # Initialize product monitor and cart
        self.product_monitor = ProductMonitor(self.page, check_interval=0.05)
        self.cart = CartManager(self.page)
        self.checkout = CheckoutManager(self.page, auto_purchase=self.auto_purchase)
        
        # Get product info
        info = self.product_monitor.get_product_info()
        if info['title']:
            log_success(f"Product: {info['title']}")
        if info['price']:
            log_info(f"Price: {info['price']}")
        
        # Check if available
        if not self.product_monitor.is_product_available():
            log_error("❌ Product not available for purchase!")
            log_warning("Possible reasons:")
            log_warning("  - Product sold out")
            log_warning("  - Need to select size/variant first")
            log_warning("  - Page hasn't fully loaded")
            return False
        
        log_success("✅ Product is available!")
        
        # Add to cart
        log_info("\n🛒 Adding to cart...")
        if not self.cart.add_to_cart_with_retry():
            log_error("❌ Failed to add to cart!")
            return False
        
        # Go to cart
        log_info("🛒 Navigating to cart...")
        if not self.cart.go_to_cart():
            log_error("❌ Failed to navigate to cart!")
            return False
        
        # Proceed to checkout
        log_info("💳 Proceeding to checkout...")
        if not self.checkout.proceed_to_checkout():
            log_error("❌ Failed to proceed to checkout!")
            return False
        
        # Verify address
        self.checkout.verify_shipping_address()
        
        # Get order summary
        summary = self.checkout.get_order_summary()
        if summary['total']:
            print("\n" + "="*60)
            print("💰 ORDER SUMMARY")
            print("="*60)
            print(f"Total: {summary['total']}")
            print("="*60 + "\n")
        
        # Complete or wait
        if self.auto_purchase:
            log_warning("⚠️  Auto-purchase is ENABLED!")
            return self.checkout.complete_purchase()
        else:
            log_info("✅ Ready for checkout!")
            log_info("💡 AUTO_PURCHASE is disabled - complete manually")
            log_info("🖱️  Click 'Place Order' in the browser when ready")
            return True
    
    def run(self):
        """Main execution"""
        try:
            self.overall_timer.start()
            
            # Setup
            self.setup()
            
            # Wait for listing time
            self.wait_for_listing_time()
            
            # Find product
            product_url = self.find_product()
            
            # Snipe it
            success = self.snipe_product(product_url)
            
            if success:
                elapsed = self.overall_timer.elapsed()
                print("\n" + "="*60)
                print("🎉 SNIPER BOT COMPLETED SUCCESSFULLY!")
                print("="*60)
                print(f"⏱️  Total time: {elapsed:.2f} seconds")
                print("="*60 + "\n")
                
                if not self.auto_purchase:
                    log_info("Browser will stay open for manual completion")
                    log_info("Press Ctrl+C when done")
                    try:
                        while True:
                            pass  # Keep browser open
                    except KeyboardInterrupt:
                        log_info("Closing browser...")
            
            return success
            
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


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  LAZADA POKEMON STORE SNIPER")
    print("="*60)
    print("\n⚠️  DISCLAIMER:")
    print("This bot is for EDUCATIONAL purposes only!")
    print("Using automation may violate Lazada's Terms of Service.")
    print("Use at your own risk!\n")
    print("="*60 + "\n")
    
    # ============================================
    # CONFIGURATION
    # ============================================
    
    # Pokemon Store URL
    STORE_URL = "https://www.lazada.sg/shop/pokemon-store-online-singapore"
    
    # Product keywords - ANY of these trigger a match
    # The bot will detect products containing these terms
    PRODUCT_KEYWORDS = [
        "tcg",                          # Trading Card Game
        "trading card",                 # Full phrase
        "booster",                      # Booster packs
        "elite trainer",                # Elite Trainer Box
        "collection box",               # Collection boxes
        "pokemon center original",      # Pokemon Center exclusives
    ]
    
    # When to start monitoring
    # Options:
    # 1. Start immediately:
    LISTING_TIME = datetime.now()
    
    # 2. Start in 5 minutes (for testing):
    # LISTING_TIME = datetime.now() + timedelta(minutes=5)
    
    # 3. Start at specific time:
    # LISTING_TIME = datetime(2024, 12, 25, 12, 0, 0)  # Dec 25, 12:00 PM
    
    # How often to refresh store page (seconds)
    CHECK_INTERVAL = 3.0  # Check every 3 seconds
    
    # Safety settings
    AUTO_PURCHASE = False  # Set to True to auto-complete purchase (DANGEROUS!)
    HEADLESS = False       # Set to True to hide browser
    
    # ============================================
    # END CONFIGURATION
    # ============================================
    
    # Confirm auto-purchase
    if AUTO_PURCHASE:
        log_warning("⚠️  AUTO_PURCHASE IS ENABLED!")
        log_warning("⚠️  This will automatically complete purchases!")
        response = input("Are you sure? Type 'YES' to continue: ")
        if response != "YES":
            log_info("Cancelled by user")
            sys.exit(0)
    
    # Create and run sniper
    sniper = LazadaStoreSniper(
        store_url=STORE_URL,
        product_keywords=PRODUCT_KEYWORDS,
        listing_time=LISTING_TIME,
        auto_purchase=AUTO_PURCHASE,
        headless=HEADLESS,
        check_interval=CHECK_INTERVAL
    )
    
    try:
        success = sniper.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log_warning("\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()

