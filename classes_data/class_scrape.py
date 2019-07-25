def scrape(br,folder):

    import time
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    import os;
    from selenium.webdriver.support.ui import Select
    
    tab_num = len(br.window_handles)

    phase_list=[]
    subject_list=[];
    career_list=[];
    class_list=[]
    text_list=[]

    for i in range(0,tab_num):
        phase_list.append(0)
        subject_list.append(int(i*240/tab_num))
        career_list.append(0)
        class_list.append(0)
        text_list.append('')

        br.switch_to_window(br.window_handles[i])
        br.get("https://sis.erp.ohio-state.edu/psp/scsosucs/EMPLOYEE/BUCK/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?")


    tab_index=-1
    done=0
    while(done==0):

        tab_index+=1

        if(tab_index==tab_num):
            tab_index=0

        br.switch_to_window(br.window_handles[tab_index])
        time.sleep(.5)
        br.switch_to_frame("ptifrmtgtframe")

        if phase_list[tab_index]==0:#get to add class from main page
            br.get("https://sis.erp.ohio-state.edu/psp/scsosucs/EMPLOYEE/BUCK/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?")
            br.switch_to_frame("ptifrmtgtframe")
            Add_a_Class_Button = br.find_element_by_link_text("Add a Class")
            Add_a_Class_Button.click()
            
            phase_list[tab_index]=1
            
        elif phase_list[tab_index]==1:#look for search button 1
             try:
                Search_Button1 = br.find_element_by_link_text("search")
                Search_Button1.click()
                phase_list[tab_index] = 2
             except NoSuchElementException:
                 pass
             
        elif phase_list[tab_index]==2:#perform search
            try:

                Campus_List = Select(br.find_element_by_id("SSR_CLSRCH_WRK_CAMPUS$0"));
                Subject_List = Select(br.find_element_by_id("SSR_CLSRCH_WRK_SUBJECT_SRCH$1"));
                Career_List = Select(br.find_element_by_id("SSR_CLSRCH_WRK_ACAD_CAREER$3"));
                Open_Box = br.find_element_by_name("SSR_CLSRCH_WRK_SSR_OPEN_ONLY$4")

                Campus_List.select_by_visible_text("Columbus")
                time.sleep(1)

                Subject_List.select_by_index(subject_list[tab_index]+1)
                time.sleep(1)

                Career_List.select_by_index(career_list[tab_index]+1)
                time.sleep(1)

                Open_Box.click()
                time.sleep(1)
    
                SearchButton2 = br.find_element_by_link_text("Search")
                SearchButton2.click()

                career_list[tab_index]+=1

                if(career_list[tab_index]>7):
                    career_list[tab_index]=0
                    subject_list[tab_index]+=1

                phase_list[tab_index]=3
 
            except NoSuchElementException:
                time.sleep(.05)
            except StaleElementReferenceException:
                time.sleep(.05)

        elif phase_list[tab_index]==3:#search results
            try:
                Class_Button0 = br.find_element_by_id("MTG_CLASS_NBR$"+str(0));

                try:
                    Class_Button = br.find_element_by_id("MTG_CLASS_NBR$"+str(class_list[tab_index]))
                    text = Class_Button.text
                    if(os.path.isfile(folder+text+".txt")):
                        class_list[tab_index]+=1
                    else:
                        text_list[tab_index] = Class_Button.text;
                        Class_Button.click();
                        phase_list[tab_index] = 4
                        
                except NoSuchElementException:
                    class_list[tab_index]=0
                    phase_list[tab_index]=0

            except NoSuchElementException:
                if(class_list[tab_index]==0):
                    try:
                        No_Results = br.find_element_by_id("DERIVED_CLSMSG_ERROR_TEXT");
                        
                        if(No_Results.text == 'Your search will exceed the maximum limit of 300 sections.  Specify additional criteria to continue.'):
                            print("OVERFLOW ERROR: "+str(subject_list[tab_index])+", "+str(career_list[tab_index]));

                        Clear_Button = br.find_element_by_link_text("Clear")
                        Clear_Button.click()

                        phase_list[tab_index] = 2

                    except NoSuchElementException:
                        time.sleep(.05)
                else:
                    time.sleep(.05)


        elif phase_list[tab_index]==4:#class page
            try:
                Return_Button = br.find_element_by_link_text("View Search Results");
                innerHTML = br.execute_script("return document.body.innerHTML");
                file = open(folder+text_list[tab_index]+".txt","w");
                file.write(innerHTML);
                file.close();

                class_list[tab_index]+=1
            
                Return_Button.click();
                phase_list[tab_index] = 3
            except NoSuchElementException:
                time.sleep(.05)

