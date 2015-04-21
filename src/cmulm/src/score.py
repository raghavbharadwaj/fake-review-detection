# takes input from results.txt and shows the score for each file
# deceptive must be prefixed with decep


# this is the format:
#test/decep49.txt  291.59  255.64
#test/decep5.txt  356.19  321.44
#test/decep50.txt  205.82  136.89

total = 0
total_decep = 0
total_truth = 0
decep_right = 0
truth_right = 0
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
			else:
				pass
		else:
			total_truth += 1

			if float(avalue) > float(bvalue):
				truth_right += 1
			else:
				pass

#####################

print ('total = '+ str(total))
print ('total deceptive = '+ str(total_decep))
print ('total truthful = '+ str(total_truth))
print ('decep right = '+ str(decep_right))
print ('truth right = '+ str(truth_right))
print ('Total rate = '+ str(float(decep_right+truth_right)/total))
print ('Truth rate = '+ str(float(truth_right)/total_truth) )
print ('Decep rate = '+  str(float(decep_right)/total_decep) )
