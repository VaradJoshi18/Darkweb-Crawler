import os
import threading
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tkinter as tk
from tkinter import messagebox, ttk

# ================== TOR SETTINGS ==================
PROXIES = {
    "http": "socks5h://127.0.0.1:9150",
    "https": "socks5h://127.0.0.1:9150"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (TorCrawler)"
}

# ================== GLOBALS ==================
SAVE_DIR = "darkweb_clone"
visited_urls = set()
visited_lock = threading.Lock()
pause_event = threading.Event()
pause_event.set()

pages_crawled = 0
MAX_PAGES = 50

# ================== HELPERS ==================
def sanitize_filename(name):
    name = name.split("?")[0]
    if not name or "." not in name:
        return f"asset_{abs(hash(name)) % 100000}.bin"
    return name.replace("/", "_")

def download_asset(url, assets_dir):
    try:
        r = requests.get(url, proxies=PROXIES, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            filename = sanitize_filename(os.path.basename(urlparse(url).path))
            path = os.path.join(assets_dir, filename)
            with open(path, "wb") as f:
                f.write(r.content)
            return filename
    except:
        pass
    return None

# ================== CORE CRAWLER ==================
def crawl_and_clone(url, base_path, depth):
    global pages_crawled

    pause_event.wait()

    with visited_lock:
        if url in visited_urls or depth <= 0 or pages_crawled >= MAX_PAGES:
            return
        visited_urls.add(url)
        pages_crawled += 1
        progress_bar["value"] = pages_crawled
        status_label.config(text=f"Pages crawled: {pages_crawled}")

    try:
        r = requests.get(url, proxies=PROXIES, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return

        soup = BeautifulSoup(r.text, "html.parser")
        parsed = urlparse(url)

        page_dir = os.path.join(SAVE_DIR, parsed.path.strip("/").replace("/", "_") or "root")
        assets_dir = os.path.join(page_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        # ---- ASSETS ----
        for tag, attr in [("img","src"),("script","src"),("link","href")]:
            for t in soup.find_all(tag):
                if t.get(attr):
                    asset_url = urljoin(url, t[attr])
                    fname = download_asset(asset_url, assets_dir)
                    if fname:
                        t[attr] = f"assets/{fname}"

        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        # ---- LINKS ----
        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a["href"]).split("#")[0]
            p = urlparse(next_url)

            if p.netloc == parsed.netloc and p.path.startswith(base_path):
                crawl_and_clone(next_url, base_path, depth - 1)

        time.sleep(1.2)

    except Exception as e:
        print("Error:", e)

# ================== UI CONTROLS ==================
def start_crawl():
    url = entry.get().strip()
    if not url.endswith(".onion"):
        messagebox.showerror("Error", "Enter valid .onion URL")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)
    parsed = urlparse(url)
    base_path = parsed.path or "/"

    progress_bar["maximum"] = MAX_PAGES

    threading.Thread(
        target=crawl_and_clone,
        args=(url, base_path, 3),
        daemon=True
    ).start()

def pause():
    pause_event.clear()
    status_label.config(text="Paused")

def resume():
    pause_event.set()
    status_label.config(text="Resumed")

# ================== TKINTER UI ==================
app = tk.Tk()
app.title("Tor Dark Web Crawler")
app.geometry("420x260")

tk.Label(app, text="Enter .onion URL").pack(pady=5)
entry = tk.Entry(app, width=50)
entry.pack()

progress_bar = ttk.Progressbar(app, length=350)
progress_bar.pack(pady=15)

status_label = tk.Label(app, text="Idle")
status_label.pack()

tk.Button(app, text="Start", command=start_crawl).pack(pady=5)
tk.Button(app, text="Pause", command=pause).pack()
tk.Button(app, text="Resume", command=resume).pack()

app.mainloop()
