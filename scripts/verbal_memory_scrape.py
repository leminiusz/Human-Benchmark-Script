from bs4 import BeautifulSoup
import requests
import pyautogui
import time
import keyboard
import random
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)  # Set window size to full HD
#You can also set the window size to your monitor size
#For example, if you have a 4K monitor, you can set it to
#But for now you are gonna have to manually set the button positions
#In the future I want to use pyautogui for the same task by that I mean pyautogui and some kind of image to string
# recognition to click the buttons based on the images of the buttons
driver.get("https://humanbenchmark.com/tests/verbal-memory")

seen_words = []

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click(1037,838)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(950, 600)  # start button
time.sleep(2)  # wait for the game to load

while not keyboard.is_pressed('q'):
    try:
        word_element = driver.find_element(By.CLASS_NAME, "word")
        word = word_element.text.strip()
        
        if word in seen_words:
            click(882, 522)  # seen button
        else:
            seen_words.append(word)
            click(1024, 522)  # new button
        
        time.sleep(0.5)
    except:
        continue

print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()  

