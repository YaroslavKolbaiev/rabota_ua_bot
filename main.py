from driver_manager import DriverManager
from login_manager import LoginManager
from vacancy_manager import VacancyManager

driver = DriverManager().driver

login_manager = LoginManager(driver=driver)

login_manager.login()

javascript_vacancies = VacancyManager(driver=driver, category="javascript")

javascript_vacancies.vacancy_manager()

python_vacancies = VacancyManager(driver=driver, category="python")

python_vacancies.vacancy_manager()

driver.quit()
