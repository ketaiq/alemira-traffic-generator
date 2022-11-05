from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from app.models.user import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.utils.time import sleep_for_seconds


class WebDriver:
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=op
        )

    def reset_password(self, url: str, user: User):
        self.driver.get(url)
        self.driver.refresh()
        title = self.driver.title
        self.driver.find_element(By.ID, "Input_Email").send_keys(user.email)
        self.driver.find_element(By.ID, "Input_Password").send_keys(user.password)
        self.driver.find_element(By.ID, "Input_ConfirmPassword").send_keys(
            user.password
        )
        self.driver.find_element(
            By.XPATH, "/html/body/div/main/div/form/div[4]/button"
        ).click()
        WebDriverWait(self.driver, 15).until_not(EC.title_is(title))
        self.driver.close()

web_driver = WebDriver()