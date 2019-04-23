import re
from collections import defaultdict
import csv

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
			
with open("output_test.csv", "w+") as fil
    w = csv.writer(fil)
    for key, val in d.items():
        w.writerow([key,val])




