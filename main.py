import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()


def target_com_scraper():
    """
    SCRAPER SETTINGS

    - API_KEY: Your ScraperAPI key. Get your API Key ==> https://www.scraperapi.com/?fp_ref=eunit
    """

    API_KEY = os.getenv("API_KEY", "yourapikey")

    # ScraperAPI proxy settings (with HTTP and HTTPS variants)
    scraper_api_proxies = {
        'proxy': {
            'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
            'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    # URLs to scrape
    url_list = [
        "https://www.target.com/p/enclosed-cat-litter-box-xl-up-up/-/A-90310047?preselect=87059440#lnk=sametab",
    ]

    # Store scraped data
    scraped_data = []

    # Setup Selenium options with proxy
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--start-maximized")

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options, seleniumwire_options=scraper_api_proxies)

    def scroll_down_page(distance=100, delay=0.2):
        """
        Scroll down the page gradually until the end.

        Args:
        - distance: Number of pixels to scroll by in each step.
        - delay: Time (in seconds) to wait between scrolls.
        """
        total_height = driver.execute_script(
            "return document.body.scrollHeight")
        scrolled_height = 0

        while scrolled_height < total_height:
            # Scroll down by 'distance' pixels
            driver.execute_script(f"window.scrollBy(0, {distance});")
            scrolled_height += distance
            time.sleep(delay)  # Pause between scrolls

            # Update the total page height after scrolling
            total_height = driver.execute_script(
                "return document.body.scrollHeight")

        print("Finished scrolling.")

    try:
        for url in url_list:

            # Use Selenium to load the page
            driver.get(url)
            time.sleep(5)  # Give the page time to load

            # Scroll down the page
            scroll_down_page()

            # Extract single elements with Selenium
            def extract_element_text(selector, description):
                try:
                    # Wait for the element and extract text
                    element = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, selector))
                    )
                    text = element.text.strip()
                    return text if text else None  # Return None if the text is empty
                except TimeoutException:
                    print(f"Timeout: Could not find {description}. Setting to None.")
                    return None
                except NoSuchElementException:
                    print(f"Element not found: {description}. Setting to None.")
                    return None

            # Extract single elements
            reviews_data = {"secondary_rating": extract_element_text("div[data-test='secondary-rating']",
                                                                     "secondary_rating"),
                            "rating_count": extract_element_text(
                                "div[data-test='rating-count']", "rating_count"),
                            "rating_histogram": extract_element_text("div[data-test='rating-histogram']",
                                                                     "rating_histogram"),
                            "percent_recommended": extract_element_text("div[data-test='percent-recommended']",
                                                                        "percent_recommended"),
                            "total_recommendations": extract_element_text("div[data-test='total-recommendations']",
                                                                          "total_recommendations")}

            # Extract reviews from 'reviews-list'
            scraped_reviews = []

            # Use Beautiful Soup to extract other content
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Select all reviews in the list using BeautifulSoup
            reviews_list = soup.select("div[data-test='reviews-list'] > div")

            for review in reviews_list:
                # Create a dictionary to store each review's data
                ratings = {}

                # Extract title
                title_element = review.select_one(
                    "h4[data-test='review-card--title']")
                ratings['title'] = title_element.text.strip(
                ) if title_element else None

                # Extract rating
                rating_element = review.select_one("span[data-test='ratings']")
                ratings['rating'] = rating_element.text.strip(
                ) if rating_element else None

                # Extract time
                time_element = review.select_one(
                    "span[data-test='review-card--reviewTime']")
                ratings['time'] = time_element.text.strip(
                ) if time_element else None

                # Extract review text
                text_element = review.select_one(
                    "div[data-test='review-card--text']")
                ratings['text'] = text_element.text.strip(
                ) if text_element else None

                # Append each review to the list of reviews
                scraped_reviews.append(ratings)

            # Append the list of reviews to the main product data
            reviews_data["reviews"] = scraped_reviews

            # Append the overall data to the scraped_data list
            scraped_data.append(reviews_data)

        # Output the scraped data
        print(f"Scraped data: {scraped_data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure driver quits after scraping
        driver.quit()


if __name__ == "__main__":
    target_com_scraper()
