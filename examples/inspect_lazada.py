"""
Lazada Inspector Tool
=====================

This script helps you inspect Lazada product pages and find the correct selectors.
Use this to:
1. Test if your product URL works
2. Find the correct button selectors
3. See product information
4. Practice before running the actual sniper

Usage:
    python examples/inspect_lazada.py
"""

from playwright.sync_api import sync_playwright
import time


def inspect_product_page(product_url: str):
    """
    Open and inspect a Lazada product page.
    
    Args:
        product_url: URL of the product to inspect
    """
    print("\n" + "="*60)
    print("LAZADA PRODUCT INSPECTOR")
    print("="*60)
    print(f"\n📍 URL: {product_url}\n")
    
    with sync_playwright() as p:
        # Launch browser
        print("🌐 Opening browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to product
        print("📄 Loading product page...")
        page.goto(product_url)
        page.wait_for_load_state("domcontentloaded")
        
        print("✅ Page loaded!\n")
        print("="*60)
        print("🔍 INSPECTING ELEMENTS...")
        print("="*60)
        
        # Try to find Add to Cart button
        print("\n1️⃣  Searching for 'Add to Cart' button...")
        add_to_cart_selectors = [
            ('button.add-to-cart-buy-now-btn', 'Class: add-to-cart-buy-now-btn'),
            ('button[class*="add-to-cart"]', 'Class contains: add-to-cart'),
            ('button:has-text("Add to Cart")', 'Text: Add to Cart'),
            ('.pdp-button-add-to-cart', 'Class: pdp-button-add-to-cart'),
        ]
        
        found_add_to_cart = False
        for selector, description in add_to_cart_selectors:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    print(f"   ✅ FOUND: {description}")
                    print(f"      Selector: {selector}")
                    is_disabled = button.get_attribute('disabled')
                    if is_disabled:
                        print(f"      Status: DISABLED (product may not be available)")
                    else:
                        print(f"      Status: ENABLED (can be clicked)")
                    found_add_to_cart = True
                    break
            except:
                pass
        
        if not found_add_to_cart:
            print("   ❌ Add to Cart button not found")
            print("   💡 Product might be out of stock or page structure changed")
        
        # Try to find Buy Now button
        print("\n2️⃣  Searching for 'Buy Now' button...")
        buy_now_selectors = [
            ('button.buy-now-btn', 'Class: buy-now-btn'),
            ('button[class*="buy-now"]', 'Class contains: buy-now'),
            ('button:has-text("Buy Now")', 'Text: Buy Now'),
        ]
        
        found_buy_now = False
        for selector, description in buy_now_selectors:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    print(f"   ✅ FOUND: {description}")
                    print(f"      Selector: {selector}")
                    found_buy_now = True
                    break
            except:
                pass
        
        if not found_buy_now:
            print("   ❌ Buy Now button not found")
        
        # Try to find product title
        print("\n3️⃣  Searching for product title...")
        title_selectors = [
            'h1.pdp-mod-product-badge-title',
            '.pdp-product-title',
            'h1[class*="title"]',
        ]
        
        for selector in title_selectors:
            try:
                title = page.locator(selector).first
                if title.count() > 0:
                    title_text = title.inner_text()
                    print(f"   ✅ FOUND: {title_text[:60]}...")
                    break
            except:
                pass
        
        # Try to find price
        print("\n4️⃣  Searching for price...")
        price_selectors = [
            '.pdp-price',
            'span[class*="price"]',
            '.price-current',
        ]
        
        for selector in price_selectors:
            try:
                price = page.locator(selector).first
                if price.count() > 0:
                    price_text = price.inner_text()
                    print(f"   ✅ FOUND: {price_text}")
                    break
            except:
                pass
        
        # Check for out of stock message
        print("\n5️⃣  Checking stock status...")
        stock_selectors = [
            'text=Out of Stock',
            'text=Currently Unavailable',
            'text=Sold Out',
        ]
        
        is_out_of_stock = False
        for selector in stock_selectors:
            try:
                if page.locator(selector).count() > 0:
                    print(f"   ⚠️  FOUND: {selector.replace('text=', '')}")
                    is_out_of_stock = True
                    break
            except:
                pass
        
        if not is_out_of_stock:
            print("   ✅ No 'Out of Stock' message found")
        
        # Summary
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        print(f"Add to Cart Button: {'✅ Found' if found_add_to_cart else '❌ Not found'}")
        print(f"Buy Now Button: {'✅ Found' if found_buy_now else '❌ Not found'}")
        print(f"Stock Status: {'❌ Out of Stock' if is_out_of_stock else '✅ In Stock'}")
        print("="*60)
        
        if found_add_to_cart or found_buy_now:
            print("\n✅ Product page looks good for sniping!")
        else:
            print("\n⚠️  WARNING: Could not find purchase buttons!")
            print("   This product may not work with the sniper bot.")
            print("   Reasons:")
            print("   - Product might be out of stock")
            print("   - Page structure might be different")
            print("   - Selectors might need updating")
        
        print("\n" + "="*60)
        print("🎓 LEARNING EXERCISE")
        print("="*60)
        print("\nThe browser will stay open. Now YOU try:")
        print("1. Right-click on the 'Add to Cart' button")
        print("2. Select 'Inspect' or 'Inspect Element'")
        print("3. Look at the HTML in DevTools")
        print("4. Find the class name")
        print("5. That's the selector you'd use!")
        print("\nPress Ctrl+C when done...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Closing browser...")
        
        browser.close()


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  LAZADA PRODUCT INSPECTOR")
    print("="*60)
    print("\nThis tool helps you inspect Lazada product pages")
    print("and find the correct selectors for your sniper bot.\n")
    
    # Get product URL from user
    print("Please enter a Lazada product URL:")
    print("Example: https://www.lazada.sg/products/...")
    print()
    
    product_url = input("Product URL: ").strip()
    
    if not product_url:
        print("❌ No URL provided!")
        return
    
    if 'lazada.sg' not in product_url.lower():
        print("⚠️  Warning: This doesn't look like a Lazada Singapore URL")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Inspect the product
    inspect_product_page(product_url)


if __name__ == "__main__":
    main()

