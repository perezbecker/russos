from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import gspread
import operator

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


def is_positive_integer(testString):
    try:
        int_testString=int(testString)
        if(int_testString >= 0):
            return True
        else:
            return False
    except:
        return False

def remove_zero_rows(itemList):
    outputList=[]
    for i in range(len(itemList)):
        if(itemList[i][1] == "0" and not is_positive_integer(itemList[i][0])):
            pass
        else:
            outputList.append(itemList[i])
    return outputList

def add_sort_column(itemList):
    i=0
    for item in itemList:
       item.append(i)
       i+=1
    return itemList

def remove_sort_column(itemList):
    for item in itemList:
        item.pop()
    return itemList

def create_sorted_list(itemList,sortIndex):
    sorted_list = sorted(itemList,key=operator.itemgetter(sortIndex))
    return sorted_list

def remove_duplicates(itemList,sortIndex):
    i=0
    listLength=len(itemList)
    while i < listLength-1:
        #print(i)
        if(itemList[i][sortIndex] == itemList[i+1][sortIndex]):
            try:
                int_override=int(itemList[i][0])
                if(int_override >= 0):
                    itemList[i][1]=int_override
                    itemList[i][0]=""
            except:
                pass
            try:
                int_override=int(itemList[i+1][0])
                if(int_override >= 0):
                    itemList[i+1][1]=int_override
                    itemList[i+1][0]=""
            except:
                pass

            mergedItem=["",str(int(itemList[i][1])+int(itemList[i+1][1])),itemList[i][2],itemList[i][3],itemList[i][4],itemList[i][5],itemList[i][6]]
            del itemList[i]
            del itemList[i]
            itemList.insert(i,mergedItem)
            listLength-=1
        else:
            i+=1
    return itemList



if __name__ == "__main__":


    # STEP 1: Get Shopping Lists from Russo's Google Docs
    globalShoppingList=[]
    subtotal=0

    mainShoppingList = shopList(secret_path,"Russos","Main")
    mainShoppingList.remove_headers()
    mainShoppingList.lists_to_include()

    print(f"Shopping from Lists: {[x for x in mainShoppingList.include]}")

    for shoppingList in mainShoppingList.include:
        myitemList = shopList(secret_path,"Russos",shoppingList)
        myitemList.remove_headers()
        for item in myitemList.list:
            globalShoppingList.append(item)

    # STEP 2: Clean up list (consolidate duplicate items together)
    nonZeroShoppingList = remove_zero_rows(globalShoppingList)
    indexedShoppingList = add_sort_column(nonZeroShoppingList)
    sortedShoppingList = create_sorted_list(indexedShoppingList,5)
    dedupedShoppingList = remove_duplicates(sortedShoppingList,5)
    rearrangedShoppingList = create_sorted_list(dedupedShoppingList,6)
    finalShoppingList = remove_sort_column(rearrangedShoppingList)


    # STEP 3: Fill up shopping cart at russos.com
    driver = webdriver.Chrome()
    for item in finalShoppingList:
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
                print(f"Added {itemToAdd.amount} {itemToAdd.unit} of {itemToAdd.name} with unit prize of ${round(float(itemToAdd.cost_per_unit),2)} to Shopping Cart | ${round(cost_for_item,2)}")
            elif(item[1]!='0'):
                print(f"Skipping {item[2]} in this order")
            else:
                pass
        except:
            print(f"Could not find {itemToAdd.name}, please verify URL: {itemToAdd.url}")

    print("――――――――――――――――――――――――――")
    print(f"Expected Subtotal: ${round(subtotal,2)}")
    print("――――――――――――――――――――――――――")
