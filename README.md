# 📄 Ratchakitcha Web Scraper

This project uses **Playwright**, **Python**, and **Docker** to scrape and download the latest monthly publication from the official Thai Government Gazette website: [ratchakitcha.soc.go.th](https://ratchakitcha.soc.go.th/).

> ⚙️ Built to demonstrate automated browser scraping and containerized deployment.

## 🚀 Features
- Headless scraping using Playwright
- Auto-selects the **last month's publication**
- Downloads official documents as files
- Containerized with Docker for easy reproducibility
- Saves output to a local `downloads/` folder

## 🧰 Tech Stack
- Python 3.12
- Playwright for browser automation
- Docker for containerization

## 🗂️ Folder Structure
```plaintext
ratchakitcha-scraper/
├── app/
│ └── pipeline_run.py # Main scraping logic
├── downloads/ # Where downloaded files are saved
├── Dockerfile # Container config
├── requirements.txt # Python packages
└── README.md # This file
```

## 🐳 How to Run with Docker

> Downloads will be saved to your local `./downloads/` folder.

### 1. Build the Docker image
```bash
docker build -t ratchakitcha-scraper .
```

### 2. Run the container
```bash
docker run --rm -v "$(pwd)/downloads:/app/downloads" ratchakitcha-scraper
```

## 🧪 Local Development (Without Docker)
If you want to test outside of Docker:

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install --with-deps
```

### 2. Run the script
```bash
python app/pipeline_run.py
```

## 📌 About the Website
- Site: [ratchakitcha.soc.go.th](https://ratchakitcha.soc.go.th)
- This is the official online gazette for Thailand.
- This project respects the site's terms of use and scrapes only publicly available documents.

## 📄 License
This project is open source and available under the [MIT License](https://opensource.org/license/mit).

## Acknowledgements
Thanks to:
- The Thai Government Gazette
- Playwright & Microsoft
- Docker community
