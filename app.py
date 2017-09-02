"""
app.py
Flask on Herouku web app for milestone project

Created by Jeremy Smith on 2017-08-29
"""

import os
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE
from flask import Flask, render_template, request
from fetchdatalib import getEODprice, generate_date_str
from datetime import date


app = Flask(__name__)

NUMBER_DAYS = 30
PORT = int(os.environ.get('PORT', 33507))
DEFAULT_TICKER = 'GOOGL'
GRAPHTYPLIST = [{'value': 'close', 'name': "Close"},
                {'value': 'open', 'name': "Open"},
                {'value': 'hlc', 'name': "High-Low-Close"}]
DEFAULT_GRAPHTYP = 'close'


@app.route('/', methods=['GET', 'POST'])
def index():
    datetoday = date.today()
    datestr = generate_date_str(datetoday, NUMBER_DAYS)

    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        graphtyp = request.form['graphtyp']
    else:
        ticker = DEFAULT_TICKER
        graphtyp = DEFAULT_GRAPHTYP

    data, status = getEODprice(ticker, datestr)

    fig = figure(title="Ticker: {}".format(ticker),
                 x_axis_type='datetime', x_axis_label='Date', y_axis_label='Price (USD)',
                 height=200, width=600,
                 responsive=True)

    if graphtyp == 'close':
        fig.line(data.date.values, data.close.values, line_width=3)
    elif graphtyp == 'open':
        fig.line(data.date.values, data.open.values, line_width=3)
    elif graphtyp == 'hlc':
        fig.line(data.date.values, data.high.values, line_width=3, line_color='lightgray')
        fig.line(data.date.values, data.low.values, line_width=3, line_color='lightgray')
        fig.line(data.date.values, data.close.values, line_width=3)

    script, div = components(fig)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    html = render_template('index.html', plot_script=script, plot_div=div,
                           js_resources=js_resources, css_resources=css_resources,
                           ticker=ticker, graphtyp=graphtyp, graphtyps=GRAPHTYPLIST)

    return encode_utf8(html)


if __name__ == '__main__':
    app.run(port=PORT)
