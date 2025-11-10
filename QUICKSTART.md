# Quick Start Guide

**Want to get running fast? Follow these steps:**

## 1. Install (2 minutes)

```bash
pip install -r requirements.txt
playwright install chromium
```

## 2. Learn the Basics (30 minutes)

Run tutorials in order:
```bash
python learning/01_html_css_basics.py
python learning/02_web_automation.py
python learning/03_python_essentials.py
python learning/04_network_analysis.py
```

## 3. Inspect Your Product (5 minutes)

```bash
python examples/inspect_lazada.py
```

Enter your product URL when prompted.

## 4. Configure (2 minutes)

Edit `main.py`:
```python
PRODUCT_URL = "your-lazada-product-url"
LISTING_TIME = datetime(2024, 12, 25, 12, 0, 0)
AUTO_PURCHASE = False  # Keep False!
```

## 5. Run! (Ready when you are)

```bash
python main.py
```

## Important Tips

✅ **DO:**
- Complete tutorials first
- Test with non-critical items
- Keep AUTO_PURCHASE=False
- Start bot 2-5 minutes early
- Be logged into Lazada already

❌ **DON'T:**
- Skip the tutorials
- Use on critical/expensive items first
- Enable AUTO_PURCHASE without testing
- Touch browser while bot is running
- Use on slow/unstable internet

---

**Need more details?** Read [GETTING_STARTED.md](GETTING_STARTED.md)

**Having issues?** Check the troubleshooting section in [GETTING_STARTED.md](GETTING_STARTED.md)

