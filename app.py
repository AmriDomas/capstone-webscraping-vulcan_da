from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'history-rates-data'})
baris1 = table.find_all('a', attrs={'class':'w'})

row_length = len(baris1)

temp = [] #initiating a list 

for i in range(0, row_length):

    #scrapping process
    Date = table.find_all('a', attrs={'class':'w'})[i].text
    USDolar_IDR = table.find_all('span', attrs={'class':'n'})[i].text
    temp.append((Date, USDolar_IDR))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns=('Date', 'USDolar_IDR'))

#insert data wrangling here
df['Date'] = df['Date'].astype('datetime64[ns]')
df['USDolar_IDR'] = df['USDolar_IDR'].str.replace('$1','')
df['USDolar_IDR'] = df['USDolar_IDR'].str.replace('=','')
df['USDolar_IDR'] = df['USDolar_IDR'].str.replace('Rp','')
df['USDolar_IDR'] = df['USDolar_IDR'].str.replace(',','')
df['USDolar_IDR'] = df['USDolar_IDR'].astype('float64')
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["USDolar_IDR"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)