import pyautogui
import time
import keyboard
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By
import easyocr


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/chimp")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click(1050,807)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(955, 596)  # start button
time.sleep(0.1)  # wait for the game to loadm

def find_numbers():
    x, y, width, height = 500, 170, 940, 532
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    
    # Zwiększ rozmiar zdjęcia dla lepszego OCR
    screenshot = screenshot.resize((screenshot.width * 3, screenshot.height * 3))
    
    # Konwertuj na grayscale i zwiększ kontrast
    screenshot = screenshot.convert("L")
    
    # Zapisz dla debugowania
    screenshot.save("chimp_screen.png")
    
    reader = easyocr.Reader(['en'], gpu=True)
    results = reader.readtext("chimp_screen.png", 
                             allowlist='0123456789',
                             width_ths=0.7,
                             height_ths=0.7,
                             paragraph=False)
    
    print(f"OCR wyniki: {results}")
    
    numbers = []
    for result in results:
        coords = result[0]
        text = result[1].strip()
        confidence = result[2]
        
        if text.isdigit() and confidence > 0.5:
            # Przeskaluj współrzędne z powrotem (bo zwiększyliśmy rozmiar x3)
            local_center_x = int((coords[0][0] + coords[2][0]) / 6)  # /6 bo *3 w resize
            local_center_y = int((coords[0][1] + coords[2][1]) / 6)
            
            # Przeskaluj na pełny ekran
            screen_x = x + local_center_x
            screen_y = y + local_center_y
            
            numbers.append((int(text), screen_x, screen_y))
            print(f"Cyfra {text} na ({screen_x}, {screen_y}), pewność: {confidence:.2f}")
    
    # Posortuj według cyfr (1, 2, 3, 4...)
    numbers.sort(key=lambda x: x[0])
    return numbers

round_number = 1
expected_numbers = 4  # First round starts with 4 numbers

while not keyboard.is_pressed('q'):
    # Znajdź cyfry na ekranie
    numbers = find_numbers()
    
    if numbers and len(numbers) == expected_numbers:
        print(f"Runda {round_number}: Znaleziono {len(numbers)} cyfr (oczekiwano {expected_numbers}): {[n[0] for n in numbers]}")
        
        for number, x, y in numbers:
            print(f"Klikam cyfrę {number} na ({x}, {y})")
            click(x, y)
            time.sleep(0.1)
        
        # Przejdź do następnej rundy
        round_number += 1
        expected_numbers += 1  # Każda kolejna runda ma +1 cyfrę
        
        time.sleep(2)  # Poczekaj na następną rundę
        click(931,564)  # Kliknij continue
    elif numbers:
        print(f"Znaleziono {len(numbers)} cyfr, ale oczekiwano {expected_numbers}. Czekam...")
        time.sleep(0.1)
    else:
        time.sleep(0.1)

print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit() 