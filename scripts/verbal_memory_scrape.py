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
driver.get("https://humanbenchmark.com/tests/verbal-memory")

seen_words = []

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


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

