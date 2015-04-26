# takes input from results.txt and shows the score for each file
# deceptive must be prefixed with decep


# this is the format:
#test/decep49.txt  291.59  255.64
#test/decep5.txt  356.19  321.44
#test/decep50.txt  205.82  136.89

total = 0
total_decep = 0 # count_belongs_in deceptive
total_truth = 0 # count_belongs_in truthful
decep_right = 0 # correctly classified as deceptive
truth_right = 0 # correctly classified as truthful
precision_truth = 0
recall_truth = 0;
precision_decep = 0
recall_decep = 0

classified_as_truth = 0
classified_as_decep = 0
with open('results.txt','r') as fp:
	for line in fp:
		total += 1
		lst = line.split()
		filename = lst[0].split('/')[1]
		avalue = lst[1]
		bvalue = lst[2]

		if filename.startswith('decep'):
			total_decep += 1

			if float(avalue) > float(bvalue):
				decep_right += 1
				classified_as_decep += 1
			else:
				classified_as_truth += 1
		else:
			total_truth += 1

			if float(avalue) > float(bvalue):
				truth_right += 1
				classified_as_truth += 1
			else:
				classified_as_decep += 1

#####################

pt = float(truth_right)/classified_as_truth
pd = float(decep_right)/classified_as_decep

rt = float(truth_right)/total_truth
rd = float(decep_right)/total_decep

f1t = float(2*pt*rt)/(pt+rt)
f1d = float(2*pd*rd)/(pd+rd)

print ('total = '+ str(total))
print ('total deceptive = '+ str(total_decep))
print ('total truthful = '+ str(total_truth))
print ('decep right = '+ str(decep_right))
print ('truth right = '+ str(truth_right))
print ('Total rate = '+ str(float(decep_right+truth_right)/total))
print ('Truth rate = '+ str(float(truth_right)/total_truth) )
print ('Decep rate = '+  str(float(decep_right)/total_decep) )
print ('Precision of truthful = ' + str(pt))
print ('Precision of deceptive = ' + str(pd))
print ('Recall of truthful = ' + str(rt))
print ('Recall of deceptive = ' + str(rd))
print ('f1 truth = ' + str(f1t))
print ('f1 deceptive = ' + str(f1d))