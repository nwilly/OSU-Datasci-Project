import glob,re;

path = './names/'
write_to = open(path+'name_data.csv','w')

files = glob.glob(path+'*.txt');

dic={};

for file in files:
    
    f = open(file,'r')
    data = f.read();
    data = data.split('\n')

    for line in data:
        splt = line.split(',');
        if(len(splt)==3):
            dic[splt[0]+'_'+splt[1]] = dic.get(splt[0]+'_'+splt[1],0) + float(splt[2]);
            


data=[]; #name, prob female, frequency
done={};
total = sum(dic.values());

for key in dic:
    if key[0:-2] in done:
        continue;
        
    female_num = 0;
    male_num = 0;
    
    female_key = key[0:-1]+'F';
    male_key = key[0:-1]+'M';

    
    if female_key in dic:
        female_num = dic[female_key];
    
    if male_key in dic:
        male_num = dic[male_key];
      
        
    probability_female=0;
    if female_num==0:
        if male_num==0:
            continue;
        else:
            probability_female = 0;
    elif male_num==0:
        probability_female = 1;
    else:
        probability_female = female_num / (female_num + male_num);
    
    
    frequency = (male_num+female_num)/total;
    
    data.append(key[0:-2]+','+str(probability_female)+','+str(frequency));
#    done.append(key[0:-2])
    done[key[0:-2]] = 0;


write_to.write('name,probability_female,frequency\n')
data.sort();
for line in data:
    write_to.write(line);
    write_to.write('\n')
    
write_to.close()
        
        
        
        
        
        
        

