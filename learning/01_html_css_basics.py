"""
Tutorial 1: HTML & CSS Basics
==============================

This tutorial teaches you how to:
1. Understand web page structure (HTML)
2. Identify elements using CSS selectors
3. Use browser DevTools to inspect elements
4. Find the right selectors for automation

Run this script and follow along!
"""

from playwright.sync_api import sync_playwright
import time


def tutorial_1_open_and_inspect():
    """
    Part 1: Opening a webpage and understanding its structure
    """
    print("\n" + "="*60)
    print("TUTORIAL 1: HTML & CSS BASICS")
    print("="*60)
    print("\n📚 What you'll learn:")
    print("  - How to open a webpage with code")
    print("  - How to inspect elements")
    print("  - How to find CSS selectors")
    print("\n" + "="*60)
    
    input("\n👉 Press Enter to open Lazada Singapore...")
    
    with sync_playwright() as p:
        # Launch a visible browser (headless=False means you can see it)
        print("\n🌐 Opening browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to Lazada Singapore
        print("📍 Navigating to Lazada.sg...")
        page.goto("https://www.lazada.sg")
        
        print("\n✅ Browser opened successfully!")
        print("\n" + "="*60)
        print("🔍 INSPECT ELEMENTS EXERCISE")
        print("="*60)
        print("\nNow, let's learn to inspect elements:")
        print("\n1. In the browser window that just opened:")
        print("   - Right-click on the SEARCH BOX")
        print("   - Select 'Inspect' or 'Inspect Element'")
        print("\n2. The DevTools panel will open showing the HTML")
        print("\n3. Look for something like:")
        print('   <input class="search-box__input" ...>')
        print("\n4. The 'class' is what we use to target elements!")
        print("   - In this case: .search-box__input")
        print("   - The dot (.) means it's a class selector")
        print("\n" + "="*60)
        
        input("\n👉 Take your time to explore. Press Enter when ready to continue...")
        
        # Demonstrate finding an element
        print("\n🎯 Now I'll show you how code finds elements...")
        print("\nLet's find the search box using CSS selector:")
        
        try:
            # Find the search input
            search_box = page.locator('input[placeholder*="Search"]')
            
            if search_box.count() > 0:
                print("✅ Found the search box!")
                print("\nNow I'll type something in it...")
                search_box.first.fill("laptop")
                print("✅ Typed 'laptop' in the search box!")
                
                time.sleep(2)
                
                print("\nNow I'll clear it...")
                search_box.first.fill("")
                print("✅ Cleared the search box!")
            else:
                print("❌ Couldn't find search box (Lazada might have changed their layout)")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            print("(Lazada's layout might have changed)")
        
        print("\n" + "="*60)
        print("📝 KEY CONCEPTS:")
        print("="*60)
        print("\n1. CSS SELECTORS - How to target elements:")
        print("   .classname          - Targets by class")
        print("   #idname             - Targets by ID")
        print("   button              - Targets by tag name")
        print("   [attribute=value]   - Targets by attribute")
        print("\n2. Common patterns:")
        print("   .button.primary     - Element with both classes")
        print("   .parent .child      - Child inside parent")
        print("   button[type='submit'] - Button with type submit")
        print("\n3. For Lazada sniper, you'll need to find:")
        print("   ✓ Add to Cart button")
        print("   ✓ Buy Now button")
        print("   ✓ Checkout button")
        print("   ✓ Place Order button")
        print("\n" + "="*60)
        
        input("\n👉 Press Enter to close the browser and continue...")
        browser.close()
    
    print("\n✅ Tutorial 1 Complete!")
    print("\n🎓 What you learned:")
    print("  ✓ How to open a browser with code")
    print("  ✓ How to inspect elements using DevTools")
    print("  ✓ How to identify CSS selectors")
    print("  ✓ How to find and interact with elements")
    print("\n📚 Next: Run 02_web_automation.py to learn browser automation!")


def homework_exercise():
    """
    Homework: Practice finding selectors
    """
    print("\n" + "="*60)
    print("📝 HOMEWORK EXERCISE")
    print("="*60)
    print("\nYour task:")
    print("1. Open Lazada.sg in your browser")
    print("2. Go to ANY product page")
    print("3. Right-click and Inspect these elements:")
    print("   - Add to Cart button")
    print("   - Buy Now button (if available)")
    print("   - Product price")
    print("   - Product title")
    print("\n4. Write down the CSS selectors for each")
    print("5. Try to find patterns in the class names")
    print("\n💡 Tip: Look for unique classes like 'btn-buy', 'add-to-cart', etc.")
    print("\n" + "="*60)


if __name__ == "__main__":
    tutorial_1_open_and_inspect()
    homework_exercise()
    
    print("\n" + "="*60)
    print("🎉 GREAT JOB! You completed Tutorial 1!")
    print("="*60)
    print("\n📚 Continue to Tutorial 2:")
    print("   python learning/02_web_automation.py")
    print("\n" + "="*60)


