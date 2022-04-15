from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	import requests 
	import json

	if request.method == 'POST' :
		ticker = request.POST['ticker']
	
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_8f39116560fb4a94992ddcf96031a137")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error...."
		return render(request, 'home.html', {'api': api})
	
	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Above ^ "})


	


	
def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
	
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added to your portfolio!"))				
			return redirect('add_stock')

	else:	
		ticker = Stock.objects.all()
		# save ticker info from api output into python list ('output list')
		output = []
		# modify to pull multiple stock tickers at the same time
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_8f39116560fb4a94992ddcf96031a137")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."	

		return render(request, 'add_stock.html', {'ticker': ticker, 'output':  output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id) # call database by primary key for id #
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Portfolio!"))
	return redirect(add_stock)


def test(request):
	return render(request, 'test.html', {})


def news(request):
	import requests
	import json
	
	# News API
	#api_request = requests.get('http://newsapi.org/v2/everything?q=stocks&apiKey=</your_api_key>')
	
	# BASIC - Stock News API
	#api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=general&items=50&token=</your_api_key>')
	
	# PREMIUM - Stock News API
	api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=alltickers&items=50&token=</your_api_key>')
	api = json.loads(api_request.content)
	return render(request, 'news.html', {'api': api}) 
	messages.success(request, ("Stock Has Been Deleted"))
	return redirect(add_stock)



#pk_8f39116560fb4a94992ddcf96031a137