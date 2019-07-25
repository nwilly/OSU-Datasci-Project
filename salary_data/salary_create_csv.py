def salary_create_csv(path):
    
    import glob,time,re
#    path = 'E:/Programs/Python/Python35/Scripts/scrape/raw_data_spring/'
    
    write_to = open(path+'salary_data.csv','w')
    
    write_to.write('name,department,title,total,year_end,annual_base_salary,regular,overtime,bonus,sick_leave_payout,vacation_payout,remaining\n')
    
    print(path+'salary_data.csv')
    
    start = time.time()
    files = glob.glob(path+'*.txt');
    print(len(files))

    for f in range(0,len(files)):
    
        #print(files[f])
        
        if(f%100==0):
            print(f/len(files)*100)
        file = open(files[f],'r');
        data = file.read();
        file.close()
    

        data = re.sub('&nbsp;','NA',data)
        data = re.sub('&amp;','&',data)
        data = re.sub(',',';',data)

        results = re.findall('(?<=d0a">)[^"<]+(?=</td>)',data);

        for i in range(0,len(results)-1,12):
            
            tmp = results[i:i+12];
            
            tmp = ",".join(tmp);
            write_to.write(tmp+'\n')
    
    
    
    write_to.close()
    end = time.time()
    print(end-start)
    
    
