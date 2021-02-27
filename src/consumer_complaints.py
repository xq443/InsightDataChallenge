#-*- coding: utf-8 -*-
import csv

file_in = open(r'./input/complaints.csv', 'r' )
reader = csv.reader(file_in, delimiter=',', quotechar='"', doublequote=True)
i = 0
info = {}
for row in reader:
    #index of line
    i = i+1
    #print i
    if i%100000 == 0:
    	print 'now calculating',i
    if i == 1:
        continue
    else:
        try:
            date_received, product, sub_product, issue, sub_issue, consumer_complaint_narrative, company_public_response, company, state, zip_code, tags, \
            consumer_consent_provided, submitted_via, date_sent_to_company, company_response_to_consumer, timely_response, consumer_disputed, complaint_id \
            = row
            product = product.lower()
            company = company.lower()
            if product not in info:
                info[product] = {}
            year = date_sent_to_company.split('-')[0]
            if year not in info[product]:
                info[product][year] = [0, {}, 0]
            info[product][year][0] += 1
            if company not in info[product][year][1]:
                info[product][year][1][company] = 0
            info[product][year][1][company] += 1
        except Exception as msg:
            print ('error occured that %s:\n%s' %(msg,row))
            print len(row)
            for word in row:
            	print '--',word
            break
        else:
            pass
file_in.close()

#highest percentage (rounded to the nearest whole number) of total complaints filed against one company for that product and year
for product in info:
    for year in info[product]:
        for company in info[product][year][1]:
            info[product][year][2] = max(info[product][year][2], int( round( float(info[product][year][1][company]) / float(info[product][year][0]) * 100 )) )
        

file_out = open(r'./output/report.csv', 'w')
info_sort = sorted(info.iteritems(), key = lambda d:d[0])
for item in info_sort:
    product = item[0]
    sorted_item = sorted(item[1].iteritems(), key = lambda d:d[0], reverse = True )
    for item_1 in sorted_item:
        year = item_1[0]
        if ',' in product:
            product_name = '"' + product + '"'
        else:
            product_name = product
        file_out.write('%s, %s, %s, %s, %s\n' %(product_name, year, info[product][year][0], len(info[product][year][1]), info[product][year][2]))
file_out.close()
