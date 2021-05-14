from selenium import webdriver

driver = webdriver.Chrome()

base_url="https://russos.com/collections/collection-of-products/products/"

class shopItem:

    def __init__(self,name,url,unit,amount):
        self.name=name
        self.url=base_url+url
        self.unit=unit
        self.amount=amount

    def go_to_url(self):
        driver.get(self.url)

    def select_quantity(self):
        choose_quantity=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-container"]')
        for option in choose_quantity.find_elements_by_tag_name('option'):
            print(option.text)
        #select_quantity=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-results"]').select_by_visible_text(self.amount)
        
    def add_to_cart(self):
        add_to_cart_button=driver.find_element_by_xpath('//*[@id="product_form_4524870434881"]/div[2]/div[2]/button/span')
        add_to_cart_button.click()

if __name__ == "__main__":

    banana=shopItem("banana","bananas-lb","lb",3)
    banana.go_to_url()
    banana.select_quantity()
    banana.add_to_cart()
