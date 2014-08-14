import pprint
import re

file1 ='/home/moh/mo/test/garbage.txt'
def totsv(myfile):
	myfile= open(myfile,'r+')
	print myfile
	nfile = myfile.read()
	myfile.close()

	p0= re.sub(r'(\d)(\'|-)(\d{1,2})"?( )',r'\1-\3in',nfile)        # uniformises the height by replacing " by in
	p1= re.sub(r'(\d)(-)(\d{7})',r'\1\3',p0)                        # "-" from number in id
	p2= re.sub(r'(-(-+))|[(\+)]+','',p1)                            # remove "+" and remove "-"s when they follow each others
	p3= re.sub(r'( +)(\w*)',r'\2',p2)                               # space in front of words
	p4 =re.sub(r'[\w\.\']+( +)',r'\1',p3)                        # space after of words
	p5= re.sub(r'\|',r'\t',p4)
	myfile1 = open('/home/moh/mo/test/garbage1.tsv','w+')
	myfile2 = open('/home/moh/leaguePlus/app/static/js/mydata.tsv','w+')
	myfile1.write(p5)
	myfile2.write(p5)
	myfile1.close()
	myfile2.close()
	



totsv(file1)




	
