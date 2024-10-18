from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Инициализация драйвера
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

def parse_ad(ad_url):
    """Парсинг одного объявления"""
    driver.get(ad_url)

    try:
        show_phone_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'show-phones')))
        show_phone_button.click()

        try:
            captcha_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
            driver.switch_to.frame(captcha_frame)

            # Ожидание исчезновения перекрывающего элемента
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[style*="z-index: 2000000000"]')))

            captcha_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.recaptcha-checkbox')))
            captcha_checkbox.click()

            # ЗДЕСЬ ПРОИСХОДИТ РЕШЕНИЕ КАПЧИ
            # При открытии браузера(хром) вpip freeze > requirements.txt нём установлено расширение nopecha
            # Оно решает 100 reCaptcha в день, в авто режиме( проверка по ip)

            driver.switch_to.default_content()
            time.sleep(30)  # Увеличенное время ожидания для решения капчи вручную
        except Exception as e:
            print()

        phone_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.offer__contacts-phones p')))
        phone_number = phone_element.text.strip()
        specialist_work = driver.find_element(By.CSS_SELECTOR,'.user-description-address-speciality').text.strip()\
            if driver.find_elements(By.CSS_SELECTOR, '.user-description-address-speciality') else 'Не указано'
        owner_name = driver.find_element(By.CSS_SELECTOR, '.owners__name').text.strip()
        agent_label = driver.find_element(By.CSS_SELECTOR, '.label-user-agent').text.strip() if driver.find_elements(
            By.CSS_SELECTOR, '.label-user-agent') else 'Не агент'

        print(f"Имя: {owner_name}, Телефон: {phone_number}, Статус: {agent_label}, Работает: {specialist_work}")
    except Exception as e:
        print(f"Ошибка при обработке объявления {ad_url}")

def parse_page(page_url):
    driver.get(page_url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-card__title')))

    ad_elements = driver.find_elements(By.CSS_SELECTOR, '.a-card__title')
    ad_links = [ad.get_attribute('href') for ad in ad_elements if ad.get_attribute('href')]

    for ad_link in ad_links:
        parse_ad(ad_link)
        time.sleep(2)

def paginate(base_url, num_pages):
    for page in range(1, num_pages + 1):
        page_url = f"{base_url}?page={page}"
        print(f"Парсинг страницы {page}: {page_url}")
        parse_page(page_url)
        time.sleep(3)

if __name__ == "__main__":
    base_url = "https://krisha.kz/prodazha/kvartiry/"
    num_pages = 5
    paginate(base_url, num_pages)
    driver.quit()
