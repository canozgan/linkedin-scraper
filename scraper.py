import time
from camoufox.sync_api import Camoufox
from bs4 import BeautifulSoup
import csv
import os
import random


class Scraper():

    def get_page_html(url, item_number, retries=3, delay=5):
        '''
        Open the given URL with Camoufox and return the page HTML.
        Includes retry logic in case of errors or slow loading.
        '''
        attempt = 0

        while attempt < retries:
            attempt += 1
            print(f"\n[INFO] Attempt {attempt}/{retries} for {url}")

            camoufox_args = {
                "headless": True,
                "humanize": True,
                "window": (1280, 720)
            }

            try:
                with Camoufox(**camoufox_args) as browser:
                    page = browser.new_page()
                    page.goto(url)

                    # Wait until page is stable
                    page.wait_for_load_state(state="domcontentloaded")
                    page.wait_for_load_state("networkidle")

                    rand = 5000 + random.randint(1000, 5000)
                    page.wait_for_timeout(rand)  # wait 5+ seconds

                    result_number = page.locator(
                        ".results-context-header__job-count"
                    ).text_content()

                    # remove non-digit characters and convert from string to int
                    result_number = Scraper.only_numbers(result_number)

                    if result_number < item_number:
                        raise Exception(
                            f"Not enough job postings, total job postings: "
                            f"{result_number}"
                        )

                    # Locate and close the pop-up
                    pop_up = page.locator("role=button[name='Dismiss']")
                    if pop_up.is_visible():
                        pop_up.click()

                    # Scroll down until see the button "see more job"
                    more_job_button_class_text = (
                        ".infinite-scroller__show-more-button."
                        "infinite-scroller__show-more-button--visible"
                    )
                    more_job_button = page.locator(more_job_button_class_text)

                    while more_job_button.count() < 1:
                        page.mouse.wheel(0, 1000)  # scroll down 1000px
                        time.sleep(2)  # wait 2 seconds

                    # click button until the page reaches the target number of items
                    item_class_text = ".base-card"
                    current_items = page.locator(item_class_text)

                    previous_item_count = current_items.count()
                    while current_items.count() < item_number:

                        # if the button is no longer visible
                        if more_job_button.count() < 1:
                            raise Exception(
                                f"Only {current_items.count()} job postings are public"
                            )

                        more_job_button.click()
                        time.sleep(3)

                        # If the button visible but not changing current number of items
                        if previous_item_count == current_items.count():
                            raise Exception(
                                f"Only {current_items.count()} job postings are public"
                            )

                        previous_item_count = current_items.count()

                    html = page.content()
                    return html  # success

            except Exception as e:
                print(f"[ERROR] Attempt {attempt} failed: {e}")

            if attempt < retries:
                random_delay = delay + random.randint(1, 5)
                print(f"[INFO] Retrying in {random_delay} seconds...")
                time.sleep(random_delay)

        print("[FATAL] All retry attempts failed.")
        return None

    def parse_items(html, item_counter, item_number):
        """
        Parse items from the given HTML using BeautifulSoup.
        """
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.base-card")[:item_number]

        # Name of the CSV file
        csv_file = "results.csv"

        # If the file does not exist, create it and write the header row
        if not os.path.exists(csv_file):
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Item", "Job_Title", "Company_Name", "Location", "Url"]
                )

        for item in items:
            item_counter += 1

            # Extract title
            job_title = item.select_one(".base-search-card__title")
            job_title_text = job_title.get_text(strip=True) if job_title else "N/A"

            # Extract company name
            company_name = item.select_one(".base-search-card__subtitle")
            company_name_text = (
                company_name.get_text(strip=True) if company_name else "N/A"
            )

            # Extract location
            location = item.select_one(".job-search-card__location")
            location_text = location.get_text(strip=True) if location else "N/A"

            # Extract url
            url = item.select_one(".base-card__full-link")
            url_text = url['href'] if url else "N/A"

            # Print results
            print(f"\nItem {item_counter}")
            print("Job Title:", job_title_text)
            print("Company Name:", company_name_text)
            print("Location:", location_text)
            print("Url:", url_text)

            # Append the current item to the CSV file
            with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        item_counter,
                        job_title_text,
                        company_name_text,
                        location_text,
                        url_text
                    ]
                )

        return item_counter

    def scrape_page(url, item_number, item_counter):
        """
        High-level function to scrape one page.
        """
        html = Scraper.get_page_html(url, item_number)
        if html:
            item_counter = Scraper.parse_items(html, item_counter, item_number)
        else:
            print("[ERROR] Could not scrape page after retries.")

        return item_counter

    def only_numbers(text):
        # Join all digits from the input string into one string
        num_str = ''.join(ch for ch in text if ch.isdigit())
        # Convert the result to an integer, return 0 if no digits were found
        return int(num_str) if num_str else 0
