"""
Tutorial 4: Network Analysis
=============================

This tutorial teaches you how to:
1. Use browser DevTools Network tab
2. Understand API calls
3. Analyze how Lazada loads products
4. Find faster alternatives to browser automation

This is ADVANCED but can make your sniper MUCH faster!
"""

from playwright.sync_api import sync_playwright
import time
import json


def tutorial_4_network_basics():
    """
    Part 1: Understanding network requests
    """
    print("\n" + "="*60)
    print("TUTORIAL 4: NETWORK ANALYSIS")
    print("="*60)
    print("\n📚 What you'll learn:")
    print("  - How websites communicate with servers")
    print("  - Using DevTools Network tab")
    print("  - Finding API endpoints")
    print("  - Making requests faster")
    print("\n" + "="*60)
    
    print("\n💡 TWO APPROACHES TO SNIPING:")
    print("\n1. BROWSER AUTOMATION (What we've learned):")
    print("   ✓ Easier to understand")
    print("   ✓ Works like a real user")
    print("   ✗ Slower (must render full page)")
    print("   ✗ Uses more resources")
    print("\n2. API CALLS (Advanced):")
    print("   ✓ Much faster (milliseconds matter!)")
    print("   ✓ More efficient")
    print("   ✗ Harder to figure out")
    print("   ✗ May need authentication tokens")
    
    input("\n👉 Press Enter to learn about APIs...")


