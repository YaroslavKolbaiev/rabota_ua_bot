from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

KEY_WORDS = [
    "хвилин",
    "хвилини",
    "хвилину",
    "годин",
    "години",
    "годину",
]

COVER_LETTER = "Hi\n\nI am automated bot created by yaroslavkolbaiev@gmail.com\n\nMy task is to look for a vacancies, while my creator is busy with solving tech related tasks\n\nPlease check his portfolio at https://portfolio-page-alpha-black.vercel.app\n\nThank you for your time\n\nHave a great day"


class VacancyManager:
    def __init__(self, driver, category):
        self.driver = driver
        self.category = category
        self.vacancies_for_today = self.get_vacancies()

    def vacancy_manager(self):
        if not self.vacancies_for_today:
            print(f"No vacancies for {self.category} today.")
            return

        for vacancy in self.vacancies_for_today:
            vacancy_link = vacancy.get_attribute("href")
            print(f"Applying for vacancy: {vacancy_link}")

            self.driver.execute_script(
                "window.open(arguments[0], '_blank');", vacancy_link
            )

            sleep(3)

            self.driver.switch_to.window(self.driver.window_handles[1])

            sleep(3)

            try:
                self.apply_for_vacancy()
            except Exception as e:
                print(f"Failed to apply for vacancy: {vacancy_link}\n\nERROR: {e}")
                print(
                    f"Vacancy ({vacancy_link}) has external application form. Closing tabs."
                )
                # Close all tabs
                self.driver.switch_to.window(self.driver.window_handles[2])
                self.driver.close()
                sleep(1)
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()
                sleep(1)
                self.driver.switch_to.window(self.driver.window_handles[0])

        sleep(2)

        print(f"All vacancies for {self.category} have been processed.")

    def apply_for_vacancy(self):
        try:
            already_applied = self.driver.find_element(
                By.CSS_SELECTOR, "div.santa-bg-green-200"
            )
            print("Already applied for this vacancy. Skipping...")
            sleep(1)
            self.driver.close()
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            return
        except Exception as e:
            pass

        apply_button = self.driver.find_element(
            By.CSS_SELECTOR, "button.primary-normal"
        )
        apply_button.click()

        sleep(3)

        add_cover_letter = self.driver.find_element(
            By.TAG_NAME, "alliance-apply-cover-letter"
        )
        add_cover_letter.click()

        sleep(1)

        cover_letter = self.driver.find_element(By.TAG_NAME, "textarea")

        # Clear the default text
        cover_letter.send_keys(Keys.CONTROL + "a")
        cover_letter.send_keys(Keys.DELETE)

        cover_letter.send_keys(COVER_LETTER)

        sleep(1)

        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button.primary-large"
        )
        submit_button.click()

        sleep(5)

        print("Successfully applied for vacancy.")

        self.driver.close()

        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[0])

        sleep(1)

    def get_vacancies(self):
        print(f"Getting vacancies for {self.category}")

        self.driver.get(f"https://robota.ua/zapros/{self.category}/ukraine")

        sleep(5)

        # Scroll to the bottom of the page to load all vacancies
        while True:
            scroll_position = self.driver.execute_script("return window.pageYOffset;")

            self.driver.execute_script(
                "window.scrollTo(0, window.pageYOffset + window.innerHeight);"
            )

            sleep(1)

            if scroll_position == self.driver.execute_script(
                "return window.pageYOffset;"
            ):
                break

        vacancies = self.driver.find_elements(By.CSS_SELECTOR, "a.card")

        vacancies_for_today = []

        for vacancy in vacancies:
            try:
                date = vacancy.find_element(
                    By.CSS_SELECTOR, ".santa-justify-between .santa-typo-secondary"
                )
            except Exception as e:
                print(
                    f"Failed to get date for vacancy: {vacancy.get_attribute('href')}\n\nERROR: {e}"
                )
                continue

            if any(keyword in date.text for keyword in KEY_WORDS):
                vacancies_for_today.append(vacancy)

        sleep(1)

        return vacancies_for_today
