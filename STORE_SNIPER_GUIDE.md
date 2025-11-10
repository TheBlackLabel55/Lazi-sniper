# Store Sniper Guide - Pokemon Edition

## 🎯 What This Does

Instead of monitoring a specific product page, this bot:
1. **Monitors the entire Pokemon store** on Lazada Singapore
2. **Watches for NEW products** matching your keywords
3. **Automatically clicks** on matching products when they appear
4. **Adds to cart** and proceeds to checkout

Perfect for when:
- Product isn't listed yet
- You don't have the direct URL
- You want to catch any new TCG products from a specific store

---

## 🚀 Quick Start

### Step 1: Test the Store Monitor

First, verify it can find products:

```bash
python examples/test_store_monitor.py
```

**What it does:**
- Opens the Pokemon store
- Scans all current products
- Shows which ones match your keywords
- Lets you verify the bot works

**Expected output:**
```
📊 RESULTS: Found X matching products

1. Pokemon TCG: Scarlet & Violet Booster Pack
   URL: https://www.lazada.sg/products/...

2. Pokemon Center Original Elite Trainer Box
   URL: https://www.lazada.sg/products/...
```

### Step 2: Configure Your Sniper

Edit `main_store_sniper.py` (lines 160-195):

**Already configured for you:**
```python
# Store URL
STORE_URL = "https://www.lazada.sg/shop/pokemon-store-online-singapore"

# Keywords (ANY of these trigger a match)
PRODUCT_KEYWORDS = [
    "tcg",                          # Trading Card Game
    "trading card",                 # Full phrase
    "booster",                      # Booster packs
    "elite trainer",                # Elite Trainer Box
    "collection box",               # Collection boxes
    "pokemon center original",      # Pokemon Center exclusives
]

# Start immediately
LISTING_TIME = datetime.now()

# Check every 3 seconds
CHECK_INTERVAL = 3.0
```

### Step 3: Run the Sniper

```bash
python main_store_sniper.py
```

**What happens:**
1. ✅ Opens browser
2. ✅ Loads Pokemon store
3. ✅ Scans existing products (marks as "seen")
4. ✅ Refreshes every 3 seconds
5. ✅ When NEW product appears with matching keywords:
   - 🎯 Instantly clicks on it
   - 🛒 Adds to cart
   - 💳 Goes to checkout
   - ⏸️ Waits for you to complete

---

## 🎮 How It Works

### Phase 1: Initial Scan
```
Loading Pokemon store...
Found 24 existing products
(These will be ignored - only NEW products trigger)
```

### Phase 2: Monitoring
```
Check #1 at 0.0s - No new matches yet...
🔄 Refreshing store page...
Check #2 at 3.0s - No new matches yet...
🔄 Refreshing store page...
Check #3 at 6.0s - No new matches yet...
```

### Phase 3: Detection
```
✨ FOUND MATCH!
Product: Pokemon TCG Elite Trainer Box - Scarlet & Violet
URL: https://www.lazada.sg/products/...

🎯 PRODUCT FOUND after 9.5s (4 checks)
```

### Phase 4: Sniping
```
🎯 SNIPING PRODUCT
Loading product page...
Product is available!
Adding to cart...
Clicked Add to Cart in 150ms!
Navigating to cart...
Proceeding to checkout...
Ready for checkout!
```

---

## ⚙️ Configuration Options

### Keywords Strategy

**Current setup (ANY keyword matches):**
```python
PRODUCT_KEYWORDS = [
    "tcg",
    "trading card",
    "booster",
]
```
✅ Finds: "Pokemon TCG Booster Pack"
✅ Finds: "Trading Card Game Elite Trainer"
✅ Finds: "Booster Bundle"

**If you want MORE specific:**
```python
# Only match products with ALL these words
PRODUCT_KEYWORDS = ["pokemon", "tcg", "scarlet", "violet"]
```
✅ Finds: "Pokemon TCG Scarlet & Violet Booster"
❌ Skips: "Pokemon TCG Sword & Shield"

**To modify:** Edit `bot/store_monitor.py` line 115

### Check Interval

How often to refresh the store page:

```python
CHECK_INTERVAL = 3.0  # Every 3 seconds (default)
```

**Options:**
- **1.0s** - Faster detection, more CPU, might trigger rate limiting
- **3.0s** - Balanced (recommended)
- **5.0s** - Slower but safer

### Timing

**Start immediately:**
```python
LISTING_TIME = datetime.now()
```

**Start in 5 minutes (for testing):**
```python
LISTING_TIME = datetime.now() + timedelta(minutes=5)
```

**Start at specific time:**
```python
LISTING_TIME = datetime(2024, 12, 25, 12, 0, 0)  # Dec 25 at 12 PM
```

---

## 📊 Success Factors

### What Affects Success Rate

1. **Check Interval** (30%)
   - Faster = Better chance
   - But don't go below 1s (rate limiting)

2. **Keywords** (25%)
   - Specific keywords = Less false positives
   - Broad keywords = Catch more products