def demo_network_inspection():
    """
    Part 2: Inspecting network requests
    """
    print("\n" + "="*60)
    print("NETWORK INSPECTION DEMO")
    print("="*60)
    
    print("\n🎯 HANDS-ON EXERCISE:")
    print("\n1. I'll open Lazada with DevTools")
    print("2. Watch the Network tab")
    print("3. We'll see what requests are made")
    
    input("\n👉 Press Enter to open Lazada with Network monitoring...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Enable request tracking
        requests = []
        
        def log_request(request):
            requests.append({
                'url': request.url,
                'method': request.method,
                'type': request.resource_type
            })
        
        page.on("request", log_request)
        
        print("\n🌐 Opening Lazada and monitoring requests...")
        page.goto("https://www.lazada.sg")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        print(f"\n📊 Captured {len(requests)} network requests!")
        print("\n🔍 Request types breakdown:")
        
        # Analyze request types
        types = {}
        for req in requests:
            req_type = req['type']
            types[req_type] = types.get(req_type, 0) + 1
        
        for req_type, count in sorted(types.items()):
            print(f"   {req_type}: {count}")
        
        print("\n" + "="*60)
        print("📝 WHAT TO LOOK FOR IN NETWORK TAB:")
        print("="*60)
        print("\n1. Open Chrome DevTools (F12)")
        print("2. Go to Network tab")
        print("3. Navigate to a product page")
        print("4. Look for:")
        print("   - XHR/Fetch requests (these are API calls!)")
        print("   - Requests with 'api' in the URL")
        print("   - Requests with 'product' or 'item' in URL")
        print("   - POST requests to 'cart' or 'checkout'")
        print("\n5. Click on a request to see:")
        print("   - Request Headers (authentication, cookies)")
        print("   - Request Payload (data being sent)")
        print("   - Response (data coming back)")
        
        input("\n👉 Now YOU try! Open DevTools Network tab (F12) and explore...")
        input("👉 Press Enter when you're done exploring...")
        
        # Demo: Go to a search page
        print("\n🔍 Let's search for a product and watch the network...")
        search_box = page.locator('input[placeholder*="Search"]').first
        search_box.fill("laptop")
        
        # Clear previous requests
        requests.clear()
        
        # Click search
        search_button = page.locator('button.search-box__button--1oH7').first
        try:
            search_button.click()
            page.wait_for_load_state("networkidle")
            
            print(f"\n📊 Search generated {len(requests)} new requests")
            
            # Find API-like requests
            api_requests = [r for r in requests if 'api' in r['url'].lower() or r['type'] == 'fetch']
            
            if api_requests:
                print(f"\n🎯 Found {len(api_requests)} potential API requests:")
                for req in api_requests[:5]:  # Show first 5
                    print(f"   {req['method']} {req['url'][:80]}...")
        except:
            print("⚠️  Note: Selectors might have changed")
        
        input("\n👉 Press Enter to close browser...")
        browser.close()


def explain_api_approach():
    """
    Part 3: Explaining the API approach
    """
    print("\n" + "="*60)
    print("THE API APPROACH (Advanced)")
    print("="*60)
    
    print("\n🎯 How it works:")
    print("\n1. Find the API endpoint")
    print("   Example: https://api.lazada.sg/products/add-to-cart")
    print("\n2. Figure out what data to send")
    print("   Example: {product_id: '12345', quantity: 1}")
    print("\n3. Get authentication (cookies, tokens)")
    print("   From your logged-in browser session")
    print("\n4. Make direct HTTP request")
    print("   Using Python's 'requests' library")
    
    print("\n📝 Example code (simplified):")
    print("""
import requests

# Your session cookies from logged-in browser
cookies = {
    'session_id': 'your_session_id',
    't': 'your_token'
}

# The API endpoint (you found this in DevTools!)
url = 'https://api.lazada.sg/cart/add'

# The data to send
data = {
    'itemId': '12345678',
    'quantity': 1
}

# Make the request (MUCH faster than browser!)
response = requests.post(url, json=data, cookies=cookies)

if response.status_code == 200:
    print('✅ Added to cart via API!')
else:
    print(f'❌ Failed: {response.status_code}')
    """)
    
    print("\n⚡ SPEED COMPARISON:")
    print("   Browser automation: 1-3 seconds")
    print("   Direct API call:    50-200 milliseconds")
    print("   → API is 10-20x faster!")
    
    print("\n⚠️  CHALLENGES:")
    print("   - Finding the right API endpoint")
    print("   - Figuring out required parameters")
    print("   - Getting valid authentication")
    print("   - APIs can change without notice")
    print("   - More complex to implement")


def practical_recommendations():
    """
    Part 4: Practical recommendations
    """
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS FOR YOUR SNIPER BOT")
    print("="*60)
    
    print("\n🎯 START WITH: Browser Automation")
    print("   Why:")
    print("   ✓ Easier to learn and implement")
    print("   ✓ More reliable")
    print("   ✓ Easier to debug")
    print("   ✓ Still fast enough for most cases")
    
    print("\n🚀 UPGRADE TO: API Calls (if needed)")
    print("   When:")
    print("   ✓ You understand browser automation well")
    print("   ✓ You need every millisecond")
    print("   ✓ You're comfortable with network analysis")
    print("   ✓ You've successfully found the APIs")
    
    print("\n📊 HYBRID APPROACH (Best!):")
    print("   1. Use browser to stay logged in")
    print("   2. Pre-load product page")
    print("   3. Use API for add-to-cart (if found)")
    print("   4. Fall back to clicking if API fails")
    
    print("\n🛠️  TOOLS YOU'LL USE:")
    print("   - Chrome DevTools (F12) → Network tab")
    print("   - Playwright for browser control")
    print("   - requests library for API calls")
    print("   - json library for data handling")


def next_steps():
    """
    What to do next
    """
    print("\n" + "="*60)
    print("📚 WHAT YOU'VE LEARNED")
    print("="*60)
    
    print("\nTutorial 1: HTML & CSS")
    print("  ✓ Inspect elements")
    print("  ✓ Find CSS selectors")
    
    print("\nTutorial 2: Web Automation")
    print("  ✓ Control browser")
    print("  ✓ Click buttons")
    print("  ✓ Handle timing")
    
    print("\nTutorial 3: Python Essentials")
    print("  ✓ Variables and functions")
    print("  ✓ Loops and conditionals")
    print("  ✓ Time handling")
    print("  ✓ Error handling")
    
    print("\nTutorial 4: Network Analysis")
    print("  ✓ Understand network requests")
    print("  ✓ Use DevTools Network tab")
    print("  ✓ API vs Browser automation")
    
    print("\n" + "="*60)
    print("🎯 YOU'RE READY FOR PHASE 3!")
    print("="*60)
    
    print("\n📂 Next: Explore the bot/ folder")
    print("   - bot/monitor.py    - Product monitoring")
    print("   - bot/cart.py       - Add to cart logic")
    print("   - bot/checkout.py   - Checkout automation")
    print("   - main.py           - Put it all together")
    
    print("\n💡 PRACTICE FIRST:")
    print("   1. Run examples/inspect_lazada.py")
    print("   2. Run examples/test_timing.py")
    print("   3. Study each bot component")
    print("   4. Test with NON-CRITICAL products first!")


if __name__ == "__main__":
    tutorial_4_network_basics()
    demo_network_inspection()
    
    input("\n👉 Press Enter for API explanation...")
    explain_api_approach()
    
    input("\n👉 Press Enter for recommendations...")
    practical_recommendations()
    
    input("\n👉 Press Enter to see next steps...")
    next_steps()
    
    print("\n" + "="*60)
    print("🎉 CONGRATULATIONS! All Tutorials Complete!")
    print("="*60)
    print("\n🏆 You've completed Phase 2!")
    print("📚 You now understand the fundamentals!")
    print("🚀 Ready to build your sniper bot!")
    print("\n" + "="*60)

