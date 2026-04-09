# 🧪 eMAG Selenium Automation Tests

Automated end-to-end test scenario for the eMAG website, built using Python and Selenium WebDriver.

This project simulates a real user flow:
- Login process
- Product search
- Adding a product to the shopping cart

---

## 🚀 Technologies Used

- Python 3
- Selenium WebDriver
- ChromeDriver
- WebDriverWait (explicit waits)

---

## 📌 Features

- Automated browser interaction using Selenium
- Login flow with manual CAPTCHA handling
- Product search functionality
- Add-to-cart automation
- Use of explicit waits for stability
- Clean and modular test structure

---

## ⚠️ Note on Authentication

Due to eMAG security measures (CAPTCHA and phone verification), full login automation is not possible.

👉 The script pauses to allow manual completion:

```python
input("Complete CAPTCHA and press Enter...")

---

emag-selenium-tests/
│
├── test_emag.py        # Main automation script
├── requirements.txt    # Dependencies
├── .gitignore          # Ignored files
├── .env                # Credentials (not uploaded)
└── chrome-profile/     # Browser session (ignored)

---

⚙️ Setup & Installation

1. Clone the repository

git clone https://github.com/cipriancorbu/emag-selenium-tests.git
cd emag-selenium-tests

2. Create virtual environment

python -m venv .venv

3. Activate environment

.venv\Scripts\Activate.ps1

▶️ Run the test

python test_emag.py

🧠 What this project demonstrates
UI test automation with Selenium
Handling real-world constraints (CAPTCHA, login verification)
Element interaction (click, send_keys, waits)
Basic test flow design
Debugging dynamic web elements


🔧 Possible Improvements
Implement Page Object Model (POM)
Add pytest framework
Add assertions for validation
Generate test reports (HTML / Allure)
Add CI/CD (GitHub Actions)
Run tests in headless mode
👨‍💻 Author

GitHub: https://github.com/cipriancorbu

