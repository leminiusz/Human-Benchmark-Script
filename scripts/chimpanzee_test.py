import pyautogui
import time
import keyboard
import easyocr
from common import as_tuple, click, create_driver, get_test_settings, start_test, wait_for_q_to_close


settings = get_test_settings("chimpanzee_test")
driver = create_driver(settings["url"])
start_test(as_tuple(settings["start_button"]))

reader = easyocr.Reader(["en"], gpu=settings["use_gpu"])

ocr_region = as_tuple(settings["ocr_region"])
ocr_scale = settings["ocr_scale"]
ocr_image = settings["ocr_image"]
ocr_allowlist = settings["ocr_allowlist"]
ocr_width_ths = settings["ocr_width_ths"]
ocr_height_ths = settings["ocr_height_ths"]
ocr_paragraph = settings["ocr_paragraph"]
ocr_confidence_threshold = settings["ocr_confidence_threshold"]
between_number_clicks_seconds = settings["between_number_clicks_seconds"]
next_round_wait_seconds = settings["next_round_wait_seconds"]
continue_button = as_tuple(settings["continue_button"])
idle_wait_seconds = settings["idle_wait_seconds"]
stop_key = settings["stop_key"]


def normalize_number_text(text):
    return "".join(char for char in text if char.isdigit())


def extract_candidates(text, expected_max):
    if not text:
        return []
    if expected_max <= 9:
        return [int(char) for char in text if char.isdigit() and char != "0"]
    return [int(text)] if text.isdigit() else []


def find_numbers(expected_max):
    x, y, width, height = ocr_region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    if ocr_scale != 1:
        screenshot = screenshot.resize((int(screenshot.width * ocr_scale), int(screenshot.height * ocr_scale)))

    screenshot = screenshot.convert("L")
    screenshot.save(ocr_image)

    results = reader.readtext(
        ocr_image,
        allowlist=ocr_allowlist,
        width_ths=ocr_width_ths,
        height_ths=ocr_height_ths,
        paragraph=ocr_paragraph,
    )

    print(f"OCR wyniki: {results}")

    best_numbers = {}
    for result in results:
        coords = result[0]
        text = normalize_number_text(result[1].strip())
        confidence = result[2]

        if text and confidence > ocr_confidence_threshold:
            local_center_x = int((coords[0][0] + coords[2][0]) / (2 * ocr_scale))
            local_center_y = int((coords[0][1] + coords[2][1]) / (2 * ocr_scale))

            screen_x = x + local_center_x
            screen_y = y + local_center_y

            for number_value in extract_candidates(text, expected_max):
                if not (1 <= number_value <= expected_max):
                    continue

                current_best = best_numbers.get(number_value)
                if current_best is None or confidence > current_best[3]:
                    best_numbers[number_value] = (number_value, screen_x, screen_y, confidence)
                    print(f"Cyfra {number_value} na ({screen_x}, {screen_y}), pewność: {confidence:.2f}")

    numbers = [(value, point_x, point_y) for value, point_x, point_y, _ in best_numbers.values()]
    numbers.sort(key=lambda item: item[0])
    return numbers


round_number = 1
expected_numbers = settings["expected_start_numbers"]

while not keyboard.is_pressed(stop_key):
    numbers = find_numbers(expected_numbers)

    if numbers and len(numbers) == expected_numbers:
        print(f"Runda {round_number}: Znaleziono {len(numbers)} cyfr (oczekiwano {expected_numbers}): {[n[0] for n in numbers]}")

        for number, point_x, point_y in numbers:
            print(f"Klikam cyfrę {number} na ({point_x}, {point_y})")
            click(point_x, point_y)
            time.sleep(between_number_clicks_seconds)

        round_number += 1
        expected_numbers += 1

        time.sleep(next_round_wait_seconds)
        click(*continue_button)
    elif numbers:
        print(f"Znaleziono {len(numbers)} cyfr, ale oczekiwano {expected_numbers}. Czekam...")
        time.sleep(idle_wait_seconds)
    else:
        time.sleep(idle_wait_seconds)

wait_for_q_to_close(driver)