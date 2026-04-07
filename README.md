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
