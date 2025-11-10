"""
Tutorial 2: Web Automation Basics
==================================

This tutorial teaches you how to:
1. Control a browser with Playwright
2. Click buttons automatically
3. Fill out forms
4. Navigate between pages
5. Wait for elements to appear

This is the CORE skill you need for the sniper bot!
"""

from playwright.sync_api import sync_playwright
import time


def tutorial_2_basic_automation():
    """
    Part 1: Basic browser automation
    """
    print("\n" + "="*60)
    print("TUTORIAL 2: WEB AUTOMATION")
    print("="*60)
    print("\n📚 What you'll learn:")
    print("  - Control a browser with code")
    print("  - Click buttons automatically")
    print("  - Fill forms")
    print("  - Wait for elements")
    print("\n" + "="*60)
    
    input("\n👉 Press Enter to start automation demo...")
    
    with sync_playwright() as p:
        # Launch browser
        print("\n🌐 Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=500)  # slow_mo for visibility
        page = browser.new_page()
        
        # Part 1: Navigation
        print("\n" + "="*60)
        print("PART 1: NAVIGATION")
        print("="*60)
        print("\n📍 Navigating to Lazada...")
        page.goto("https://www.lazada.sg")
        print("✅ Navigated successfully!")
        
        time.sleep(2)
        
        # Part 2: Finding and clicking elements
        print("\n" + "="*60)
        print("PART 2: CLICKING ELEMENTS")
        print("="*60)
        print("\n🔍 Looking for search box...")
        
        try:
            # Find search box
            search_box = page.locator('input[placeholder*="Search"]').first
            print("✅ Found search box!")
            
            # Type in search box
            print("\n⌨️  Typing 'iPhone'...")
            search_box.fill("iPhone")
            print("✅ Typed successfully!")
            
            time.sleep(1)
            
            # Find and click search button
            print("\n🔍 Looking for search button...")
            search_button = page.locator('button.search-box__button--1oH7').first
            print("✅ Found search button!")
            
            print("\n🖱️  Clicking search button...")
            search_button.click()
            print("✅ Clicked successfully!")
            
            # Wait for results to load
            print("\n⏳ Waiting for search results...")
            page.wait_for_load_state("networkidle")
            print("✅ Search results loaded!")
            
        except Exception as e:
            print(f"⚠️  Note: {e}")
            print("(Lazada's selectors might have changed - this is common!)")
        
        time.sleep(2)
        
        # Part 3: Waiting strategies
        print("\n" + "="*60)
        print("PART 3: WAITING STRATEGIES")
        print("="*60)
        print("\n💡 Why waiting is important:")
        print("  - Web pages load asynchronously")
        print("  - Elements appear after JavaScript runs")
        print("  - Network requests take time")
        print("\n🎯 Different wait methods:")
        print("\n  1. time.sleep(seconds)")
        print("     - Simple, but not smart")
        print("     - Always waits the full time")
        print("\n  2. page.wait_for_selector(selector)")
        print("     - Waits for specific element to appear")
        print("     - Smart - continues as soon as element appears")
        print("\n  3. page.wait_for_load_state('networkidle')")
        print("     - Waits for network to be idle")
        print("     - Good for waiting for page to finish loading")
        print("\n  4. locator.wait_for(state='visible')")
        print("     - Waits for element to be visible")
        print("     - Best for buttons that need to be clickable")
        
        input("\n👉 Press Enter to continue to Part 4...")
        
        # Part 4: Error handling
        print("\n" + "="*60)
        print("PART 4: ERROR HANDLING")
        print("="*60)
        print("\n💡 Things can go wrong:")
        print("  - Element not found")
        print("  - Page loads slowly")
        print("  - Selectors change")
        print("\n✅ Good practice: Use try-except blocks")
        print("\nExample code:")
        print("""
try:
    button = page.locator('.add-to-cart-btn')
    button.click()
    print('✅ Success!')
except Exception as e:
    print(f'❌ Error: {e}')
    # Take screenshot for debugging
    page.screenshot(path='error.png')
        """)
        
        input("\n👉 Press Enter to see practical examples...")
        
        # Part 5: Practical examples for sniper bot
        print("\n" + "="*60)
        print("PART 5: SNIPER BOT TECHNIQUES")
        print("="*60)
        print("\n🎯 Key techniques you'll use:")
        print("\n1. FAST ELEMENT CHECKING:")
        print("   while not product_available:")
        print("       check_if_add_to_cart_exists()")
        print("       time.sleep(0.1)  # Check every 100ms")
        print("\n2. INSTANT CLICKING:")
        print("   button.click(force=True)  # Don't wait for animations")
        print("\n3. PRE-LOADING:")
        print("   # Load product page BEFORE listing time")
        print("   page.goto(product_url)")
        print("   # Then just keep checking for button")
        print("\n4. KEEP SESSION ALIVE:")
        print("   # Stay logged in")
        print("   # Keep cookies")
        print("   # Browser stays open")
        
        input("\n👉 Press Enter to close browser...")
        browser.close()
    
    print("\n✅ Tutorial 2 Complete!")


def demo_code_example():
    """
    Show example code structure
    """
    print("\n" + "="*60)
    print("📝 EXAMPLE: SIMPLE SNIPER LOGIC")
    print("="*60)
    print("""
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def snipe_product(product_url, listing_time):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Pre-load the product page
        print("🔄 Loading product page...")
        page.goto(product_url)
        
        # Wait until listing time
        while datetime.now() < listing_time:
            time.sleep(0.1)
        
        # Start checking for Add to Cart button
        print("🎯 Sniping started!")
        while True:
            try:
                # Look for Add to Cart button
                button = page.locator('.add-to-cart-btn')
                
                if button.count() > 0:
                    # Found it! Click immediately!
                    button.first.click(force=True)
                    print("✅ Added to cart!")
                    break
                    
            except:
                pass
            
            time.sleep(0.05)  # Check every 50ms
        
        browser.close()

# Usage:
# snipe_product(
#     "https://www.lazada.sg/products/...",
#     datetime(2024, 1, 1, 12, 0, 0)
# )
    """)
    print("="*60)


if __name__ == "__main__":
    tutorial_2_basic_automation()
    demo_code_example()
    
    print("\n" + "="*60)
    print("🎉 EXCELLENT! You completed Tutorial 2!")
    print("="*60)
    print("\n🎓 What you learned:")
    print("  ✓ Navigate to pages")
    print("  ✓ Find and click elements")
    print("  ✓ Fill forms")
    print("  ✓ Wait for elements")
    print("  ✓ Handle errors")
    print("  ✓ Sniper bot logic structure")
    print("\n📚 Next: Run 03_python_essentials.py")
    print("   python learning/03_python_essentials.py")
    print("\n" + "="*60)


