#!/bin/bash

for filename in test/*.txt
do
	truthfullm=$(echo perplexity -text $filename | ./evallm -binary a.binlm 2>&1)
	deceptivelm=$(echo perplexity -text $filename | ./evallm -binary b.binlm 2>&1 )
	perplexity_tlm=$(echo $truthfullm | cut -d "=" -f 2 | cut -d "," -f 1 2>&1)
	perplexity_dlm=$(echo $deceptivelm | cut -d "=" -f 2 | cut -d "," -f 1 2>&1)
	
	echo "$filename $perplexity_tlm $perplexity_dlm"
done
