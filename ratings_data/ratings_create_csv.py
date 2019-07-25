import glob, re

files = glob.glob('e:/code/datasci/scrape/prof_rate/'+'*.txt');
write_to = open('e:/code/datasci/scrape/osu_ratings.csv','w');

for f in range(len(files)):
    
    print(files[f])
    file = open(files[f], encoding='utf8');
    data = file.read();
    file.close();

    fname = re.findall('(?<="pfname">)[^"<]+(?=</span>)',data);
    lname = re.findall('(?<="plname">)[^"<]+(?=</span>)',data);
    title = re.findall('(?<="result-title">)[^"<]+(?=<br>)',data);

    write_to.write(fname[0].strip()+','+fname[1].strip()+','+lname[0].strip()+','+title[0].strip()+',');
  
#    try:
#        write_to.write(fname[0].strip()+','+fname[1].strip()+','+lname[0].strip()+','+title[0].strip()+',');
#    except UnicodeEncodeError as e:
#        print(files[f])
#        continue;
    #overall quality, would take again, level of difficulty 
    overall_ratings = re.findall('(?<="grade" title="">)[^"<]+(?=</div>)',data);    
    for rate in overall_ratings:
        write_to.write(rate.strip()+',');
    
    
    number_ratings = re.findall('(?<=="rating-filter">)[^/]+(?=Student Ratings)',data)
    write_to.write(number_ratings[0].strip()+',')
    
    #all tags in form
    #tag_name <b>(#)
    #converted to tag_name1:#;;tag_name2:#;;...
    tags = re.findall('(?<="tag-box-choosetags">)[^/]+(?=</b>)',data);
    tags = ';;'.join(tags);
    tags = tags.replace(' <b>(',':');
    tags = tags.replace(')','');
    
    write_to.write(tags+',');
    
    
    
    comments = re.findall('(?<=data-report-text=")[^/]+(?=">)',data);
    comments = ';;'.join(comments);
    comments = comments.replace(',','/comma')
    comments = comments.replace('\n','')
    write_to.write(comments+'\n')
    
    
write_to.close();
    

        

    