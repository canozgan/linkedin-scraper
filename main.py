from scraper import Scraper
import sys

def main(item_number, search_job_posting, location):
    print(f"Scraping job posting: {search_job_posting}")
    print(f"Location: {location}")
    print(f"Scraping total items: {item_number}")

    
    item_counter = 0


    url = (
        f"https://www.linkedin.com/jobs/search"
        f"?keywords={search_job_posting}"
        f"&crid=2X7M468O7X5EL&qid=1756250305"
        f"&location={location}"
        f"&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    )
    
    item_counter = Scraper.scrape_page(url, item_number, item_counter)

    print(f"\n\nTotal items found: {item_counter}")
    print("All items were saved to the results.csv file")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <item_number> <search_job_posting> <location>")
    else:
        try:
            item_number = int(sys.argv[1])
            search_job_posting = sys.argv[2]
            location = sys.argv[3]

            if item_number < 1:
                print("Error: item_number must be greater than 0")
            else:
                main(item_number, search_job_posting, location)
        except ValueError:
            print("Error: page_number must be an integer")

    

