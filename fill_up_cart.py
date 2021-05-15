from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome()

base_url="https://russos.com/collections/collection-of-products/products/"

class shopItem:

    def __init__(self,amount,name,unit,url):
        self.amount=amount
        self.name=name
        self.unit=unit
        self.url=base_url+url

    def go_to_url(self):
        driver.get(self.url)

    def select_quantity(self):
        quantity_button=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-container"]').click()
        #select_quantity=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-result-82lz-3"]').click()
        #select_quantity=driver.find_element_by_xpath('//*[starts-with(@id="select2-quantity-proxy-result") and ends-with(@id="3")]').click()
        #select_quantity=driver.find_element_by_xpath('//*[contains(@id,"-3")]').click()


        #quantity_options=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-results"]')
        #//*[@id="select2-quantity-proxy-result-xspx-2"]
        #quantity_options=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-results"]')
        #select_quantity=Select(quantity_options)
        #select_quantity.select_by_visible_text(self.amount)

        #choose_quantity=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-results"]').select_by_visible_text(self.amount).click()

        #for option in choose_quantity.find_elements_by_tag_name('option'):
        #    if str(option.text) == self.amount:
        #        option.click()
        #select_quantity=driver.find_element_by_xpath('//*[@id="select2-quantity-proxy-results"]').select_by_visible_text(self.amount)

    def add_to_cart(self):
        #add_to_cart_button=driver.find_element_by_xpath('//*[contains(@id,"product_form_")]')
        add_to_cart_button=driver.find_element_by_xpath('//button[normalize-space()="Add to Cart"]')
        add_to_cart_button.click()

if __name__ == "__main__":

    items=[[1,"Bananas","lb","bananas-lb"],
           [1,"Celery","bunch","celery-bunch-each"],
           [1,"Macintosh Apples","4-to-5-pound-bag","local-apples-4-5-lb-bags?variant=32206638547009"],
           [1,"Kale","bunch","kale-organic-local-black-kale-bunch"],
          ]

    for item in items:
        if item[0] != 0:
            itemToAdd=shopItem(item[0],item[1],item[2],item[3])
            itemToAdd.go_to_url()
            time.sleep(3)
            #ItemToAdd.select_quantity()
            itemToAdd.add_to_cart()
            time.sleep(3)
            print(f"Added {itemToAdd.amount} {itemToAdd.unit} of {itemToAdd.name} to Shopping Cart")
        else:
            print(f"Skipping {item[1]} in this order")


