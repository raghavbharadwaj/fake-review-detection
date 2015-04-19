# TripAdvisor dataset preprocessing script
# 
# Arry Fajar Firdaus
#
# Preprocess TripAdvisor dataset [1] into format suitable for Weka Class 
# Association Rule (CAR) [2] input
#
# [1] Hongning Wang, Yue Lu and ChengXiang Zhai. Latent Aspect Rating Analysis without Aspect Keyword Supervision. The 17th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD'2011), P618-626, 2011. http://times.cs.uiuc.edu/~wang296/Data/LARA/TripAdvisor/TripAdvisorJson.tar.bz2
# [2] Liu, B., Hsu W., and Ma Y. Integrating classification and association rule mining. KDD, 1998. 
#
import json
import pprint
import glob
import re
from os.path import basename, splitext
rating_class = {
        '0': 'negative',
        '1': 'negative',
        '2': 'negative',
        '3': 'neutral',
        '4': 'positive',
        '5': 'positive', }
dataset_dir = "datasets/tripadvisor_json/"
output_dir = "datasets/tripadvisor_weka/"
for fn in sorted(glob.glob(dataset_dir + '*.json')):
    base_fn = basename(fn)
    hotel_id = splitext(base_fn)[0]
    with open(fn, 'r') as f:
        hotel = json.load(f)
    city = ''
    state = ''
    if 'Address' in hotel['HotelInfo']:
        m = re.search('<span property="v:locality">(.*?)</span>', \
                hotel['HotelInfo']['Address'])
        if (m):
            city = m.group(1)
        m = re.search('<span property="v:region">(.*?)</span>', \
                hotel['HotelInfo']['Address'])
        if (m):
            state = m.group(1)
    f = open(output_dir + hotel_id + '.txt', 'w', encoding="utf-8")
    for review in hotel['Reviews']:
        author_id = review['Author']
        if author_id == 'A TripAdvisor Member':
            continue
        review_class = \
            rating_class[str(round(float(review['Ratings']['Overall'])))]
        f.write("%s %s-%s %s %s\n" % \
                (hotel_id, city, state, author_id, review_class))
    f.close()
