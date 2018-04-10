# -*- coding: utf-8 -*-
"""
    Finance App
    ~~~~~~
    A stock modelling application.
    :copyright: (c) 2017
"""

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, validators, SelectField


application = Flask(__name__)
application.secret_key = 'donttellnobody'


##### PARAMETERS TO CHANGED GloballY in UI #####

# global_start = datetime.datetime(2017,10,23)
# global_start_ = int(global_start.strftime("%s"))
#
# global_end = datetime.datetime(2018,4,8)
# global_end_ = int(global_end.strftime("%s"))
#
# ## How often to re-allocate ##
# recalibrate_days = 7
#
# ## Window to look back on for momentum ##
# performance_window_days = -14
#
# ## Window to look back on for global volume filter ##
# volume_window_days = 70
#
# ## Number of coins for momentum -- Has to be less than 20 and greater than 3 ##
# coin_universe_filter = 5
#
# ## Number of coins for momentum -- Has to be less than 20 and greater than 3 ##
# coin_allocation = 5
#
# ## Your starting BTC to backtest w/ ##
# global_start_btc = 5



##### PARAMETERS TO CHANGED GloballY in UI #####


class Form(FlaskForm):

    date_start = DateField('Start Date', [validators.Required('Please select a start date')], format='%Y-%m-%d')
    date_end = DateField('End Date', [validators.Required('Please select an end date')], format='%Y-%m-%d')
    recalibrate_days = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")
    volume_window_days = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")

    coin_universe_filter_number = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")

    coin_allocation_number = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")

    performance_window_days = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")

    global_start_btc = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
                                  validators.Length(min=1, max=5)], id = "ticker")




@application.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if request.method == 'POST' and form.validate():

        security = request.form['stock']

        return redirect(url_for('results'))

    return render_template('index.html', form = form)


@application.route('/results')
def results(security1,security2,start_date,end_date):


    return render_template('results.html')




# ## evenutally ##
# @application.route('/results/result/<security1>/<security2>/<start_date>/<end_date>')
# def correlation_result(security1,security2,start_date,end_date):
#
#
#     return render_template('results.html')


# class StockForm(FlaskForm):
#     stock = StringField('Stock', [validators.Required('Start typing ticker symbol and select'),
#                                   validators.Length(min=1, max=5)], id = "ticker")
#     date_start = DateField('Start Date', [validators.Required('Please select a start date')], format='%Y-%m-%d')
#     date_end = DateField('End Date', [validators.Required('Please select an end date')], format='%Y-%m-%d')
#
#
# @application.route('/', methods=['GET', 'POST'])
# def index():
#     form = HomepageForm()
#     if request.method == 'POST' and form.validate():
#
#         security = request.form['stock']
#
#         return redirect(url_for('results', security=security, start_date='2010-09-20',
#                                 end_date='2017-09-19', sma_=20, lma_=80))
#
#     return render_template('index.html', form = form)
#
#
# @application.route('/daysout', methods=['GET', 'POST'])
# def results():
#     form = StockForm()
#     if request.method == 'POST' and form.validate():
#
#         security = request.form['stock']
#         start_date = request.form['date_start']
#         end_date = request.form['date_end']
#
#         return redirect(url_for('daysout_result', security=security, start_date=start_date, end_date=end_date))
#
#     return render_template('daysout.html', form=form)








if __name__ == "__main__":
    application.jinja_env.auto_reload = True
    application.run(debug=True, threaded=True)