3. **Timing** (20%)
   - Start monitoring before drop
   - Account for page load time

4. **Internet Speed** (15%)
   - Faster = Quicker page refreshes
   - Stable connection crucial

5. **Competition** (10%)
   - Other shoppers matter
   - Bot gives edge but no guarantees

---

## 🔍 Troubleshooting

### No Products Found in Test

**Problem:** `test_store_monitor.py` finds 0 products

**Solutions:**
1. Store might be empty temporarily
2. Keywords too specific
3. Page structure changed

**Fix:**
```bash
# Try broader keywords
PRODUCT_KEYWORDS = ["pokemon"]  # Very broad

# Or check if store loads properly
# Visit: https://www.lazada.sg/shop/pokemon-store-online-singapore
```

### Bot Finds Wrong Products

**Problem:** Matches non-TCG products

**Solution:** Make keywords more specific:
```python
# Instead of:
PRODUCT_KEYWORDS = ["pokemon"]  # Too broad

# Use:
PRODUCT_KEYWORDS = ["pokemon tcg", "trading card"]  # More specific
```

### Bot Misses New Products

**Problem:** New product appeared but bot didn't detect

**Reasons:**
1. Check interval too slow
2. Product doesn't match keywords
3. Product was already there initially

**Fix:**
- Lower check interval to 1-2 seconds
- Add more keyword variations
- Clear `seen_products` by restarting bot

### Page Won't Load

**Problem:** Store page fails to load

**Solution:**
```bash
# Check if URL is correct
# Should be: https://www.lazada.sg/shop/pokemon-store-online-singapore

# Try manual visit in browser first
# If it works there, bot should work
```

---

## 💡 Pro Tips

### 1. Test First
Always run `test_store_monitor.py` before real sniping:
```bash
python examples/test_store_monitor.py
```

### 2. Use Specific Times
If you know when products drop:
```python
# Pokemon usually drops at 10 AM
LISTING_TIME = datetime(2024, 12, 25, 10, 0, 0)
```

### 3. Multiple Keywords
Cover variations:
```python
PRODUCT_KEYWORDS = [
    "tcg",
    "trading card game",
    "booster pack",
    "booster box",
    "elite trainer box",
    "etb",
]
```

### 4. Check Results
Bot saves screenshots on errors to `screenshots/` folder

### 5. Stay Logged In
Before running bot:
- Log into Lazada in normal browser
- Add payment method
- Add shipping address

---

## 🆚 Store Sniper vs Product Sniper

### Use Store Sniper When:
- ✅ Product not listed yet
- ✅ Don't have product URL
- ✅ Want to catch ANY new TCG product
- ✅ Monitoring a specific store

### Use Product Sniper (main.py) When:
- ✅ Have exact product URL
- ✅ Product already listed but out of stock
- ✅ Know exact product you want
- ✅ Need maximum speed (50ms intervals)

**Speed Comparison:**
- Product Sniper: Checks every **50ms**
- Store Sniper: Refreshes every **3000ms**
- Product Sniper is **60x faster** but needs URL

---

## 📈 Expected Timeline

From new product appearing to checkout:

1. **Detection**: 0-3 seconds (depends on check interval)
2. **Click Product**: 500ms
3. **Load Product Page**: 1-2 seconds
4. **Add to Cart**: 200-500ms
5. **Navigate to Cart**: 1-2 seconds
6. **Checkout**: 1-2 seconds

**Total: 5-10 seconds** from product appearing to ready for order

---

## ⚠️ Important Notes

### This Bot Will:
- ✅ Refresh store page every few seconds
- ✅ Click on NEW matching products
- ✅ Add to cart automatically
- ✅ Stop at checkout (if AUTO_PURCHASE=False)

### This Bot Won't:
- ❌ Work for restocks (only NEW products)
- ❌ Select size/color variants automatically
- ❌ Solve captchas automatically
- ❌ Guarantee you get the product

### Legal & Ethical:
- ⚠️ May violate Lazada's Terms of Service
- ⚠️ Could result in account suspension
- ⚠️ Use at your own risk
- ⚠️ For educational purposes only

---

## 🎯 Quick Command Reference

```bash
# Test if bot can find products
python examples/test_store_monitor.py

# Run the store sniper
python main_store_sniper.py

# Test your regular product sniper
python main.py
```

---

## 📞 Support

If you have issues:

1. **Run test first:**
   ```bash
   python examples/test_store_monitor.py
   ```

2. **Check keywords match** products in store

3. **Verify store URL** is correct

4. **Try broader keywords** if nothing found

5. **Check internet connection**

---

## 🎮 Ready to Go!

You're all set up for Pokemon TCG sniping! 

**Recommended workflow:**
1. ✅ Run `test_store_monitor.py` to verify
2. ✅ Adjust keywords if needed
3. ✅ Set your desired start time
4. ✅ Run `main_store_sniper.py`
5. ✅ Let it monitor for new products
6. ✅ Complete purchase manually when it finds one

Good luck catching 'em all! 🎴✨

