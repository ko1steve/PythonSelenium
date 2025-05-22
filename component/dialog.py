import time
from selenium.webdriver.common.by import By
import tkinter as tk
import threading


def show_wait_select_class(driver):
    wait_window = tk.Tk()
    wait_window.title = "等待中"
    wait_window.geometry("250x100")
    label = tk.Label(wait_window, text="請點擊任意課程")
    label.pack(expand=True, pady=20)
    threading.Thread(target=wait_select_class, args=(wait_window, driver), daemon=True).start()
    wait_window.mainloop()

def wait_select_class(window, driver):
    while True:
        try:
            title = driver.find_element(By.XPATH, "//p[@class='f-size-4 title']")
            if len(title.text) > 0:
                window.quit()
                break
        finally:
            time.sleep(0.5)