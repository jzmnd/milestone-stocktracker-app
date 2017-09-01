"""
app.py
Flask on Herouku web app for milestone project

Created by Jeremy Smith on 2017-08-29
"""

import os
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request, redirect
from fetchdatalib import getEODprice, generate_date_str
from datetime import date


app = Flask(__name__)
NUMBER_DAYS = 30
PORT = int(os.environ.get("PORT", 33507))


@app.route('/')
def index():

    datetoday = date.today()
    datestr = generate_date_str(datetoday, NUMBER_DAYS)
    data, status = getEODprice('GOOGL', datestr)

    print datetoday.isoformat()
    print data
    print status
    print data.dtypes

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=PORT)
