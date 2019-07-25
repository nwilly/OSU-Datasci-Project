from selenium import webdriver
import time
import codecs
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import os.path
import string

br = webdriver.Chrome()

br.get('https://www.bizjournals.com/columbus/datacenter/osu-salaries-database-for-year-end-2015-2014-and.html')

iframe = br.find_element_by_css_selector('iframe.embedded-object.clearfix.js-init')
br.switch_to_frame(iframe)

year_field = br.find_element_by_id('Value5_1')
year_field.send_keys('2017')

time.sleep(.5)

search_button = br.find_element_by_id('searchID')
search_button.click()

class_name = input('name of button class:')

count=1

while(1==1):

    innerHTML = br.execute_script("return document.body.innerHTML");
    file = codecs.open('e:/osu_pay_2017/'+str(count)+'.txt',"w",'utf-8');
    file.write(innerHTML)
    file.close()

    try:
        next_button = br.find_element_by_css_selector("a."+class_name+"[data-cb-name='JumpToNext']")
        next_button.click()
        time.sleep(1)
    except NoSuchElementException as e:
        print(e)
        break
    
    
    count+=1

#<a data-cb-name="JumpToNext" href="https://www.bizjournals.com/columbus/datacenter/osu-salaries-database-for-year-end-2015-2014-and.html?s=embeddeditem&amp;appSession=47G8H3703MV317H7F3N453F3HN9Z7VDXM7GL914B0PX1AZPNS0RQQ2BCU3352V1P62XJT9G9H3FPZ06B3Z57V550A6Z2HR7N2676PKB155V48G9GUO8JV56643NCJV2J&amp;PageID=2&amp;PrevPageID=2&amp;cpipage=1707&amp;CPISortType=&amp;CPIorderBy=" class="cbResultSetNavigationLinks_5dbd5b3f262ee1"><img src="https://b3.caspio.com/images/set1_next.gif" alt="Next" border="0"></a>
#.cbResultSetNavigationLinks_67c1f1266dc112