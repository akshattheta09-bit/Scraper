from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from openpyxl import Workbook
import argparse
import sys

def scrape(url):
    print(f"Starting Scrapy for URL: {url}")

    chrome_options = Options()   

    wb = Workbook()
    ws = wb.active
    ws.title = "Scraped Data"
    ws.append(["Category", "Content"]) 
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Navigating to {url}...")
        driver.get(url)
        

        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        

        title = driver.title
        print(f"Title: {title}\n")
        ws.append(["Title", title])
        

        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        if h1_tags:
            for tag in h1_tags:
                text = tag.text.strip()
                print(f"- {text}")
                ws.append(["H1 Heading", text])
        else:
            print("No H1 tags found.")
            
        p_tags = driver.find_elements(By.TAG_NAME, "p")
        if p_tags:
            for i, tag in enumerate(p_tags[:5]):
                text = tag.text.strip()
                if text:
                    print(f"{i+1}. {text}")
                    ws.append([f"Paragraph {i+1}", text])
        else:
            print("No paragraph found.")
            
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
            

        excel_filename = "scraped_data.xlsx"
        wb.save(excel_filename)
        print(f"\nSuccessfully saved to {excel_filename}")

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
        print("\nScraping completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Scraper")
    parser.add_argument("url", help="URL to scrape", nargs="?", default="")
    args = parser.parse_args()
    

    url = args.url
    if not url:
        try:
            url = input("Enter the URL :(e.g., https://example.com): ")
        except KeyboardInterrupt:
            print("\nExiting Scrapy.")
            sys.exit(0)
            
    if url:

        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        scrape(url)
    else:
        print("No URL provided.")
