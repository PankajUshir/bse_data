from flask import Flask, render_template
from bsedata.bse import BSE
from flask_socketio import SocketIO, emit
import eventlet

from utils import capitalize_words
from constants import defaultCategories

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
b = BSE()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/get-company-name-by-quote")
def allData():
    b.updateScripCodes()
    data = b.getQuote('543932') #script code in top gainer data
    return data

@app.route("/top-gainers")
def topGainers():
    data = b.topGainers()
    return render_template('top_gainers.html', topGainers=data)

@app.route("/top-losers")
def topLosers():
    data = b.topLosers()
    return render_template('top_losers.html', topLosers=data)

@app.route("/scrip-codes")
def scripCodes():
    b.updateScripCodes()
    data = b.getScripCodes()
    for code in data.keys():
        data[code] = capitalize_words(data[code])
    return render_template('scrip_code.html',scripCodes=data)

@app.route("/get-indices", defaults={"category": None})
@app.route("/get-indices/<string:category>")
def getIndices(category):
    if not category:
        return render_template('indices.html', defaultCategories=defaultCategories)
    record = next((record for record in defaultCategories if record['link'] == category), None)
    if not record:
        return render_template('404.html'), 404
    categoryName = record['name'] if record else category
    data = b.getIndices(category=categoryName)
    return render_template('indices.html', categoryTitle=record['alias'], indicesDetails=data, defaultCategories=defaultCategories)


if __name__ == "__main__":
    socketio.run(app,debug=True, port=5000) 