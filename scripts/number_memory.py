import pyautogui
import time
import keyboard
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By
import easyocr

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/number-memory")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click(1050,807)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(955, 596)  # start button
time.sleep(0.1)  # wait for the game to load

error_printed = False 
while not keyboard.is_pressed('q'):
    # Click on the game area to start the number memory test
    x,y, width, height = 440, 300, 1050, 270 
    if pyautogui.pixel(913, 493) == (255, 255, 255) or pyautogui.pixel(913,542) == (255, 255, 255) or pyautogui.pixel(915, 502) == (255, 255, 255): 
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot= screenshot.convert("L") # Convert to grayscale
        screenshot.save("number_screen.png")
        reader = easyocr.Reader(['en'])
        results = reader.readtext("number_screen.png",allowlist='0123456789')
        time.sleep(0.2) 
        #ocr zwraca wyniki listę krotek, gdzie pierwszy element to współrzędne, a drugi to tekst
        print("Wyniki OCR:", results)
    if results and pyautogui.pixel(832,338) == (255, 255, 255):
        print("Input screen detected - rozpoczynam pisanie liczby")
        error_printed = False 
        #Trzeba przesortowac wyniki według współrzędnych Y zeby laczylo dolna liczbe do gorej a nie na odwrót
        sorted_results = sorted(results, key=lambda x: x[0][0][1])
        number_text = ""
        for result in sorted_results:
            #usuwamy jeszcze potencjalne spacje i znaki nowej linii, bo result[1] zawiera
            # ale moga sie tam wkrasc jakies bledy w rozpoznaniu
            text = result[1].replace(" ", "").replace("\n", "")
            number_text += text
        
        print(f"Detected number: {number_text}")
        
        click(847,436)#click to input the number
        time.sleep(0.1)  # wait for the input field to be ready
        pyautogui.write(number_text)
        time.sleep(0.1) 
        click(941,531)  # click the submit button
        time.sleep(0.1)
        click(945,592)  # click the next button
        time.sleep(0.1)
    else:
        if not error_printed:
            print("ERROR - No number detected")
            error_printed = True

print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()     