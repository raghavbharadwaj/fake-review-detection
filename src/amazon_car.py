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
        'author_brand': { },
        'classes': {
            'positive': {'total': 0, 'pr': 0},
            'neutral' : {'total': 0, 'pr': 0},
            'negative': {'total': 0, 'pr': 0} 
        },
        'total': 0
}

print("Reading dataset...")
fn = '../../datasets/amazon_dataset/cell_phones_preprocessed.txt'
fh = open(fn, encoding='cp437')
for line in fh:
    line = line.rstrip()
    (product_id, brand, author_id, review_class) = line.split(' ')
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
    author_brand = author_id + '_' + brand
    if author_brand not in calc_data['author_brand']:
        calc_data['author_brand'][author_brand] = {
                'classes': {
                    'positive': {'total': 0},
                    'negative': {'total': 0},
                    'neutral': {'total': 0}
                },
                'total': 0
        }
    calc_data['author'][author_brand]['classes']\
            [review_class]['total'] += 1
    calc_data['author'][author_brand]['total'] += 1
    calc_data['total'] += 1

print("Calculating prior probabilities...")
print('total', calc_data['total'])
for rclass, class_data in calc_data['classes'].items():
    class_data['pr'] = class_data['total']/calc_data['total']
    print(rclass, class_data['total'], class_data['pr'])

print("Calculating one-condition rule unexpectedness...")
total_pr_vja = 0
for author_id, author_data in calc_data['author'].items():
    total_pr_vja += author_data['total']/calc_data['total']
    for c, cdata in author_data['classes'].items():
        confidence = cdata['total']/author_data['total']
                # (1) confidence = Pr(c_i|v_jk)
                # (2) expected confidence = E(Pr(c_i|v_jk)) = Pr(C_i)
                # confidence unexpectedness = ((1) - (2))/(2)
        pr_ci = calc_data['classes'][c]['pr']
        cdata['confidence'] = confidence
        cdata['cu'] = (confidence - pr_ci)/pr_ci

print("Calculating two-condition rule unexpectedness...")
for author_brand, ab_data in calc_data['author_brand'].items():
    for c, cdata in ab_data['classes'].items():
        confidence = cdata['total']/ab_data['total']
                # (1) confidence = Pr(c_i|v_jk)
                # (2) expected confidence = E(Pr(c_i|v_jk)) = Pr(C_i)
                # confidence unexpectedness = ((1) - (2))/(2)
        cdata['confidence'] = confidence


print('Expected support')
for rclass, class_data in calc_data['classes'].items():
    e_pr_vjk_ci = class_data['pr'] * total_pr_vja/len(calc_data['author'])
    print(rclass, e_pr_vjk_ci)

total_above_support_threshold = 0
total_positive_only = 0
total_negative_only = 0

for author_id, author_data in calc_data['author'].items():
    if author_data['total'] >= 3:
        total_above_support_threshold += 1
        if author_data['classes']['positive']['confidence'] == 1.0:
            total_positive_only += 1
        if author_data['classes']['negative']['confidence'] == 1.0:
            total_negative_only += 1
print('Total reviewers above support threshold:', 
        total_above_support_threshold)
print('Total reviewers with positive only reviews:', total_positive_only)
print('Total reviewers with negative only reviews:', total_negative_only)

for author_id, author_data in \
        sorted(calc_data['author'].items(), reverse=True,
        key=lambda author: (author[1]['classes']['positive']['confidence'],
            author[1]['classes']['positive']['total'])):
    print(author_id, author_data['total'])
