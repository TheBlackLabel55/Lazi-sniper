"""
Tutorial 3: Python Essentials
==============================

This tutorial covers Python concepts you need for the sniper bot:
1. Variables and data types
2. Functions
3. Loops and conditionals
4. Time and datetime
5. Error handling

Note: This is a quick refresher. If completely new to Python,
consider taking a full Python course first.
"""

import time
from datetime import datetime, timedelta


def lesson_1_variables_and_types():
    """
    Lesson 1: Variables and Data Types
    """
    print("\n" + "="*60)
    print("LESSON 1: VARIABLES AND DATA TYPES")
    print("="*60)
    
    # Strings (text)
    product_url = "https://www.lazada.sg/products/abc123"
    print(f"\n📝 String: {product_url}")
    
    # Numbers
    max_price = 999.99
    quantity = 1
    print(f"💰 Float: ${max_price}")
    print(f"🔢 Integer: {quantity}")
    
    # Booleans (True/False)
    auto_purchase = False
    is_available = True
    print(f"✅ Boolean: auto_purchase = {auto_purchase}")
    
    # Lists (arrays)
    product_urls = [
        "https://lazada.sg/product1",
        "https://lazada.sg/product2",
    ]
    print(f"\n📋 List: {len(product_urls)} products")
    
    # Dictionaries (key-value pairs)
    config = {
        "headless": False,
        "timeout": 30000,
        "retry_count": 3
    }
    print(f"\n⚙️  Dictionary: {config}")
    print(f"   Access value: config['timeout'] = {config['timeout']}")
    
    print("\n💡 Why this matters for sniper bot:")
    print("  - Store product URLs (strings)")
    print("  - Store prices and quantities (numbers)")
    print("  - Track if product is available (boolean)")
    print("  - Store multiple products to snipe (lists)")
    print("  - Store configuration settings (dictionaries)")


def lesson_2_functions():
    """
    Lesson 2: Functions - Reusable blocks of code
    """
    print("\n" + "="*60)
    print("LESSON 2: FUNCTIONS")
    print("="*60)
    
    # Define a function
    def check_product_price(price, max_price):
        """Check if price is within budget"""
        if price <= max_price:
            return True
        return False
    
    # Use the function
    product_price = 899.99
    max_budget = 1000.00
    
    if check_product_price(product_price, max_budget):
        print(f"\n✅ ${product_price} is within budget of ${max_budget}")
    else:
        print(f"\n❌ ${product_price} exceeds budget of ${max_budget}")
    
    print("\n💡 Functions help organize code:")
    print("  - check_product_availability()")
    print("  - add_to_cart()")
    print("  - proceed_to_checkout()")
    print("  - complete_purchase()")
    
    print("\n📝 Function structure:")
    print("""
def function_name(parameter1, parameter2):
    # Do something
    result = parameter1 + parameter2
    return result
    """)


def lesson_3_loops_and_conditionals():
    """
    Lesson 3: Loops and Conditionals
    """
    print("\n" + "="*60)
    print("LESSON 3: LOOPS AND CONDITIONALS")
    print("="*60)
    
    # If-else statements
    print("\n1️⃣  IF-ELSE STATEMENTS:")
    product_available = True
    
    if product_available:
        print("  ✅ Product is available - attempt to purchase!")
    else:
        print("  ⏳ Product not available yet - keep waiting...")
    
    # While loops
    print("\n2️⃣  WHILE LOOPS:")
    print("  Used for: Continuously checking until condition met")
    print("\n  Example:")
    print("""
    attempts = 0
    max_attempts = 5
    
    while attempts < max_attempts:
        if try_add_to_cart():
            print("Success!")
            break
        attempts += 1
        time.sleep(0.1)
    """)
    
    # For loops
    print("\n3️⃣  FOR LOOPS:")
    print("  Used for: Iterating through lists")
    
    product_urls = [
        "https://lazada.sg/product1",
        "https://lazada.sg/product2",
        "https://lazada.sg/product3",
    ]
    
    print(f"\n  Checking {len(product_urls)} products:")
    for i, url in enumerate(product_urls, 1):
        print(f"    {i}. {url}")
    
    print("\n💡 For sniper bot:")
    print("  - IF: Check if product is available")
    print("  - WHILE: Keep checking until available")
    print("  - FOR: Snipe multiple products")


