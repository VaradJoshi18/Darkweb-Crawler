import os
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tkinter as tk
from tkinter import messagebox

# Tor proxy settings
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

SAVE_DIR = "darkweb_clone"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

visited_urls = set()

def sanitize_filename(url):
    return url.replace("/", "_").replace("?", "_").replace(":", "_")

def download_asset(url, folder):
    try:
        response = requests.get(url, proxies=PROXIES, timeout=10)
        if response.status_code == 200:
            filename = sanitize_filename(os.path.basename(urlparse(url).path))
            if not filename:
                filename = "index.html"
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as file:
                file.write(response.content)
            return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return None

def crawl_and_clone(url, depth=2):
    if url in visited_urls or depth <= 0:
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url, proxies=PROXIES, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            parsed_url = urlparse(url)
            page_folder = os.path.join(SAVE_DIR, parsed_url.netloc + parsed_url.path.replace("/", "_"))
            if not os.path.exists(page_folder):
                os.makedirs(page_folder)
            
            for tag in soup.find_all(["link", "script", "img"]):
                asset_url = None
                if tag.name == "link" and tag.get("href"):
                    asset_url = urljoin(url, tag["href"])
                    local_path = download_asset(asset_url, page_folder)
                    if local_path:
                        tag["href"] = os.path.relpath(local_path, SAVE_DIR)
                elif tag.name == "script" and tag.get("src"):
                    asset_url = urljoin(url, tag["src"])
                    local_path = download_asset(asset_url, page_folder)
                    if local_path:
                        tag["src"] = os.path.relpath(local_path, SAVE_DIR)
                elif tag.name == "img" and tag.get("src"):
                    asset_url = urljoin(url, tag["src"])
                    local_path = download_asset(asset_url, page_folder)
                    if local_path:
                        tag["src"] = os.path.relpath(local_path, SAVE_DIR)
            
            page_file = os.path.join(page_folder, "index.html")
            with open(page_file, "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            
            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if parsed_url.netloc in next_url:
                    crawl_and_clone(next_url, depth-1)
    except Exception as e:
        print(f"Error: {e}")

def start_crawling():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a .onion URL")
        return
    
    threading.Thread(target=crawl_and_clone, args=(url, 3)).start()
    messagebox.showinfo("Success", "Crawling started! Check the darkweb_clone folder.")

app = tk.Tk()
app.title("Dark Web Crawler")
app.geometry("400x200")

label = tk.Label(app, text="Enter Dark Web (.onion) URL:")
label.pack(pady=5)

entry_url = tk.Entry(app, width=50)
entry_url.pack(pady=5)

start_button = tk.Button(app, text="Start Crawling", command=start_crawling)
start_button.pack(pady=20)

app.mainloop()
