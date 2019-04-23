import sys
import subprocess
import pandas as pd
import os
import re
from collections import defaultdict
import csv

readfile = sys.argv[1]

file_list=os.listdir(readfile)
df = pd.DataFrame({'image_name':file_list})
df=readfile+df['image_name']
df.to_csv(r'panda.txt', header=None, index=None, sep=' ', mode='a')


"""
bashcalls = ['./darknet', 'detector', 'test', 'cfg/obj.data', 'cfg/yolo-panda.cfg', 'backup/yolo-panda_30000.weights','-dont_show','-ext_output','panda.txt','> results_test.txt']
process = subprocess.Popen(bashcalls, stdout=subprocess.PIPE)
output, error = process.communicate()
"""

os.system("./darknet detector test cfg/obj.data cfg/yolo-panda.cfg backup/yolo-panda_30000.weights -dont_show -ext_output < panda.txt > results_test.txt")  

#os.system("python3 retest.py")
re1='.*?'	# Non-greedy match on filler
re2='(?:\\/[\\w\\.\\-]+)+'	# Uninteresting: unixpath
re3='.*?'	# Non-greedy match on filler
re4='((?:\\/[\\w\\.\\-]+)+)'	# Unix Path 1)'	# File Name 1


re5='.*?'	# Non-greedy match on filler
re6='(-?[\d]+)'	# Integer Number 1
re7='.*?'	# Non-greedy match on filler
re8='(-?[\d]+)'	# Integer Number 1
re9='.*?'	# Non-greedy match on filler
re10='(-?[\d]+)'	# Integer Number 2
re11='.*?'	# Non-greedy match on filler
re12='(-?[\d]+)'	# Integer Number 3
re13='.*?'	# Non-greedy match on filler
re14='(\\d+)'	# Integer Number 3
rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
rnum=re.compile(re5+re6+re7+re8+re9+re10+re11+re12+re13+re14,re.IGNORECASE|re.DOTALL)


d=defaultdict(list)
for line in open("results_test.txt"):
	if (line.startswith("Enter")):	
		m = rg.search(line)
		if m:
			file1=m.group(1)
			var=file1[1:]
			d[var]=list()
	elif(line.startswith("Object")):
		m = rnum.search(line)
		if m:
			int1=int(m.group(2))
			int2=int(m.group(3))
			int3=int(m.group(4))
			int4=int(m.group(5))
			l=[int1,int2,int3,int4]
			d[var].append(l)
			
            
w = csv.writer(open("output_test.csv", "w+"))
for key, val in d.items():
	w.writerow([key,val])

df = pd.read_csv('output_test.csv', header=None)
df.columns=['img_name','list']
a=[]
list_lst=[]
i=0
for row in df['list']:
    a = row.replace('[',' ').replace(']',' ').replace(',',' ').split()
    numbers = [ int(x) for x in a ]
    i+=1
    if numbers:
        numbers=[numbers[i:i + 4] for i in range(0, len(numbers), 4)]
    else:
        numbers=[[160,120,320,240]]
    best_bbox=max(numbers, key=lambda x: x[2]*x[3])
    list_lst.append(best_bbox)
    
results = pd.DataFrame(list_lst,columns=['x','y','W','H'])
results['image_name']= df['img_name']
results['x1']=results['x']+(0.1*results['W'])
results['x2']=results['x']+(0.9*results['W'])
results['y1']=results['y']-(0.17*results['H'])
results['y2']=results['y']+(1.17*results['H'])
results=results.drop(['x','y','W','H'],axis=1)
results = results[['image_name','x1','x2','y1','y2']]
results.to_csv('output_bestbbox.csv')