def lesson_4_time_and_datetime():
    """
    Lesson 4: Working with Time (CRITICAL for sniper bot!)
    """
    print("\n" + "="*60)
    print("LESSON 4: TIME AND DATETIME")
    print("="*60)
    
    # Current time
    now = datetime.now()
    print(f"\n🕐 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create specific time (listing time)
    listing_time = datetime(2024, 12, 25, 12, 0, 0)  # Christmas, 12:00 PM
    print(f"🎯 Listing time: {listing_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Calculate time difference
    time_until_listing = listing_time - now
    print(f"⏰ Time until listing: {time_until_listing}")
    
    # Wait until specific time
    print("\n💡 Waiting logic:")
    print("""
from datetime import datetime
import time

listing_time = datetime(2024, 12, 25, 12, 0, 0)

# Wait until listing time
while datetime.now() < listing_time:
    remaining = (listing_time - datetime.now()).total_seconds()
    print(f"Waiting... {remaining:.1f}s remaining")
    time.sleep(1)

print("GO! Start sniping!")
    """)
    
    # Precise timing
    print("\n⚡ Precise timing (important!):")
    print("  - Use time.sleep(0.1) for 100ms intervals")
    print("  - Use time.sleep(0.05) for 50ms intervals")
    print("  - Faster = better chance to snipe")
    
    # Demonstration
    print("\n🎬 Demo: Checking every 0.5 seconds for 2 seconds")
    start = time.time()
    checks = 0
    
    while time.time() - start < 2:
        checks += 1
        print(f"  Check #{checks}")
        time.sleep(0.5)
    
    print(f"✅ Performed {checks} checks in 2 seconds")


def lesson_5_error_handling():
    """
    Lesson 5: Error Handling (try-except)
    """
    print("\n" + "="*60)
    print("LESSON 5: ERROR HANDLING")
    print("="*60)
    
    print("\n💡 Why error handling matters:")
    print("  - Network issues")
    print("  - Element not found")
    print("  - Timeout errors")
    print("  - Unexpected popups")
    
    print("\n✅ Good code handles errors gracefully:")
    print("""
try:
    # Try to add to cart
    button = page.locator('.add-to-cart-btn')
    button.click()
    print("✅ Added to cart!")
    
except TimeoutError:
    print("⏱️  Timeout - button didn't appear")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    # Save screenshot for debugging
    page.screenshot(path='error.png')
    
finally:
    # This always runs
    print("🏁 Attempt finished")
    """)
    
    # Practical example
    print("\n🎬 Demo: Safe division")
    
    def safe_divide(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print("❌ Cannot divide by zero!")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    print(f"  10 / 2 = {safe_divide(10, 2)}")
    print(f"  10 / 0 = {safe_divide(10, 0)}")


def practical_sniper_example():
    """
    Putting it all together
    """
    print("\n" + "="*60)
    print("🎯 PUTTING IT ALL TOGETHER")
    print("="*60)
    
    print("\n📝 Complete sniper bot structure:")
    print("""
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

def snipe_product(product_url, listing_time):
    '''
    Main sniper function combining all concepts
    '''
    # Variables
    max_attempts = 100
    check_interval = 0.05
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Load product page
            print(f"📍 Loading: {product_url}")
            page.goto(product_url)
            
            # Wait until listing time
            while datetime.now() < listing_time:
                remaining = (listing_time - datetime.now()).total_seconds()
                print(f"⏰ Waiting... {remaining:.1f}s")
                time.sleep(1)
            
            # Start sniping!
            print("🎯 SNIPING NOW!")
            
            attempts = 0
            while attempts < max_attempts:
                try:
                    # Check if Add to Cart button exists
                    button = page.locator('.add-to-cart-btn')
                    
                    if button.count() > 0:
                        # FOUND IT! Click immediately!
                        button.first.click(force=True)
                        print("✅ SUCCESS! Added to cart!")
                        return True
                    
                except Exception as e:
                    # Ignore errors, keep trying
                    pass
                
                attempts += 1
                time.sleep(check_interval)
            
            print("❌ Max attempts reached")
            return False
            
        except Exception as e:
            print(f"❌ Critical error: {e}")
            page.screenshot(path='error.png')
            return False
            
        finally:
            browser.close()

# Usage
listing_time = datetime(2024, 12, 25, 12, 0, 0)
success = snipe_product(
    "https://www.lazada.sg/products/...",
    listing_time
)
    """)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TUTORIAL 3: PYTHON ESSENTIALS")
    print("="*60)
    
    input("\n👉 Press Enter to start...")
    
    lesson_1_variables_and_types()
    input("\n👉 Press Enter for next lesson...")
    
    lesson_2_functions()
    input("\n👉 Press Enter for next lesson...")
    
    lesson_3_loops_and_conditionals()
    input("\n👉 Press Enter for next lesson...")
    
    lesson_4_time_and_datetime()
    input("\n👉 Press Enter for next lesson...")
    
    lesson_5_error_handling()
    input("\n👉 Press Enter to see complete example...")
    
    practical_sniper_example()
    
    print("\n" + "="*60)
    print("🎉 AWESOME! Tutorial 3 Complete!")
    print("="*60)
    print("\n🎓 What you learned:")
    print("  ✓ Variables and data types")
    print("  ✓ Functions")
    print("  ✓ Loops and conditionals")
    print("  ✓ Time and datetime")
    print("  ✓ Error handling")
    print("  ✓ Complete sniper structure")
    print("\n📚 Next: Run 04_network_analysis.py")
    print("   python learning/04_network_analysis.py")
    print("\n" + "="*60)

