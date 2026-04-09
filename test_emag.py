import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Load environment variables
load_dotenv()

SEARCH_TERM = os.getenv("SEARCH_TERM")

if not SEARCH_TERM:
    raise ValueError("SEARCH_TERM is missing from .env file")


def get_chrome_binary_path():
    """Try to locate Chrome installation on Windows."""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def create_driver():
    """Create Chrome driver with automatic driver management."""
    options = Options()
    options.add_argument("--start-maximized")

    chrome_binary = get_chrome_binary_path()
    if not chrome_binary:
        raise FileNotFoundError(
            "Google Chrome not found. Install Chrome or switch to Edge."
        )

    options.binary_location = chrome_binary

    # Use a dedicated Chrome profile for test sessions
    options.add_argument(
        r"--user-data-dir=C:\Users\cipri\Documents\Projects\emag-selenium-tests\chrome-profile"
    )
    options.add_argument("--profile-directory=Default")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


@pytest.fixture
def driver():
    """Create and close the browser for each test."""
    browser = create_driver()
    yield browser
    browser.quit()


def open_emag_login_page(driver, wait):
    """Open eMAG homepage, accept cookies if present, and open login page."""
    driver.get("https://www.emag.ro/")

    try:
        accept = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept.click()
        print("Cookies accepted.")
    except TimeoutException:
        print("Cookies popup not present.")

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]"))
    )
    login_button.click()
    print("Login page opened.")


def search_and_add_to_cart(driver, wait):
    """Search for product and add it to cart."""

    search = wait.until(
        EC.visibility_of_element_located((By.ID, "searchboxTrigger"))
    )
    search.clear()
    search.send_keys(SEARCH_TERM)
    search.send_keys(Keys.ENTER)
    print("Search executed.")

    add_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Adauga in Cos')]")
        )
    )
    add_button.click()
    print("Product added to cart.")

    # Assertion: verify confirmation message
    confirmation = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Produsul a fost adaugat in cos')]")
        )
    )

    assert "cos" in confirmation.text.lower(), "Product was NOT added to cart!"
    print("Assertion passed: Product successfully added to cart.")

    # Wait for confirmation popup action
    view_cart_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(., 'Vezi detalii cos') or contains(., 'Vezi detalii coș')]"
            )
        )
    )
    driver.execute_script("arguments[0].click();", view_cart_button)
    print("Navigated to cart from confirmation popup.")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Cosul tau') or contains(text(), 'Coșul tău')]")
        )
    )
    print("Cart page loaded successfully.")


def test_search_and_add_to_cart(driver):
    """End-to-end test: open eMAG, login manually, search product, add to cart."""
    wait = WebDriverWait(driver, 10)

    open_emag_login_page(driver, wait)

    input("Login manually in the browser, then press Enter here to continue...")

    search_and_add_to_cart(driver, wait)

    input("Press Enter to close the browser...")