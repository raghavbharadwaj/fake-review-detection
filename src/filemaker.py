import sys
import os

source = open('Baby.txt','r')
i=1
for line in source:
	contents=line.split(':')
	if contents[0] == 'review/text':
		review_file = open('review-'+str(i),'w')
		review_file.write(contents[1])
		i=i+1
		review_file.close()
source.close()
