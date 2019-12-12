from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
def hello():
    import requests
    import json
    import oauth2 as oauth

    consumer_key = ""
    consumer_secret = ""
       
    access_token = ""
    access_token_secret = ""
          
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    access_token = oauth.Token(key=access_token, secret=access_token_secret)
             
    client = oauth.Client(consumer, access_token)
                
    url="https://api.twitter.com/1.1/search/tweets.json?q=bitcoin" 
    response_1, res=client.request(url)
    tweets=json.loads(res)
    username = []
    tweet = []
    dates = []

    for i in tweets['statuses']:
        username.append(i['user']['screen_name'])
        tweet.append(i['text'])
        dates.append(i['created_at'])
                            
    return render_template('bitcoinPredictions.html', finals = zip(username,tweet,dates))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
