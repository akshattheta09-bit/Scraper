import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 1. Get the URL from the user
url = input("Enter the URL to scrape (e.g., example.com): ")
if not url.startswith('http'):
    url = 'https://' + url

print(f"\nScraping {url}...")

try:
    # 2. Download the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. Create a new Excel file
    wb = Workbook()
    ws = wb.active
    ws.title = "Scraped Data"
    ws.append(["Category", "Content"])

    # 4. Scrape the Title
    title = soup.title.string if soup.title else "No Title"
    print(f"Title: {title}")
    ws.append(["Title", title])

    # 5. Scrape Headings (H1)
    print("\n--- Headings (H1) ---")
    for tag in soup.find_all('h1'):
        text = tag.get_text(strip=True)
        print(f"- {text}")
        ws.append(["Heading (H1)", text])

    # 6. Scrape First 5 Paragraphs
    print("\n--- First 5 Paragraphs ---")
    for i, tag in enumerate(soup.find_all('p')[:5]):
        text = tag.get_text(strip=True)
        if text:
            print(f"{i+1}. {text}")
            ws.append([f"Paragraph {i+1}", text])

    # 7. Scrape First 5 Links
    print("\n--- First 5 Links ---")
    for i, tag in enumerate(soup.find_all('a')[:5]):
        href = tag.get('href', '')
        text = tag.get_text(strip=True)
        if text and href:
            print(f"{i+1}. {text} -> {href}")
            ws.append([f"Link {i+1}", f"{text} -> {href}"])

    # 8. Save the data
    filename = "scraped_data.xlsx"
    wb.save(filename)
    print(f"\nSuccessfully saved to {filename}")

except Exception as e:
    print(f"\nError: {e}")
