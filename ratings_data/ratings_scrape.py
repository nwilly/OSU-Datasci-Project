#this script goes through every professor listed under OSU on ratemyprofessor.

#it first goes to a search result page which contains all of the professors
#associated with OSU.  However this page will not actually load all the results.
#(there are a lot).  So it navigates through links which allow you to view just
#the professors whose last name begins with that letter.

#On the letter filtered search results page, still all the professors won't be
#loaded.  You must repeatedly click the 'load more' button.

#once it has identified that it has loaded all the professors, it saves the urls
#linking to each of them.

#it follows each link to a professor's ratings page.  Again not all the ratings
#are loaded until you repeatedly click a 'load more' button at the bottom of the
#page.

#when it has finally loaded all of a professors ratings, it saves the inner html
#as a text file


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

import os.path
import string
import time
import codecs



#list of letters used to sequentially use letter filter buttons
letters =  list(string.ascii_uppercase) 
#you can easily start from later in the alphabet if you need to restart after
#an incomplete run e.g. 
letters = letters[10:]

#this url is to the results page of OSU professors
#note: you could easily change this url to the search results of another school
#if you so desired and scrape all the ratings of a different university.
search_result_url = 'http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=The+Ohio+State+University&schoolID=724&queryoption=TEACHER';

#this is the folder where the data is saved
output_path = 'e:/prof_rate/'

#start automation browser
br = webdriver.Chrome()


#loop through letters sequentially
for letter in letters:

    #list used to store all professor page urls
    url_list = []
    
    #goto search results page
    br.get(search_result_url)
    time.sleep(3)#just in case of browser hangups
    
    #find and click letter filter button
    letter_button = br.find_element_by_link_text(letter)
    time.sleep(3)
    letter_button.click()
    
    print(letter_button.text)#im a sucker for progress bars
    
    #this is an interactable element on the left panel (where the search results
    #are located). This element allows me to send commands to the results rather
    #than the body of the page.
    temp = br.find_element_by_partial_link_text(',')
    
    
    #click on 'load more' results button until all results are loaded
    can_load_more=1
    count=0
    while(can_load_more==1):
        #print(count)
        try:
            #try to find the 'load more' button
            more = br.find_element_by_css_selector('div.content')
            #if the button is found, click it!
            more.click()
            
            time.sleep(.25)#just in case
            
            #loacte another left panel element
            temp = br.find_element_by_partial_link_text(',')
            
            #this loop scrolls the left panel to the very top.  There is a (broken?)
            #footer on this page which will, upon reaching the bottom of the page,
            #extend upwards until it covers all other elements, making them non-
            #interactable.  By scrolling up and then back down, I found I could prevent
            #this from happeneing.
            q=0;
            while(q<100):
                temp.send_keys(Keys.PAGE_UP)
                q=q+1;
            
            count+=1
            
            #if there is no 'load more' element, then all results are accessible
        except NoSuchElementException as e:
            can_load_more=0
            print(e)
            
            #if there is no 'load more' element, then all results are accessible
        except ElementNotVisibleException as e:
            can_load_more=0
            print(e)
            
            #this is the error that results when there exists a 'load more' button
            #but it is currently off screen or otherwise occluded.  Since, it first
            #scrolled to the top of the panel, it can now scroll downward confident
            #that it will eventually see the button.  So we scoot down a bit and
            #continue the loop to try to find the button again.
        except WebDriverException as e:
            try:
                temp = br.find_element_by_partial_link_text(',')
                temp.send_keys(Keys.ARROW_DOWN)
                time.sleep(.1)
                
                #if the browser locks up, this can happen
            except StaleElementReferenceException as e:
                pass
    
    #find all the professor links. They all have text last_name, first_name, thus
    #all links have a comma in the link text
    link_list = br.find_elements_by_partial_link_text(',')
    
    #save urls to url_list
    for el in link_list:
        url_list.append(el.get_attribute('href'))
    
    print('Done finding urls!!!!')
    
    #loop through each professor url
    for i in range(0,len(url_list)):
        url = url_list[i]#just for code simplification
        
        #go to professor's ratings page, but don't be discouraged by browser
        #timing out
        loaded=0;
        while(loaded==0):
            try:
                br.get(url)
                loaded=1;
                #try again if throws TimeoutException
            except TimeoutException as e:
                print(e)
        
        #locate the main header of the professor's ratings page
        try:      
            name_header = br.find_element_by_css_selector('h1.profname')
            
        #weirdly, there are professors listed, who have no ratings whatsoever.
        #These aren't at all useful, so I don't save them.  These 'no ratings'
        #pages have no main header, so failing to find one means you are on
        #a page with no ratings.
        except NoSuchElementException as e:
            print('no results '+str(i)+"/"+str(len(url_list)))
            continue
        
        #generate a file name out of the header text and remove any problematic
        #characters (ones that mess up a file path).
        file_name = name_header.text;
        file_name = file_name.replace("\"",".");
        file_name = file_name.replace("/"," ");


        #delicious, delicious progress
        print(file_name+" "+str(i)+"/"+str(len(url_list)))
        
        #if the file already exists for whatever reason, skip it
        if(os.path.isfile(output_path+file_name+'.txt')):
            continue
        
        #similar to above, loop until the 'load more' button no longer exists.
        #Or, more accurately, it exists but has no text.
        can_load_more=1
        while(can_load_more==1):
        
            try:
                more = br.find_element_by_id('loadMore')
                if(more.text==''):
                    break
                
                more.click()
                
                
                time.sleep(.25)
            except NoSuchElementException:
                can_load_more=0
            except ElementNotVisibleException:
                more.send_keys(Keys.ARROW_DOWN)
                time.sleep(.25)
            except WebDriverException:
                more.send_keys(Keys.ARROW_DOWN)
                time.sleep(.25)
        
        #grab inner html and save it to a new text file in the output directory
        innerHTML = br.execute_script("return document.body.innerHTML");
        file = codecs.open(output_path + file_name + '.txt',"w",'utf-8');
        file.write(innerHTML)
        file.close()

#close browser
br.close()

    

        
