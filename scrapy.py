import argparse
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

def scrape(url):
    print(f"Starting Scrapy (Selenium) for URL: {url}")
    
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Modern headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize Excel Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Scraped Data"
    ws.append(["Category", "Content"]) # Header row
    
    try:
        # Initialize the driver (Selenium 4+ handles the driver executable automatically)
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for the body tag
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scrape basic data
        title = driver.title
        print(f"Page Title: {title}\n")
        ws.append(["Page Title", title])
        
        print(f"--- Headings (H1) ---")
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        if h1_tags:
            for tag in h1_tags:
                text = tag.text.strip()
                print(f"- {text}")
                ws.append(["H1 Heading", text])
        else:
            print("No H1 tags found.")
            
        print(f"\n--- First 5 Paragraphs ---")
        p_tags = driver.find_elements(By.TAG_NAME, "p")
        if p_tags:
            for i, tag in enumerate(p_tags[:5]):
                text = tag.text.strip()
                if text:
                    print(f"{i+1}. {text}")
                    ws.append([f"Paragraph {i+1}", text])
        else:
            print("No paragraph tags found.")
            
        print(f"\n--- First 5 Links ---")
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        if a_tags:
            count = 0
            for tag in a_tags:
                if count >= 5:
                    break
                href = tag.get_attribute('href')
                text = tag.text.strip()
                if href and text:
                    print(f"{count+1}. {text} -> {href}")
                    ws.append([f"Link - {text}", href])
                    count += 1
        else:
            print("No links found.")
            
        # Save to Excel
        excel_filename = "scraped_data.xlsx"
        wb.save(excel_filename)
        print(f"\nSuccessfully saved scraped data to {excel_filename}")

    except Exception as e:
        print(f"\nAn error occurred while scraping: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
        print("\nScraping completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Scraper named Scrapy using Selenium")
    parser.add_argument("url", help="URL to scrape", nargs="?", default="")
    args = parser.parse_args()
    
    # Use URL from argument if provided, otherwise prompt the user
    url = args.url
    if not url:
        try:
            url = input("Please enter the URL to scrape (e.g., https://example.com): ")
        except KeyboardInterrupt:
            print("\nExiting Scrapy.")
            sys.exit(0)
            
    if url:
        # Ensure url has scheme
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        scrape(url)
    else:
        print("No URL provided. Exiting.")
