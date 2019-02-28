from selenium import webdriver, common
import time

# given an allrecipes.com url, scrapes and returns the list of reviews of the given recipe
def fetch_reviews(url):
    # load the website using selenium
    driver = webdriver.Chrome('/Users/develop/Desktop/chromedriver')
    driver.get(url)
    
    # try to click the more reviews button as many times as possible
    tried_to_close_popup = False
    while True:
        try:
            more_reviews_button = driver.find_element_by_class_name('more-button')
            more_reviews_button.click()
            time.sleep(3)
        except common.exceptions.ElementNotVisibleException:
            # if this is the first time the button is not possible, it's possible that 
            # it's hidden behind the pop-up so we try to close it 
            if not tried_to_close_popup:
                tried_to_close_popup = True
                try:
                    popup_button = driver.find_element_by_id('bx-close-inside-856988')
                    driver.execute_script("arguments[0].click();", popup_button);
                    popup_appeared_and_closed = True
                    time.sleep(3)
                except (common.exceptions.NoSuchElementException, common.exceptions.ElementNotVisibleException):
                    pass
            # else, this means that the button really did disappear so that all reviews are available
            else: 
                break
    
    # find all of the reviews bodies and return their textt
    review_bodies = driver.find_elements_by_xpath('//p[@itemprop="reviewBody"]')
    reviews = [review.text for review in review_bodies]
    driver.close()
    return reviews