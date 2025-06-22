# 📄 Ratchakitcha Web Scraper

This project uses **Playwright**, **Python**, and **Docker** to scrape and download the latest monthly publication from the official Thai Government Gazette website: [ratchakitcha.soc.go.th](https://ratchakitcha.soc.go.th/).

> ⚙️ Built to demonstrate automated browser scraping and containerized deployment.

## 🚀 Features
- **Headless** or **headed** browser mode  
- CLI flags:
  - `-m, --month` (1–12) – select the target month  
  - `-o, --out-dir` – specify the download directory (default: `./downloads`)  
  - `--headless` – run without a visible browser window  
- Automatically saves the PDF to `downloads/`  
- Fully containerized with Docker 

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
> ⚙️ Replace 6 with any month number (1–12).
```bash
mkdir -p downloads
docker run --rm -v "$(pwd)/app/downloads:/app/downloads" ratchakitcha-scraper -m 6 --headless
```
- Downloads for month 6 (June) are saved to ./downloads/ on your host.
- Replace 6 with any month number (1–12)

## 🧪 Local Development (Without Docker)
If you want to test outside of Docker:

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install --with-deps
```

### 2. Run the script
> ⚙️ Replace 6 with any month number (1–12).
```bash
python app/pipeline_run.py -m 6 --headless
```
- The file will be written to ./downloads/ by default.

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
