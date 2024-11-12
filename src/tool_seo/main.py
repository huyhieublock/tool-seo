from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mảng từ khóa và trang
keys = ['allroundz', 'allroundz event', 'allroundz dancer', 'allroundz crew']
pages = ['allroundz.io', 'allroundz.io/event', 'allroundz.io/dancer', 'allroundz.io/crew']

# Hàm tìm kiếm và click vào trang web
def search_and_click(search_key, target_page, run_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.com')

    # Tìm kiếm từ khóa
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_key)
    search_box.submit()

    # Chờ kết quả tìm kiếm
    time.sleep(2)

    try:
        link = driver.find_element(By.XPATH, f"//a[contains(@href, '{target_page}')]")
        link.click()
        print(f"Luồng {run_id}: Đã click vào trang {target_page} với từ khóa '{search_key}'.")
    except Exception as e:
        print(f"Luồng {run_id}: Không tìm thấy phần tử: {e}")
    
    time.sleep(1)
    driver.quit()

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Tạo các tác vụ trong hàng đợi (chỉ chạy 4 luồng cùng lúc)
        futures = [
            executor.submit(search_and_click, keys[i % len(keys)], pages[i % len(pages)], i + 1)
            for i in range(1000)
        ]

        # Duyệt qua các tác vụ theo thứ tự hoàn thành
        for future in as_completed(futures):
            try:
                future.result()  # Chờ tác vụ hoàn thành và xử lý kết quả
            except Exception as e:
                print(f"Lỗi khi chạy luồng: {e}")
