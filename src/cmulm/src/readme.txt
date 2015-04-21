Place all the test file in test directory, and place models 'a' and 'b': truthful and deceptive respectively in current directory.
Run $sh classifier.sh

Output format:
filename perplexity_of_truthful perplexity_of_deceptive

To get scores:
$sh classifier.sh > results.txt
$python score.py # It takes results.txt by default
