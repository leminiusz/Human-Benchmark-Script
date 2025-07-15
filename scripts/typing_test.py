import pyautogui
import time
import keyboard
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/typing")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def scrape_text_from_page():
    try:
        wait = WebDriverWait(driver, 10)
        letters_div = driver.find_element(By.CLASS_NAME, "letters")
        full_text = letters_div.text
        
        print(f"Scrapowany tekst: {full_text[:100]}...")
        return full_text
        
    except Exception as e:
        print(f"Błąd scraping: {e}")
        return None

def type_text_fast(text):
    click(486,465)  # Centrum obszaru pisania
    time.sleep(0.1)
    #pyautogui.write is slower, we can use typewrite for faster typing
    # for char in text:
    #     pyautogui.write(char)
    pyautogui.typewrite(text, interval=0)  
    
    print("Zakończono pisanie!")


click(1050, 807)  # accept cookies button
time.sleep(2)  # wait for the page to load


# Scrapuj tekst ze strony
text_to_type = scrape_text_from_page()
if text_to_type:
    print(text_to_type)
    print(f"Tekst do przepisania ({len(text_to_type)} znaków)")
    
while not keyboard.is_pressed('q'):
    if pyautogui.pixel(486,465) == (234,243,250):
        type_text_fast(text_to_type)
        break
    else:
        time.sleep(0.1)
print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()