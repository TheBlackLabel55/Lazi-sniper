"""
Timing Test Tool
================

This script tests timing precision and helps you understand:
1. How fast the bot can check for product availability
2. Network latency to Lazada
3. How timing works for sniping

Usage:
    python examples/test_timing.py
"""

import time
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright


def test_check_speed():
    """Test how many checks we can perform per second"""
    print("\n" + "="*60)
    print("TEST 1: Check Speed")
    print("="*60)
    print("\nTesting how fast we can check for product availability...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Load a product page
        print("\n📄 Loading Lazada homepage...")
        page.goto("https://www.lazada.sg")
        
        # Test different check intervals
        intervals = [0.01, 0.05, 0.1, 0.5]
        
        for interval in intervals:
            print(f"\n🔄 Testing with {interval}s interval...")
            checks = 0
            start = time.time()
            test_duration = 2  # Test for 2 seconds
            
            while time.time() - start < test_duration:
                # Simulate checking for element
                try:
                    page.locator('body').count()
                    checks += 1
                except:
                    pass
                time.sleep(interval)
            
            elapsed = time.time() - start
            checks_per_sec = checks / elapsed
            print(f"   ✅ {checks} checks in {elapsed:.2f}s")
            print(f"   ⚡ {checks_per_sec:.1f} checks per second")
            print(f"   💡 Can detect availability within {interval}s")
        
        browser.close()
    
    print("\n📊 ANALYSIS:")
    print("  - Lower interval = more checks = faster detection")
    print("  - But also uses more CPU")
    print("  - 0.05s (50ms) is a good balance")
    print("  - Can detect product within 50ms of availability")


def test_network_latency():
    """Test network latency to Lazada"""
    print("\n" + "="*60)
    print("TEST 2: Network Latency")
    print("="*60)
    print("\nMeasuring network latency to Lazada.sg...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        latencies = []
        
        for i in range(5):
            print(f"\n📡 Test #{i+1}...")
            start = time.time()
            page.goto("https://www.lazada.sg/favicon.ico")
            latency = (time.time() - start) * 1000  # Convert to ms
            latencies.append(latency)
            print(f"   ⏱️  {latency:.0f}ms")
            time.sleep(0.5)
        
        browser.close()
        
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        
        print("\n📊 STATISTICS:")
        print(f"  Average: {avg_latency:.0f}ms")
        print(f"  Best: {min_latency:.0f}ms")
        print(f"  Worst: {max_latency:.0f}ms")
        
        print("\n💡 WHAT THIS MEANS:")
        print(f"  - Your clicks take ~{avg_latency:.0f}ms to reach Lazada")
        print(f"  - You should start monitoring {avg_latency/1000:.2f}s before listing time")
        print(f"  - Faster internet = lower latency = better chance")


def test_button_click_speed():
    """Test how fast we can click a button"""
    print("\n" + "="*60)
    print("TEST 3: Button Click Speed")
    print("="*60)
    print("\nTesting how fast we can click a button...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Load Lazada
        print("\n📄 Loading Lazada...")
        page.goto("https://www.lazada.sg")
        page.wait_for_load_state("domcontentloaded")
        
        # Try to find and click search button
        print("\n🔍 Finding search box...")
        
        try:
            search_box = page.locator('input[placeholder*="Search"]').first
            
            if search_box.count() > 0:
                # Test normal click
                print("\n⏱️  Testing NORMAL click...")
                search_box.fill("test")
                start = time.time()
                search_button = page.locator('button.search-box__button--1oH7').first
                search_button.click()
                normal_time = (time.time() - start) * 1000
                print(f"   Normal click: {normal_time:.0f}ms")
                
                time.sleep(2)
                page.goto("https://www.lazada.sg")
                
                # Test force click
                print("\n⏱️  Testing FORCE click (bot mode)...")
                search_box = page.locator('input[placeholder*="Search"]').first
                search_box.fill("test")
                start = time.time()
                search_button = page.locator('button.search-box__button--1oH7').first
                search_button.click(force=True)
                force_time = (time.time() - start) * 1000
                print(f"   Force click: {force_time:.0f}ms")
                
                print("\n📊 COMPARISON:")
                print(f"  Normal: {normal_time:.0f}ms")
                print(f"  Force: {force_time:.0f}ms")
                print(f"  Speedup: {normal_time/force_time:.1f}x faster")
                
                print("\n💡 INSIGHT:")
                print("  Force click skips visibility/animation checks")
                print("  This is what the sniper bot uses for speed!")
                
        except Exception as e:
            print(f"⚠️  Could not perform test: {e}")
        
        browser.close()


def test_timing_precision():
    """Test timing precision"""
    print("\n" + "="*60)
    print("TEST 4: Timing Precision")
    print("="*60)
    print("\nTesting ability to hit exact timing...")
    
    # Set target 5 seconds in future
    target_time = datetime.now() + timedelta(seconds=5)
    print(f"\n🎯 Target time: {target_time.strftime('%H:%M:%S.%f')[:-3]}")
    print("⏰ Waiting for target time...\n")
    
    # Wait until target
    while datetime.now() < target_time:
        remaining = (target_time - datetime.now()).total_seconds()
        print(f"   {remaining:.3f}s remaining", end='\r')
        
        if remaining < 0.1:
            time.sleep(0.001)  # Very precise at the end
        elif remaining < 1:
            time.sleep(0.01)
        else:
            time.sleep(0.1)
    
    actual_time = datetime.now()
    difference = (actual_time - target_time).total_seconds() * 1000
    
    print(f"\n\n✅ Actual time: {actual_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"📊 Difference: {difference:.0f}ms {'early' if difference < 0 else 'late'}")
    
    print("\n💡 ANALYSIS:")
    if abs(difference) < 50:
        print("  ✅ Excellent timing precision!")
    elif abs(difference) < 100:
        print("  ✅ Good timing precision")
    else:
        print("  ⚠️  Timing could be better")
    print("  The sniper bot uses similar logic for precision timing")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  TIMING TEST TOOL")
    print("="*60)
    print("\nThis tool helps you understand timing and performance")
    print("factors that affect sniper bot success.\n")
    
    print("Tests to run:")
    print("1. Check Speed - How fast can we detect availability?")
    print("2. Network Latency - How fast is your connection?")
    print("3. Button Click Speed - Normal vs Force click")
    print("4. Timing Precision - Can we hit exact times?")
    print()
    
    response = input("Run all tests? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled")
        return
    
    try:
        # Run tests
        test_check_speed()
        input("\n👉 Press Enter to continue to next test...")
        
        test_network_latency()
        input("\n👉 Press Enter to continue to next test...")
        
        test_button_click_speed()
        input("\n👉 Press Enter to continue to next test...")
        
        test_timing_precision()
        
        # Final summary
        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETE!")
        print("="*60)
        print("\n🎓 KEY TAKEAWAYS:")
        print("  1. Bot can check 10-20 times per second (0.05s interval)")
        print("  2. Network latency affects success (lower is better)")
        print("  3. Force clicks are faster than normal clicks")
        print("  4. Timing precision is possible within ~50ms")
        print("\n💡 For best results:")
        print("  - Use fast, stable internet connection")
        print("  - Start monitoring few seconds before listing")
        print("  - Use force clicks (bot does this automatically)")
        print("  - Be logged in and payment info saved beforehand")
        print("\n" + "="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during tests: {e}")


if __name__ == "__main__":
    main()

