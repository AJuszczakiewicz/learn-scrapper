from util import *

index = 0
driver = get_page("https://learn.co/")
login(config()['login'], config()['password'], driver)

open_lesson(driver)

while not last_page_reached(driver):
    if page_has_loaded(driver.current_url):
        open_github_page(driver)
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        download_file(index, driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        click_on_js_element(driver, 'js--next-button')
        click_on_js_element(driver, 'js--button')
        index += 1

driver.quit()
