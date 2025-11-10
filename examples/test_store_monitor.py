"""
Test Store Monitor
==================

This script tests the store monitor on the Pokemon store.
Use this to verify it can find products before running the full sniper.

Usage:
    python examples/test_store_monitor.py
"""

from playwright.sync_api import sync_playwright
from bot.store_monitor import StoreMonitor


def test_pokemon_store():
    """Test monitoring the Pokemon store"""
    
    print("\n" + "="*60)
    print("POKEMON STORE MONITOR TEST")
    print("="*60)
    print("\nThis will scan the Pokemon store and show matching products.")
    print("Use this to verify your keywords work!\n")
    
    # Configuration
    STORE_URL = "https://www.lazada.sg/shop/pokemon-store-online-singapore"
    
    KEYWORDS = [
        "tcg",
        "trading card",
        "booster",
        "elite trainer",
        "collection box",
        "pokemon center original",
    ]
    
    print("Store:", STORE_URL)
    print("Keywords:", KEYWORDS)
    print("\n" + "="*60)
    
    input("\n👉 Press Enter to start test...")
    
    with sync_playwright() as p:
        print("\n🌐 Opening browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Create monitor
        monitor = StoreMonitor(
            page=page,
            store_url=STORE_URL,
            product_keywords=KEYWORDS,
            check_interval=2.0
        )
        
        # Load store
        print("\n📄 Loading Pokemon store...")
        monitor.load_store_page()
        
        # Scan current products
        print("\n🔍 Scanning current products...")
        matching = monitor.scan_current_products()
        
        print("\n" + "="*60)
        print(f"📊 RESULTS: Found {len(matching)} matching products")
        print("="*60)
        
        if matching:
            for i, product in enumerate(matching, 1):
                print(f"\n{i}. {product['title']}")
                print(f"   URL: {product['url']}")
        else:
            print("\n⚠️  No matching products found!")
            print("\nPossible reasons:")
            print("  - Keywords don't match current products")
            print("  - Store has no TCG products listed")
            print("  - Page structure changed")
            print("\n💡 Try adjusting keywords in main_store_sniper.py")
        
        print("\n" + "="*60)
        print("TEST COMPLETE")
        print("="*60)
        print("\nThe browser will stay open so you can:")
        print("1. Inspect the page")
        print("2. See what products are available")
        print("3. Right-click products to inspect their HTML")
        print("\nPress Ctrl+C when done...")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n\n👋 Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    test_pokemon_store()

