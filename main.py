from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import gspread

russos_base_url="https://russos.com/collections/collection-of-products/products/"
secret_path="../secrets/russos.json"
PLT = 1


class shopList:

    def __init__(self,secret_path,spreadsheet,worksheet):

        gc = gspread.service_account(secret_path)
        self.list = gc.open(spreadsheet).worksheet(worksheet).get_all_values()

    def remove_headers(self,numberOfLines=2):
        del self.list[:numberOfLines]

    def lists_to_include(self):
        includeList = []
        for item in self.list:
            if(item[1]=='1'):
                includeList.append(item[0])
        self.include = includeList


class shopItem:

    def __init__(self,override,amount,name,unit,cost_per_unit,url):
        self.override=override
        self.amount=amount
        self.name=name
        self.unit=unit
        self.cost_per_unit = cost_per_unit
        self.url=russos_base_url+url
        self.shop=False

    def decide_if_override(self):
        try:
            int_override=int(self.override)
            if(int_override >= 0):
                self.amount = self.override
        except:
            pass

    def decide_if_shop(self):
        try:
            int_amount=int(self.amount)
            if(int_amount > 0):
                self.shop = True
            else:
                self.shop = False
        except:
            self.shop = False

    def go_to_url(self):
        driver.get(self.url)

    def go_to_cart(self):
        driver.get("https://russos.com/cart")

    def update_quantity(self,itemLine=1):
        driver.get(f"https://russos.com/cart/change?line={str(itemLine)}&quantity={str(self.amount)}")

    def add_to_cart(self):
        #add_to_cart_button=driver.find_element_by_xpath('//*[contains(@id,"product_form_")]')
        add_to_cart_button=driver.find_element_by_xpath('//button[normalize-space()="Add to Cart"]')
        add_to_cart_button.click()

if __name__ == "__main__":


    globalShoppingList=[]
    subtotal=0

    mainShoppingList = shopList(secret_path,"Russos","Main")
    mainShoppingList.remove_headers()
    mainShoppingList.lists_to_include()

    print(f"Shopping from Lists: {[x for x in mainShoppingList.include]}")

    for shoppingList in mainShoppingList.include:
        itemList = shopList(secret_path,"Russos",shoppingList)
        itemList.remove_headers()
        for item in itemList.list:
            globalShoppingList.append(item)



   # TO DO: CONSOLIDATE ITEMS: 2 BANANAS. 



    driver = webdriver.Chrome()
    for item in globalShoppingList:
        itemToAdd=shopItem(item[0],item[1],item[2],item[3],item[4],item[5])
        itemToAdd.decide_if_override()
        itemToAdd.decide_if_shop()
        try:
            if itemToAdd.shop:
                itemToAdd.go_to_url()
                time.sleep(PLT)
                itemToAdd.add_to_cart()
                time.sleep(PLT)
                itemToAdd.go_to_cart()
                time.sleep(PLT)
                if(itemToAdd.amount != "1"):
                    itemToAdd.update_quantity()
                    time.sleep(PLT)
                else:
                    pass
                cost_for_item=float(itemToAdd.amount)*float(itemToAdd.cost_per_unit)
                subtotal = subtotal + cost_for_item
                print(f"Added {itemToAdd.amount} {itemToAdd.unit} of {itemToAdd.name} to Shopping Cart | ${cost_for_item}")
            else:
                print(f"Skipping {item[2]} in this order")
        except:
            print(f"Could not find {itemToAdd.name}, please verify URL: {itemToAdd.url}")

    print(f"Expected Subtotal: ${subtotal}")
