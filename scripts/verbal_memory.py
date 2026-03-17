import time
import keyboard
from selenium.webdriver.common.by import By
from common import as_tuple, click, create_driver, get_test_settings, start_test, wait_for_q_to_close

settings = get_test_settings("verbal_memory")
driver = create_driver(settings["url"])
#You can also set the window size to your monitor size
#For example, if you have a 4K monitor, you can set it to
#But for now you are gonna have to manually set the button positions
#In the future I want to use pyautogui for the same task by that I mean pyautogui and some kind of image to string
# recognition to click the buttons based on the images of the buttons

seen_words = []
start_test(as_tuple(settings["start_button"]))
stop_key = settings["stop_key"]

while not keyboard.is_pressed(stop_key):
    try:
        word_element = driver.find_element(By.CLASS_NAME, "word")
        word = word_element.text.strip()
        
        if word in seen_words:
            click(*as_tuple(settings["seen_button"]))
        else:
            seen_words.append(word)
            click(*as_tuple(settings["new_button"]))
        
        time.sleep(settings["loop_sleep_seconds"])
    except:
        continue

wait_for_q_to_close(driver)

