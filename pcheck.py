from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup as BS
import requests
#import urllib2
from re import sub
from decimal import Decimal
import os
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

JolseResults = []
RRSResults = []
TKResults = []
globkeyword = ""
#Jolse
class JolseResults(Resource):
     def get(self, item_name):
        home = 'http://jolse.com'
        keyword = item_name
        keyword = keyword.replace(' ', '+')
        site ="http://jolse.com/product/search.html?banner_action=&keyword=" + keyword
        html = requests.get(site)
        soup = BS(html.content, "html.parser")
        elem = soup.findAll('p', {'class': 'record'})
        result_num = elem[0].strong.string
        result_links = soup.findAll('div', {'class':'box'})	
        #if only one result then get and return data
        if result_num == '1':
    	    product_link = result_links[0].find('a')['href']
            JolseData = getJolsePrice(home+product_link)
            return JolseData
        #if no result
        elif result_num == '0':
            return [item_name, "", "", "not found"]

        else: #output multiple results 	
            result_list = []
            for link in result_links:	
        	if(link.find('a')):
    	            mydict = {'link': home+link.find('a')['href'],
    	    	      'title':link.find('a')['title'],
    	    	      'src':link.find('img')['src']}
    	        result_list.append(mydict)
            return [result_list]
#RRS
class RRSResults(Resource):
    def get(self, item_name):
        home = 'http://www.roseroseshop.com'   
        keyword = item_name
        keyword = keyword.replace(' ', '+')
        site ="http://www.roseroseshop.com/index.php?route=product/search&search=" + keyword +"&limit=50"
        html = requests.get(site)
        soup = BS(html.content)
        elem = soup.findAll('span', {'class': 'price-new'})
        if(len(elem)>0):
            if(len(elem) > 2):
                #more than one result
                search_results = soup.findAll('div', {'class': 'col-sm-3 col-xs-6'})
                result_list = []
                for link in search_results:	 
                    if(link.find('a')):
                        mydict = {'link': link.find('a')['href'],
                          'title':link.find('img')['alt'],
                          'src':link.find('img')['src']}
                    result_list.append(mydict) 
                return [result_list]
            else: 
                search_results = soup.findAll('div', {'class': 'image'}, limit=1)
                product_link = search_results[0].find('a')['href'] 
                return getRRSPriceWeight(product_link)

        else: 
            return [item_name, "", "", "not found", "not found"]
#TesterKorea
class TKResults(Resource):
    def get(self, item_name):
        home = 'http://www.testerkorea.com'
        keyword = item_name
        keyword = keyword.replace(' ', '+')
        site = 'http://testerkorea.com/search?q=' + keyword
        html = requests.get(site)
        soup = BS(html.content, "html.parser")
        elem = soup.findAll('div', {'class': 'col-xs-12 item-picture'})
        if(len(elem)>0):
            if(len(elem) > 2):
                result_list = []
                for link in elem:	
                    if(link.find('a')):
                        mydict = {'link': home+link.find('a')['href'],
                          'title':link.find('img')['alt'],
                          'src':link.find('img')['src']}
                    result_list.append(mydict)
                return [result_list]
            else:
                product_link = home+elem[0].find('a')['href']
                getTKPriceWeight(product_link)

        else:
            return [item_name, "", "", "not found", "not found"]


class JolsePrice(Resource):
    #getting the price data from the product page
    def get(self, product_num):
        #home = 'http://jolse.com'  
        #product_link = home + link
        #print product_link
        #print request.args.get('product_num')
        product_link = "http://jolse.com/product/detail.html?" + product_num
        html2 = requests.get(product_link)
        soup2 = BS(html2.content, "html.parser")
        price = soup2.findAll('span', {'id': 'span_product_price_sale'}) 
        title = soup2.title.string
        image = soup2.find('div', {'class': 'keyImg '})
        img_src = image.find('img')['src']
        return [title, product_link, img_src, price[0].text]
class RRSPriceWeight(Resource):
    def get(self, product_link):
        html = requests.get(product_link)
        soup = BS(html.content, "html.parser")
        elem = soup.findAll('div', {'class': 'description'})  
        title = soup.title.string
        weight = elem[0].contents[19] 
        elem_price = soup.findAll('span', {'itemprop': 'price'})
        price = elem_price[0].text
        dollars = Decimal(sub(r'[^\d.]', '', price)) /1160
        dollars = round(dollars, 2)
        img = soup.findAll('div', {'class': 'product-image cloud-zoom'})
        image = img[0].find('img')['src']

        item_data = [title, product_link, image, dollars, weight]
        return item_data
