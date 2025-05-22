import sys
import time
import configparser
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tkinter import simpledialog
from tkinter import messagebox
from component import dialog
from tool import crypto as crypto


config = configparser.ConfigParser()
config.read('login.ini')

driver = webdriver.Chrome()
driver.maximize_window()
actions_chains = ActionChains(driver)

try:
    url = crypto.decrypt(config['login']['url'])
    driver.get(url)
except Exception as e:
    print(e)
    messagebox.showerror("Error","無法開啟網頁。請確認網路狀態是否正常。")
    driver.close()
    sys.exit()

# 登入介面
account = driver.find_element(By.XPATH, "//input[@id='account']")
password = driver.find_element(By.XPATH, "//input[@id='password']")
captcha=driver.find_element(By.XPATH, "//input[@placeholder='驗證碼']")
login=driver.find_element(By.XPATH, "//button[@id='submit_button']")

account.send_keys(crypto.decrypt(config['login']['username']))
password.send_keys(crypto.decrypt(config['login']['password']))

driver.execute_script("window.scrollTo({top: 100});")

captcha_input = simpledialog.askstring(title="驗證碼", prompt="請輸入驗證碼：")

if type(captcha_input) == "None":
    messagebox.showerror("Error","驗證碼未輸入。")
    driver.close()
    sys.exit()

captcha.send_keys(captcha_input)
login.submit()

if driver.current_url.find("loginErrorCode") > -1:
    messagebox.showerror("Error","登入失敗。詳情請查看登入頁面錯誤訊息。")
    driver.close()
    sys.exit()

# 首頁
try:
    classBtn = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located(
            (
                By.XPATH, "//button[@routerlink='/ctms/learner/my-incomplete-courses']"
            )
        )
    )
except Exception as e:
    print(e)
    messagebox.showerror("Error","無法取得修課數目按鈕。")
    driver.close()
    sys.exit()

time.sleep(2)

try:
    numberOfClass = driver.find_element(By.ID, "mat-badge-content-0").text
    if int(numberOfClass) > 0:
        classBtn.click()
except Exception as e:
    print(e)
    messagebox.showinfo("Info","目前沒有排定課程。")
    driver.close()
    sys.exit()

# 課程列表
try:
    classList = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located(
            (
                By.XPATH, "//div[@class='wrap-content']//ehrd-container"
            )
        )
    )
    WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located(
            (
                By.TAG_NAME, "mat-card"
            )
        )
    )
    time.sleep(2)
    classes = classList.find_elements(By.TAG_NAME, "mat-card")
    if len(classes) == 0:
        messagebox.showinfo("Error","找不到課程內容。")
        driver.close()
        sys.exit()
    if len(classes) > 1:
        dialog.show_wait_select_class(driver)
    else:
        classLink = classes[0].find_element(By.XPATH, "//h3[@class='ma-0 pa-0']")
        classLink.click()
except Exception as e:
    print(e)
    messagebox.showinfo("Error","找不到課程內容。")
    driver.close()
    sys.exit()

# 課程細節
try:
    table = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located(
            (
                By.CLASS_NAME, "ui-treetable-table"
            )
        )
    )
except Exception as e:
    print(e)
    messagebox.showerror("Error","無法取得課程細節。")
    driver.close()
    sys.exit()

time.sleep(2)

tbody = table.find_element(By.TAG_NAME, "tbody")
trArr = tbody.find_elements(By.TAG_NAME, "tr")

print("=============================")

i = 0
for tr in trArr:
    tdArr = tr.find_elements(By.TAG_NAME, "td")
    try:
        lessonLink = (tdArr[0].find_element(By.TAG_NAME, "div")
                      .find_element(By.CLASS_NAME, "el-word-break"))
        lessonStatus = tdArr[-1].find_element(By.TAG_NAME, "div").text
        if lessonStatus.find("未曾觀看") > -1:
            driver.execute_script("arguments[0].click();", lessonLink)
            break
    except:
        print( "{}{}{}".format("第", i+1, "行沒有課程狀態，略過。"))
    print("--------------------")
    i += 1

input("自動化程式即將關閉，請按任意健：")
driver.close()