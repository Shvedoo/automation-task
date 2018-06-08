from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 30)
driver.get("https://www.f-secure.com/en/web/about_global/careers/job-openings")

try:
    passed = None
    # Click OK on cookie consent if visible
    cookieConsent = driver.find_element_by_id("cookie-consent")
    if cookieConsent.value_of_css_property("z-index") != "-1":
        driver.find_element_by_xpath(
            "//div[@id='cookie-consent']"
            "//ancestor::a[text()='OK']"
            ).click()

    # Choose the city
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
    firstJob = (
        "//div[@id='job-ads']"
        "//article[1]"
        )
    wait.until(
        EC.visibility_of_element_located((By.XPATH, firstJob))
        )

    # Check if there is desired job offer
    QAJob = (
        "//div[@id='job-ads']"
        "//h2[text()='Quality Engineer']"
        "//following-sibling::a"
        )
    wait.until(
        EC.presence_of_element_located((By.XPATH, QAJob))
        )

    # Handle pagination
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
            nextPage = (
                "//ul[starts-with(@class, 'pagination')]"
                "//a[@class='page-link next']"
                )
            wait.until(
                EC.presence_of_element_located((By.XPATH, nextPage))
                )
            driver.find_element_by_xpath(nextPage).click()

    # Assert the job offer page
    wait.until(lambda driver: 1 != len(driver.window_handles))
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
    passed = True
finally:
    driver.quit()
    finalMessage = "Test finished "
    if passed is True:
        finalMessage += "successfully!"
    else:
        finalMessage += "with an error..."
    print(finalMessage)