class TKPriceWeight(Resource):
    def get(item, product_link):
        html = requests.get(product_link)
        soup = BS(html.content, "html.parser")
        title_elem = soup.find('div', {'class': 'col-md-12 product-name'})
        title = title_elem.text
        weight_elem = soup.findAll('div', {'class': 'col-md-9 col-xs-9'})
        weight = weight_elem[2].text
        elem_price = soup.find('span', {'class': 'currency retailUSD'})
        price = elem_price.text
        img = soup.find('img', {'id': 'gallery-view'})
        img_src = img['src']
        
        item_data = [title, product_link, img_src, price, weight]
       # print item_data
        return item_data
def getJolsePrice(product_link):
    #home = 'http://jolse.com'	
    #product_link = home + link
    #print product_link
    html2 = requests.get(product_link)
    soup2 = BS(html2.content)
    price = soup2.findAll('span', {'id': 'span_product_price_sale'}) 
    title = soup2.title.string
    image = soup2.find('div', {'class': 'keyImg '})
    img_src = image.find('img')['src']
    return [title, product_link, img_src, price[0].text]

def getRRSPriceWeight(product_link):
    html = requests.get(product_link)
    soup = BS(html.content)
    elem = soup.findAll('div', {'class': 'description'})  
    title = soup.title.string
    weight = elem[0].contents[19] 
    elem_price = soup.findAll('span', {'itemprop': 'price'})
    price = elem_price[0].text
    dollars = Decimal(sub(r'[^\d.]', '', price)) /1160
    dollars = round(dollars, 2)
    img = soup.findAll('div', {'class': 'product-image cloud-zoom'})
    image = img[0].find('img')['src']

    item_data = [title, product_link, image, dollars, weight]
    return item_data

def getTKPriceWeight(product_link):
    html = requests.get(product_link)
    soup = BS(html.content)
    title_elem = soup.find('div', {'class': 'col-md-12 product-name'})
    title = title_elem.text
    weight_elem = soup.findAll('div', {'class': 'col-md-9 col-xs-9'})
    weight = weight_elem[2].text
    elem_price = soup.find('span', {'class': 'currency retailUSD'})
    price = elem_price.text
    img = soup.find('img', {'id': 'gallery-view'})
    img_src = img['src']
    
    item_data = [title, product_link, img_src, price, weight]
    return item_data

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
))
app.jinja_options = jinja_options



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def item():    
    item_name = request.args['item_name']
    return getItemData(item_name)

def getItemData(item_name):
    global globkeyword
    globkeyword = item_name
    #return render_template('search_results.html')
    global JolseResults
    JolseResults = getJolseResults(item_name)
    global RRSResults 
    RRSResults = getRRSResults(item_name)
    global TKResults
    TKResults = getTKResults(item_name)
    return render_template('price_results.html', JolseResults=JolseResults, RRSResults=RRSResults, TKResults=TKResults)

@app.route('/result', methods=['POST'])
def getOne():
    product_link = request.form['choosen']
    item_name=request.form['product_name']
    #if getting result for jolse
    global RRSResults
    global TKResults
    if(product_link.find("jolse")!=-1):
        global JolseResults
        JolseResults = getJolsePrice(product_link)
        return render_template('price_results.html', 
                JolseResults=JolseResults, RRSResults=RRSResults, TKResults=TKResults)
    #if get result for rrs
    elif(product_link.find('roseroseshop')!=-1):
        RRSResults = getRRSPriceWeight(product_link)
        return render_template('price_results.html', 
                JolseResults=JolseResults, RRSResults=RRSResults, TKResults=TKResults)

    elif(product_link.find('testerkorea')!=-1):
        TKResults = getTKPriceWeight(product_link)
        return render_template('price_results.html', 
                JolseResults=JolseResults, RRSResults=RRSResults, TKResults=TKResults)

    #return
api.add_resource(JolseResults, '/jolseresults/<item_name>')
api.add_resource(RRSResults, '/rrsresults/<item_name>')
api.add_resource(TKResults, '/tkresults/<item_name>')
api.add_resource(JolsePrice, '/jolseprice/<product_num>')
api.add_resource(RRSPriceWeight, '/rrsprice/<path:product_link>')
api.add_resource(TKPriceWeight, '/tkprice/<path:product_link>')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)
