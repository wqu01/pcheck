from flask import Flask, render_template, request, url_for
from BeautifulSoup import BeautifulSoup as BS
import requests
#import urllib2
from re import sub
from decimal import Decimal

app = Flask(__name__)

#Jolse
def getJolseResults(item_name):
    home = 'http://jolse.com'
    #keyword = "blackhead power liquid"
    keyword = item_name
    #print keyword
    keyword = keyword.replace(' ', '+')
    site ="http://jolse.com/product/search.html?banner_action=&keyword=" + keyword
    #print site
    #html = urllib2.urlopen(site)
    html = requests.get(site)
    soup = BS(html.content)
    elem = soup.findAll('p', {'class': 'record'})
    result_num = elem[0].strong.string
    result_links = soup.findAll('div', {'class':'box'})	
    if result_num == '1':
	product_link = result_links[0].find('a')['href']
	price = getJolsePrice(product_link)
 	#return render_template('price_results.html',
	#		 item_name=item_name, price=price)
        return [item_name, price]
    elif result_num == '0':
	#return render_template('price_results.html',
    	#	 item_name=item_name, price="not found")
        return [item_name, "not found"]

    else: #output multiple results 	
        #links = []
    	#search_result = soup.findAll('div', {'class':'box'})
        #print "Search Results"
    	#result_link = getResults(search_result)
    	#should return one result later, only showing multiple results right now
    	#return getResults(result_link)
    	#return "Please select an item"
        result_list = []
        for link in result_links:	
    	#links.append(link.find('a')['href'])
    	    if(link.find('a')):
	        mydict = {'link': link.find('a')['href'],
	    	      'title':link.find('a')['title'],
	    	      'src':link.find('img')['src']}
	        result_list.append(mydict)
        #render_template('choose_results.html', results_list=result_list)
        return [result_list]

def getJolsePrice(link):
    #print "there is one result"
    home = 'http://jolse.com'
    #link = result_link[0].find('a')['href']	
    product_link = home + link
    #print product_link

    #getPrice(product_link)
    #html2 = urllib2.urlopen(product_link)
    html2 = requests.get(product_link)
    soup2 = BS(html2.content)
    price = soup2.findAll('span', {'id': 'span_product_price_sale'})
    #print price[0].text
    return price[0].text

"""
def getResults(search_results):
    result_list = []
    for link in search_results:	
    	#links.append(link.find('a')['href'])
    	if(link.find('a')):
	    mydict = {'link': link.find('a')['href'],
	    	      'title':link.find('a')['title'],
	    	      'src':link.find('img')['src']}
	    result_list.append(mydict)
    return render_template('choose_results.html', results_list=result_list)	
"""

#RRS
def getRRSResults(item_name):
    home = 'http://www.roseroseshop.com'
    #keyword = "[LANEIGE] Time Freeze Intensive Cream - 50ml"
    keyword = item_name
    #print keyword
    keyword = keyword.replace(' ', '+')
    site ="http://www.roseroseshop.com/index.php?route=product/search&search=" + keyword
    html = requests.get(site)
    soup = BS(html.content)
    elem = soup.findAll('span', {'class': 'price-new'})
    if(len(elem)>0):
        if(len(elem) > 2):
            #print "more than one result"
            search_results = soup.findAll('div', {'class': 'image'})
            result_list = []
            for link in search_results:	
    	        #links.append(link.find('a')['href'])
    	        if(link.find('a')):
	            mydict = {'link': link.find('a')['href'],
	    	      'title':link.find('img')['alt'],
	    	      'src':link.find('img')['src']}
	        result_list.append(mydict)
            return [result_list]
        else:
            #price=elem[0]
            #print price
            #only one element so get link then get weight and price
            search_results = soup.findAll('div', {'class': 'image'}, limit=1)
            product_link = search_results[0].find('a')['href']
            #print product_link
            return getRRSPriceWeight(product_link)

    else:
        print "no products found"

def getRRSPriceWeight(product_link):
    html = requests.get(product_link)
    soup = BS(html.content)
    elem = soup.findAll('div', {'class': 'description'})
    #for i in elem:
    title = soup.title.string
    weight = elem[0].contents[19]
    print weight
    elem_price = soup.findAll('span', {'itemprop': 'price'})
    price = elem_price[0].text
    print price
    dollars = Decimal(sub(r'[^\d.]', '', price)) /1160
    dollars = round(dollars, 2)
    item_data = [title, dollars, weight]
    return item_data


@app.route('/')
def index():
    return render_template('index.html')
#@app.route('/items', methods=['POST'])
#@app.route('/item/<item_name>', methods=['POST'])
@app.route('/', methods=['POST'])
def item():    
    item_name = request.form['item_name']
    #return render_template('search_results.html')
    JolseResults = getJolseResults(item_name)
    if(len(JolseResults) > 1):
        item_name = JolseResults[0]
        price = JolseResults[1]
        return render_template('price_results.html',
            item_name=item_name, price=price)
    else:
        result_list = JolseResults[0]
        return render_template('choose_results.html', results_list=result_list)

    RRSResults = getRRSResults(item_name)
    #RRSResults is a list with [title, dollars, weight]


@app.route('/result', methods=['POST'])
def getOne():
    option = request.form['choosen']
    item_name=request.form['product_name']
    print item_name
    #home = 'http://jolse.com'
    price = getJolsePrice(option)
    #html2 = requests.get(home+option)
    #soup2 = BS(html2.content)
    #item_name = str(soup2.title.text)
    #return "spi2"
    return render_template('price_results.html',
		item_name=item_name, price=price)
	
if __name__ == '__main__':
    app.run(debug=True)
