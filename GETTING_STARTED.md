# Getting Started with Lazada Sniper Bot

Welcome! This guide will help you get started with the Lazada Listing Sniper Bot.

## ⚠️ Important Disclaimer

**READ THIS FIRST:**
- This project is for **EDUCATIONAL PURPOSES ONLY**
- Using automation bots on e-commerce platforms may **VIOLATE THEIR TERMS OF SERVICE**
- You could face **ACCOUNT SUSPENSION** or **LEGAL CONSEQUENCES**
- Use at your **OWN RISK**
- Always test with **NON-CRITICAL ITEMS** first

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Basic command line knowledge**
   - How to open terminal/command prompt
   - How to navigate directories (`cd` command)

3. **A Lazada account**
   - Already logged in with shipping info saved
   - Payment method configured

## 🚀 Step 1: Install Dependencies

Open your terminal/command prompt in the project folder and run:

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

If you get errors:
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
playwright install chromium
```

## 📚 Step 2: Complete the Learning Tutorials

**Don't skip this!** The tutorials teach you essential concepts.

Run each tutorial in order:

```bash
# Tutorial 1: HTML & CSS Basics
python learning/01_html_css_basics.py

# Tutorial 2: Web Automation
python learning/02_web_automation.py

# Tutorial 3: Python Essentials
python learning/03_python_essentials.py

# Tutorial 4: Network Analysis
python learning/04_network_analysis.py
```

Each tutorial is interactive and will open a browser to show you examples.

## 🔍 Step 3: Inspect Your Target Product

Before sniping, you need to inspect the product page:

```bash
python examples/inspect_lazada.py
```

This will:
- Open the product page
- Check if buttons are detectable
- Show you the page structure
- Confirm the product works with the bot

When prompted, paste your product URL:
```
https://www.lazada.sg/products/your-product-i123456789.html
```

## ⏱️ Step 4: Test Timing (Optional but Recommended)

Understand timing and performance:

```bash
python examples/test_timing.py
```

This shows you:
- How fast the bot can detect availability
- Your network latency to Lazada
- Click speed comparisons
- Timing precision

## 🎯 Step 5: Configure the Bot

Open `main.py` in a text editor and configure these settings:

```python
# Line ~265 - Set your product URL
PRODUCT_URL = "https://www.lazada.sg/products/your-actual-product-url"

# Line ~271 - Set when product becomes available
LISTING_TIME = datetime(2024, 12, 25, 12, 0, 0)  # Year, month, day, hour, minute, second

# Or for testing - 5 minutes from now:
# LISTING_TIME = datetime.now() + timedelta(minutes=5)

# Line ~274 - Auto-purchase (DANGEROUS!)
AUTO_PURCHASE = False  # Keep False for manual completion

# Line ~277 - Headless mode
HEADLESS = False  # Keep False to see what's happening
```

## 🏃 Step 6: Run the Bot

### Test Run First

For your first run, test with:
- A non-critical product
- `AUTO_PURCHASE = False` (complete manually)
- A listing time 5-10 minutes in the future

```bash
python main.py
```

The bot will:
1. Open a browser
2. Load the product page
3. Show product information
4. Wait until listing time
5. Monitor for availability
6. Add to cart when available
7. Navigate to checkout
8. Stop and let you complete manually (if AUTO_PURCHASE=False)

### Real Run

Once you're confident:
1. Make sure you're logged into Lazada in a normal browser first
2. Save shipping info and payment method
3. Set the correct product URL
4. Set the exact listing time
5. Run the bot **a few minutes early** to pre-load
6. Keep AUTO_PURCHASE=False for safety

```bash
python main.py
```

## 💡 Pro Tips for Success

### Before Running

1. **Stay Logged In**
   - Log into Lazada in your normal browser
   - Save your address and payment info
   - The bot browser shares this session

2. **Fast Internet**
   - Use wired connection if possible
   - Close other downloads/streams
   - Lower latency = better chance

3. **Pre-Load Early**
   - Start the bot 2-5 minutes before listing
   - This loads the page and gets ready
   - Bot will wait and monitor automatically

### During Running

1. **Don't Touch the Browser**
   - Let the bot work
   - Touching it might interfere

2. **Watch for Popups**
   - Some products have size/color selection
   - You may need to select these first
   - Consider doing this before listing time

3. **Be Ready for Captcha**
   - Lazada might show captcha
   - Solve it quickly when it appears

### After Running

1. **Complete Purchase Manually**
   - If AUTO_PURCHASE=False (recommended)
   - Bot stops at checkout
   - You click "Place Order" yourself

2. **Check Confirmation**
   - Verify order went through
   - Save order number
   - Take screenshot

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Playwright not installed" errors
```bash
playwright install chromium
```

### Bot can't find buttons
- Product page structure may have changed
- Run `inspect_lazada.py` to check
- Buttons might need different selectors
- Update selectors in `bot/monitor.py` and `bot/cart.py`

### Bot too slow
- Check your internet speed
- Run `test_timing.py` to measure latency
- Reduce `check_interval` in monitor (but uses more CPU)
- Use headless mode: `HEADLESS = True`

### Product always shows as unavailable
- Product might actually be unavailable
- Selectors might be wrong
- Run `inspect_lazada.py` to verify

### Browser closes immediately
- Check for Python errors in terminal
- Invalid product URL
- Configuration errors

## 📖 Understanding the Code

### Project Structure

```
Lazada/
├── learning/          # Tutorials (start here!)
├── bot/              # Core bot components
│   ├── monitor.py    # Detects availability
│   ├── cart.py       # Adds to cart
│   └── checkout.py   # Completes checkout
├── examples/         # Helper scripts
├── config/           # Settings
└── main.py          # Main bot runner
```

### Key Files

- `main.py` - Main entry point, configure and run here
- `bot/monitor.py` - Monitors product availability
- `bot/cart.py` - Handles add to cart
- `bot/checkout.py` - Handles checkout process
- `config/settings.py` - Configuration settings

### How It Works

1. **Pre-load**: Loads product page ahead of time
2. **Wait**: Waits until listing time (minus few seconds)
3. **Monitor**: Checks for "Add to Cart" button every 50ms
4. **Snipe**: Clicks button immediately when found
5. **Cart**: Adds to cart, handles popups
6. **Checkout**: Proceeds to checkout
7. **Complete**: Either auto-completes or lets you finish

## 🎓 Next Steps

1. ✅ Complete all 4 tutorials
2. ✅ Run `inspect_lazada.py` on your target product
3. ✅ Run `test_timing.py` to understand performance
4. ✅ Do a test run with a non-critical product
5. ✅ Once confident, try with real target
6. 📚 Study the code to understand how it works
7. 🔧 Customize for your specific needs

## ⚖️ Ethical Considerations

Please consider:
- Is it fair to other shoppers?
- Are you violating platform rules?
- Could this harm small sellers?
- What are the legal implications?

This tool should be used **responsibly and ethically**. Consider the impact of your actions.

## 🆘 Getting Help

If you're stuck:
1. Read error messages carefully
2. Check the troubleshooting section above
3. Review the learning tutorials
4. Inspect your product page with `inspect_lazada.py`
5. Test timing with `test_timing.py`

## ✨ Good Luck!

Remember:
- Start small, test thoroughly
- Keep AUTO_PURCHASE=False for safety
- Be prepared to complete manually
- Have patience and practice

Happy (ethical and legal) sniping! 🎯

