import os
from dotenv import load_dotenv
from time import sleep
from selenium.webdriver.common.by import By

load_dotenv()

account_email = os.environ.get("ACCOUNT_EMAIL")
account_password = os.environ.get("ACCOUNT_PASSWORD")


class LoginManager:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.get("https://rabota.ua/")
        sleep(3)

        login_button = self.driver.find_element(
            By.TAG_NAME, "alliance-header-link-with-icon"
        )
        login_button.click()
        sleep(3)

        email_input = self.driver.find_element(By.ID, "otp-username")
        email_input.send_keys(account_email)
        sleep(1)

        password_input = self.driver.find_element(By.CSS_SELECTOR, "input.ng-pristine")
        password_input.send_keys(account_password)
        sleep(1)

        submit_button = self.driver.find_element(
            By.XPATH,
            "/html/body/app-root/div/alliance-login-page/div/alliance-login-desktop/div/lib-login-form/div/div/santa-button-spinner/div/santa-button/button",
        )
        submit_button.click()

        sleep(5)
