import pyautogui
import time
import keyboard
from selenium.webdriver.common.by import By
from common import accept_cookies, as_tuple, click, create_driver, get_test_settings, wait_for_q_to_close

settings = get_test_settings("typing_test")
driver = create_driver(settings["url"])
typing_area = as_tuple(settings["typing_area"])
ready_color = as_tuple(settings["ready_color"])
stop_key = settings["stop_key"]

def scrape_text_from_page():
    try:
        letters_div = driver.find_element(By.CLASS_NAME, "letters")
        full_text = letters_div.text
        
        print(f"Scrapowany tekst: {full_text[:100]}...")
        return full_text
        
    except Exception as e:
        print(f"Błąd scraping: {e}")
        return None

def type_text_fast(text):
    click(*typing_area)
    time.sleep(0.1)
    #pyautogui.write is slower, we can use typewrite for faster typing
    # for char in text:
    #     pyautogui.write(char)
    pyautogui.typewrite(text, interval=settings["type_interval"])
    
    print("Zakończono pisanie!")


accept_cookies()


# Scrapuj tekst ze strony
text_to_type = scrape_text_from_page()
if text_to_type:
    print(text_to_type)
    print(f"Tekst do przepisania ({len(text_to_type)} znaków)")
    
while not keyboard.is_pressed(stop_key):
    if not text_to_type:
        time.sleep(settings["loop_sleep_seconds"])
        continue
    if pyautogui.pixel(*typing_area) == ready_color:
        type_text_fast(text_to_type)
        break
    else:
        time.sleep(settings["loop_sleep_seconds"])

wait_for_q_to_close(driver)