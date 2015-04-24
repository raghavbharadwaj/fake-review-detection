import re

rating_class = {
    '1.0': 'negative',
    '2.0': 'negative',
    '3.0': 'neutral',
    '4.0': 'positive',
    '5.0': 'positive',
}
brands = {}
with open("../../datasets/amazon_dataset/"
        +"amazon_cell_phone_brands.txt", 'r') as fh:
    for line in fh:
        line = line.rstrip()
        (product, brand) = line.split(" ", 1)
        brands[product] = brand

fin = open("../../datasets/amazon_dataset/Cell_Phones_&_Accessories.txt")
fout = open("../../datasets/amazon_dataset/cell_phones_preprocessed.txt", 'w')
for line in fin:
    m1 = re.match('product/productId: (.*)', line)
    m2 = re.match('review/userId: (.*)', line)
    m3 = re.match('review/score: (.*)', line)
    if (m1):
        product_id = m1.group(1)
        fout.write(product_id+' ')
        brand = brands[product_id]
        brand = re.sub(" ", "_", brand)
        fout.write(brand+' ')
    elif (m2):
        user_id = m2.group(1)
        fout.write(user_id+' ')
    elif (m3):
        rating = m3.group(1)
        fout.write(rating_class[rating]+'\n')

