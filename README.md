# Dark Web Crawler

Dark Web Crawler is a Python-based application designed to crawl and clone websites on the dark web (specifically, `.onion` domains) using the Tor network. The tool downloads web pages along with their essential assets (such as images, JavaScript, and CSS), storing them locally for offline browsing and analysis. 

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Disclaimer and Legal Notice](#disclaimer-and-legal-notice)
- [Contributing](#contributing)

## Features

- **Dark Web Crawling:** Specifically built to target dark web (`.onion`) websites using Tor.
- **Asset Downloading:** Downloads essential assets (HTML, JavaScript, CSS, images) to create a local clone of the website.
- **Recursive Crawling:** Follows internal links on the site up to a specified depth (default depth level is 3).
- **Graphical User Interface (GUI):** A simple Tkinter-based GUI that allows users to input a URL and start the crawling process.
- **Local Storage:** Saves the cloned website in a structured folder named `darkweb_clone`.

## Requirements

- **Python 3.x**: Ensure you are running Python version 3.6 or higher.
- **Tor**: The script uses a Tor proxy. Make sure the Tor service is installed and running on your machine, listening on port `9050`.
- **Python Packages:**
  - `requests`
  - `beautifulsoup4`
  - `tkinter` (typically included with the standard Python distribution)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/darkweb-crawler.git
   cd darkweb-crawler
   ```

2. **Set Up a Virtual Environment (Optional):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Packages:**

   ```bash
   pip install beautifulsoup
   ```
   ```bash
   pip install pysocks
   ```

4. **Install and Run Tor:**

   - **Linux:** Install the Tor package via your package manager (e.g., `sudo apt-get install tor`), then start the Tor service.
   - **Windows/Mac:** Download the Tor Browser from the [official website](https://www.torproject.org/) and run it, ensuring the proxy is accessible on port 9050.

## Usage

1. **Launch the Application:**

   Execute the Python script:

   ```bash
   python darkweb_crawler.py
   ```

2. **Interface Overview:**

   - A GUI window will appear prompting you to enter a `.onion` URL.
   - Enter the target dark web URL and click on **Start Crawling**.

3. **Crawling Process:**

   - The application will begin crawling from the provided URL.
   - It will recursively navigate through links found on the site (up to a specified depth) and download HTML pages along with assets (images, scripts, and CSS).
   - Downloaded files are saved in a folder named `darkweb_clone` within the project directory.

4. **Viewing the Cloned Site:**

   - Navigate to the `darkweb_clone` folder to view the saved websites.
   - Open the `index.html` file in your web browser to view the cloned homepage.

## How It Works

- **Tor Proxy Configuration:**  
  The tool is configured to use the Tor network via a SOCKS5 proxy running on `127.0.0.1:9050` (both for HTTP and HTTPS requests).

- **Asset Handling:**  
  The script uses BeautifulSoup to parse HTML and find tags such as `<img>`, `<link>`, and `<script>`. Each asset is downloaded, and its reference within the HTML is updated to point to the local file.

- **Recursive Crawling:**  
  URLs are collected from `<a>` tags and recursively processed to a user-defined depth. The crawler ensures that each URL is only processed once to avoid infinite loops.

- **GUI Interface:**  
  Tkinter is used to create a simple window interface where users can input a `.onion` URL and start the crawling in a separate thread to keep the GUI responsive.

## Disclaimer

> **Important:** This project is intended for educational and research purposes only.  
> Crawling and cloning websites, especially on the dark web, can have legal and ethical implications. Ensure that you have permission to crawl any website. Use this tool responsibly and be aware of the laws in your jurisdiction regarding web scraping and dark web activities.

## Contributing

Contributions are welcome! If you would like to contribute to this project:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with clear descriptions of your changes.

---

Feel free to modify the sections to better align with your project's specifics and your personal preferences. Happy coding and stay safe while exploring the dark web!
