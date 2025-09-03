# LinkedIn Scraper 🚀

This project leverages an AI-driven **headless browser** to simulate real user behavior, **overcome automated protection systems**, and extract job posting data from LinkedIn. The scraped results are stored in CSV format, making them easy to analyze or integrate into other workflows.

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/canozgan/linkedin-scraper.git
cd linkedin-scraper
```

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
# or
.\venv\Scripts\activate    # Windows PowerShell

pip install -r requirements.txt
```

---

## ▶️ Usage

Run the scraper with:
```bash
python main.py <item_number> <search_job_posting> <location>
```

**item_number** → the number of job postings to scrape (e.g., 50, 100)

**search_job_posting** → the job title or keyword to search for (e.g., python developer, data analyst)

**location** → the location where job postings will be searched (e.g., Istanbul, London, Remote)

Example:

```bash
python main.py 50 "python developer" Istanbul
```

Results will be saved into results.csv.
An example output file is included: example_results.csv.

---

## 📂 Project Structure

```
linkedin-scraper/
├── main.py
├── scraper.py
├── requirements.txt
├── results.csv        # generated after running the scraper
├── example_results.csv
└── README.md
```

---

## 🛠️ Technologies & Libraries

**[Camoufox](https://pypi.org/project/camoufox/)** – Headless browser that mimics human-like behavior

**[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** – HTML parsing

**Python standard libraries**: csv, sys, os, time, random

---

## ⚠️ Disclaimer

This project is intended for educational purposes only.
You are solely responsible for how you use it.
Please do not use it in ways that violate [LinkedIn’s User Agreement](https://www.linkedin.com/legal/user-agreement).







