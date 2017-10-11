# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import urllib.request as ur
from bs4 import BeautifulSoup as bs

"""
感觉find只会当前目录的数据,
而find_all会挖全部的
"""
#%% Functions ------------------------------------------------------------------------------------
def sold_out(info):
	QG = []
	for k in info.find_all('div', attrs={'class':'jingxuan_main'}):
		temp_name = k.find(name='p', attrs={'class':'jingxuan_tl'}).get_text()[1:-1]
		qg = k.find('div', attrs={'class':'qiangugang'})
		if qg is not None:
			QG.append(temp_name)
	return list(set(QG))



def find_how_many_pages(cate):
    """Find how many sub-pages under a given category. Only used for 51go"""
    i=0
    while True:
        try:
            i+=1
            url = 'https://www.51go.com.au/Category/'+cate+'?pageIndex='+str(i)+'&pageSize=20'
            url_file = ur.urlopen(url)
            info = bs(url_file, 'html.parser')
            used_info = info.find_all(name='p', attrs={'class':'jingxuan_tl'})
            if i > 30:
                print('Categories entered is probably wrong.')
                i = 0
                break
            if used_info != []:
                pass
            else:
                i-=1
                raise TypeError
        except:
            break
    return i

#------------------------------------------------------------------------------------------------
def find_all_products():
    """Find all products with corresponding Url, returned as Pandas DataFrame."""
    cate_pool = {}
    names = []
    url_pool = []
    base_url = 'https://www.51go.com.au'
    c_name = []
    qiang_guang = []
    
    # Find categories
    main_page = ur.urlopen(base_url)
    main_page_bs = bs(main_page, 'html.parser')
    cate_info = main_page_bs.find_all('li', attrs={'class':"popup_parent"})
    # find what categories exists
    for indiv in cate_info:
        cate_name = os.path.basename(indiv.find('a', href=True)['href'])
        cate_pool[cate_name] = find_how_many_pages(cate_name)
        c_name.append(indiv.find('a', href=True).get_text())
    
    # Individual category crawl
    for cate in cate_pool:
        page_quantity = cate_pool[cate]
        if page_quantity == 0:
            continue
        
        for i in range(page_quantity):
            temp_url = 'https://www.51go.com.au/Category/'+cate+'?pageIndex='+str(i+1)+'&pageSize=20'
            url_file = ur.urlopen(temp_url)
            info = bs(url_file, 'html.parser')
            # Sold out or not
            
            temp_qg = sold_out(info)
            for item in temp_qg:
            	qiang_guang.append(item)

            used_info = info.find_all(name='p', attrs={'class':'jingxuan_tl'})
            for thing in used_info:
                new_name = thing.get_text()[1:-1]
                new_url =thing.find('a', href=True)['href']
                names.append(new_name)
                url_pool.append(base_url+new_url)

    final_pool = pd.DataFrame({'Product':names, 'Url':url_pool})
    print('------------------------------------------------------------------------------------------------')  
    print('Product list has been obtained.')
    print('------------------------------------------------------------------------------------------------')
    for i in range(len(cate_pool)):
    	print('{}'.format(c_name[i]))
    print('------------------------------------------------------------------------------------------------')
    print('Totally {} products will be crawled.'.format(len(final_pool)))
    print('{} of them are sold out.'.format(len(qiang_guang)))
    print('------------------------------------------------------------------------------------------------')
    #final_pool.to_excel('P&N.xlsx', header=True,index=False)  # output as Excel file, product name & url
    return final_pool, qiang_guang

#------------------------------------------------------------------------------------------------
def fetch_ind_product(final_pool, qiang_guang):
    names = []
    price = []
    descr = []
    Url = []

    for i in range(len(final_pool)):
        p_name = final_pool.iloc[i,0]
        p_url = final_pool.iloc[i,1]
        
        url_info = bs(ur.urlopen(p_url), 'html.parser')
        p_descr = [k.get_text() for k in url_info.find_all('div', attrs={'class':'pro_con_t_rt_xinx'})][0].strip()[:-1]
        p_price = [k.get_text() for k in url_info.find_all('span', attrs={'class':'color_red bold'})][0]
        
        names.append(p_name)
        price.append(p_price)
        descr.append(p_descr)
        Url.append(p_url)
        if i % int(len(final_pool)/10) == 0:
            print('{}% hss been crawled.'.format(int((i / int(len(final_pool)/10))*10)))
    print('------------------------------------------------------------------------------------------------')

    qg_or_not = []
    for f_product in names:
    	if f_product in qiang_guang:
    		qg_or_not.append('已抢光')
    	else:
    		qg_or_not.append('')


    final_result = pd.DataFrame({'Names':names,
                                 'Prices':price,
                                 'Descriptions':descr,
                                 'Url':Url,
                                 'Sold Out': qg_or_not}, 
                                 columns = ['Sold Out',
                                 			'Names', 
                                           'Prices', 
                                           'Descriptions', 
                                           'Url'])

    return final_result.to_excel('Final_result.xlsx', header=True, index=False)
    

#------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	# try:
	# 	para = sys.argv[1].lower()
	# except IndexError:
	# 	print('\nPlease enter Yes or No after main_crawling.py.')
	# 	exit()
	# if para == 'yes' or para == 'y':
	# 	output = True
	# 	print('\nThe result will be output as excel file with name of Final_result')
	# elif para == 'no' or para == 'n':
	# 	output = False
	# 	print('\nThe result will not be output as excel file with name of Final_result.\nPlease enter Yes or Y if you want to output it.')
	# else:
	# 	print('\nPlease enter Yes or No after main_crawling.py.')
	# 	exit()

    print('\nThe result will be output as excel file with name of Final_result.xlsx')
    final_pool, qiang_guang = find_all_products()
    fetch_ind_product(final_pool, qiang_guang)
    # os.startfile('Final_result.xlsx')

