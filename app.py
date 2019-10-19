from flask import Flask, redirect, url_for, request,render_template, session
from pytrends.request import TrendReq
import pytrends 
from pytrends.request import TrendReq
import pandas as pd
import json  


app = Flask(__name__,template_folder='template')



@app.route('/')
def hello_world():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    a = pytrends.interest_over_time()
    return str(a)

@app.route('/fetch',methods = ['GET'])
def fetch():
    if request.method == 'GET':
        data = request.args.get('name')
        pytrends = TrendReq(hl='en-US', tz=360)
        # Preparing KEYWORD List
        kw_list =[data]
        # Build Payload
        pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='US', gprop='')
        # Get result for interest_over_time
        #return str(pytrends.interest_over_time())
        df =pytrends.interest_over_time()
        df.to_json(r'data.json')
        with open('data.json') as f: 
            d = json.load(f)
            print(d) 
        return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)



if __name__ == '__main__':
    app.run()