from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
def hello():
    import requests
    import json
  
    url = "http://34.69.131.19:5000/get_top_users"
    response = requests.get(url)
    topusers = response.json()['result']
    
    url = "http://34.69.131.19:5000/get_popular_users"
    response = requests.get(url)
    popularusers = response.json()['result'][:10]
    return render_template('bitcoinPredictions.html', topusers = topusers,popularusers=popularusers)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
