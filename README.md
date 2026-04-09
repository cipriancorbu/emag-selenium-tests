# 🧪 eMAG Selenium Automation Test

Automated end-to-end UI test for the eMAG website using Python, Selenium WebDriver, and pytest.

This project simulates a real user flow:
- Manual login (due to CAPTCHA and anti-bot protection)
- Product search
- Adding a product to the shopping cart
- Validation using assertions
- Navigation to cart page

---

## 🚀 Technologies Used

- Python 3
- Selenium WebDriver
- Pytest
- WebDriver Manager
- Explicit waits (WebDriverWait)

---

## 📌 Features

- Automated browser interaction
- End-to-end test scenario
- Assertion-based validation
- Handling dynamic elements
- Manual login workaround for real-world constraints
- Structured test using pytest

---

## ⚠️ Authentication Note

Due to eMAG security measures (CAPTCHA and anti-bot protection), login cannot be fully automated.

👉 The test requires manual login:

```python
input("Login manually in the browser, then press Enter...")

---

emag-selenium-tests/
│
├── test_emag.py # Main pytest test
├── requirements.txt # Dependencies
├── .gitignore
├── .env
└── chrome-profile/ # Optional saved session

---

⚙️ Setup & Installation

1. Clone the repository

git clone https://github.com/cipriancorbu/emag-selenium-tests.git
cd emag-selenium-tests

2. Create virtual environment

python -m venv .venv

3. Activate environment

.venv\Scripts\Activate.ps1

4. Install dependencies

pip install -r requirements.txt

▶️ Run the test

pytest -v -s

🧠 What this project demonstrates
UI test automation with Selenium
Test execution using pytest
Assertion-based validation
Handling real-world constraints (CAPTCHA, login)
Working with dynamic web elements
End-to-end test design
🔧 Possible Improvements
Page Object Model (POM)
Full test suite (multiple test cases)
Test reporting (Allure / HTML)
CI/CD integration (GitHub Actions)
Headless execution
Session reuse (cookies / profile)
👨‍💻 Author

GitHub: https://github.com/cipriancorbu