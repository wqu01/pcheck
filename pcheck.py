from flask import Flask, render_template, request, url_for
from BeautifulSoup import BeautifulSoup as BS
import requests
#import urllib2

app = Flask(__name__)

#python code
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
	result_link = soup.findAll('div', {'class':'box'})	
	if result_num == '1':
		product_link = result_link[0].find('a')['href']
		price = getJolsePrice(product_link)
 		return render_template('price_results.html',
			 item_name=item_name, price=price)

	elif result_num == '0':
		return render_template('price_results.html',
			 item_name=item_name, price="not found")

	else:
		links = []
		#search_result = soup.findAll('div', {'class':'box'})
		print "Search Results"
		#result_link = getResults(search_result)
		#should return one result later, only showing multiple results right now
		return getResults(result_link)
		#return "Please select an item"
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

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/items', methods=['POST'])
@app.route('/item/<item_name>', methods=['POST'])
def item():    
	item_name = request.form['item_name']
	#return render_template('search_results.html')
	return getJolseResults(item_name)
	#return render_template('search_results.html',
	#		 item_name=item_name, price=price)

@app.route('/choose', methods=['POST'])
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
