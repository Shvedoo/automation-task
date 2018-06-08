from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get("https://www.f-secure.com/en/web/about_global/careers/job-openings")
try:
    if driver.find_element_by_id("cookie-consent").is_displayed():
        driver.find_element_by_xpath(
            "//div[@id='cookie-consent']"
            "//ancestor::a[text()='OK']"
            ).click()
    cities = (
        "//div[@class='form-group filled']"
        "//span[text()='All cities']"
        "//parent::button[@data-id='job-city']"
        )
    poznan = (
        "//div[@class='dropdown-menu open']"
        "//span[text()='Poznań']"
        "//parent::a"
        )
    wait.until(
        EC.presence_of_element_located((By.XPATH, poznan))
        )
    driver.find_element_by_xpath(cities).click()
    driver.find_element_by_xpath(poznan).click()
    QAJob = (
        "//div[@id='job-ads']"
        "//h2[text()='Quality Engineer']"
        "//following-sibling::a"
        )
    wait.until(
        EC.presence_of_element_located((By.XPATH, QAJob))
        )
    pages = driver.find_element_by_xpath(
        "//ul[starts-with(@class, 'pagination')]"
        "//li[last()-1]"
        "//a"
        ).text
    count = int(pages)
    for i in range(count):
        if driver.find_element_by_xpath(QAJob).is_displayed():
            driver.find_element_by_xpath(QAJob).click()
            break
        else:
            nextPage = driver.find_element_by_xpath(
                "//ul[starts-with(@class, 'pagination')]"
                "//a[@class='page-link next']"
                ).click()
    wait.until(lambda d: 1 != len(driver.window_handles))
    driver.switch_to.window(driver.window_handles[-1])
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
    assert "Quality Engineer" in driver.title
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    bodyText = driver.find_element_by_tag_name('body').text
    assert "Quality Engineer wanted" in bodyText
    pass
finally:
    driver.quit()
    print("Test finished")
