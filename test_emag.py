import os
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

EMAIL = os.getenv("EMAG_EMAIL")
PASSWORD = os.getenv("EMAG_PASSWORD")
SEARCH_TERM = os.getenv("SEARCH_TERM")


# Validate environment variables
if not EMAIL:
    raise ValueError("EMAG_EMAIL is missing from .env file")

if not PASSWORD:
    raise ValueError("EMAG_PASSWORD is missing from .env file")

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
    options.add_argument(r"--user-data-dir=C:\Users\cipri\Documents\Projects\emag-selenium-tests\chrome-profile")
    options.add_argument("--profile-directory=Default")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def login(driver, wait):
    """Perform login flow until manual verification step."""
    driver.get("https://www.emag.ro/")

    # Accept cookies if present
    try:
        accept = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept.click()
        print("Cookies accepted.")
    except TimeoutException:
        print("Cookies popup not present.")

    # Click login
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'login')]"))
    )
    login_button.click()
    print("Login button clicked.")

    # Enter email
    email_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user_login_email"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("Email entered.")

    # Click continue
    continue_button = wait.until(
        EC.element_to_be_clickable((By.ID, "user_login_continue"))
    )
    continue_button.click()
    print("Continue clicked.")

    # Try to find password field
    password_selectors = [
        (By.ID, "user_login_password"),
        (By.NAME, "user_login_password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]

    password_input = None
    for by, value in password_selectors:
        try:
            password_input = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((by, value))
            )
            print(f"Password field found using: {by} = {value}")
            break
        except TimeoutException:
            continue

    if password_input is None:
        raise TimeoutException("Password field not found.")

    password_input.clear()
    password_input.send_keys(PASSWORD)
    print("Password entered.")

    # Click submit
    submit_selectors = [
        (By.ID, "user_login_submit"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(., 'Login')]"),
        (By.XPATH, "//button[contains(., 'Autentificare')]"),
    ]

    submit_button = None
    for by, value in submit_selectors:
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((by, value))
            )
            print(f"Submit button found using: {by} = {value}")
            break
        except TimeoutException:
            continue

    if submit_button is None:
        raise TimeoutException("Submit button not found.")

    submit_button.click()
print("Login submitted.")

# Manual verification step
input("Complete the CAPTCHA, phone verification, and click Continue in the browser, then press Enter here to continue...")
def search_and_add_to_cart(driver, wait):
    """Search for product and add to cart."""
    
    search = wait.until(
        EC.visibility_of_element_located((By.ID, "searchboxTrigger"))
    )
    search.clear()
    search.send_keys(SEARCH_TERM)
    search.send_keys(Keys.ENTER)
    print("Search executed.")

    add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Adauga in Cos')]"))
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


def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver, wait)
        search_and_add_to_cart(driver, wait)
        input("Press Enter to close browser...")
    except Exception as error:
        print(f"Test failed: {error}")
        input("Check the browser manually, then press Enter to close...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()