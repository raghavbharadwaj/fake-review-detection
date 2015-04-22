# 
# Fake reviewer identification
# Author: Arry Fajar Firdaus
#
# Based on the algorithm described in:
#
# Nitin Jindal, Bing Liu and Ee-Peng Lim. "Finding Unusual Review Patterns 
#   Using Unexpected Rules" The 19th ACM International Conference on 
#   Information and Knowledge Management (CIKM-2010, short paper), Toronto, #   Canada, Oct 26 - 30, 2010. 
#
from glob import glob
from collections import defaultdict
calc_data = {
        'author': { },
        'classes': {
            'positive': {'total': 0, 'pr': 0},
            'neutral' : {'total': 0, 'pr': 0},
            'negative': {'total': 0, 'pr': 0} 
        },
        'total': 0
}

print("Reading dataset...")
for fn in glob('../../datasets/tripadvisor_weka/*.txt'):
    fh = open(fn, encoding='cp437')
    for line in fh:
        line = line.rstrip()
        (hotel_id, city_state, author_id, review_class) = line.split(' ')
#        print(hotel_id, city_state, author_id, review_class)
        calc_data['classes'][review_class]['total'] += 1
        if author_id not in calc_data['author']:
            calc_data['author'][author_id] = {
                    'classes': {
                        'positive': {'total': 0},
                        'negative': {'total': 0},
                        'neutral': {'total': 0}
                    },
                    'total': 0
            }
        calc_data['author'][author_id]['classes']\
                [review_class]['total'] += 1
        calc_data['author'][author_id]['total'] += 1
        calc_data['total'] += 1

print("Prior probabilities...")
print('total', calc_data['total'])
for rclass, class_data in calc_data['classes'].items():
    class_data['pr'] = class_data['total']/calc_data['total']
    print(rclass, class_data['total'], class_data['pr'])

print("Calculating unexpectedness...")
cu = {}
for author_id, author_data in calc_data['author'].items():
    if author_data['total'] < 3:
        continue
    for c, cdata in author_data['classes'].items():
        pr_ci_vjk = cdata['total']/author_data['total']
        pr_ci = calc_data['classes'][c]['pr']
        cdata['pr_ci_vjk'] = pr_ci_vjk
        cu[author_id] = (pr_ci_vjk - pr_ci)/pr_ci


