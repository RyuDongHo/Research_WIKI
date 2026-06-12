"""Capture MVP GUI screenshots for the assignment submission."""
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "submission/screenshots")
OUT.mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1680,1050")
driver = webdriver.Edge(options=options)
try:
    driver.get("http://127.0.0.1:8780/")
    time.sleep(4)
    driver.save_screenshot(str(OUT / "01-dashboard.png"))
    views = [("papers", "02-papers.png"), ("pages", "03-wiki-pages.png"), ("mcp", "04-mcp-status.png")]
    for view, name in views:
        driver.find_element(By.CSS_SELECTOR, f'[data-nav-view="{view}"]').click()
        time.sleep(2)
        driver.save_screenshot(str(OUT / name))
    print("saved:", sorted(p.name for p in OUT.glob("*.png")))
finally:
    driver.quit()
