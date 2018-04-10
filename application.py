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

    choices1 = []
    for i in range(4, 56):
        choices1.append((i, i))

    choices2 = []
    for i in range(10, 140):
        choices2.append((i, i))

    choices3 = []
    for i in range(5, 70):
        choices3.append((i, i))

    choices4 = []
    for i in range(3, 70):
        choices4.append((i, i))

    choices5 = []
    for i in range(2, 98):
        choices5.append((i, i))

    choices6 = []
    for i in range(1, 20):
        choices6.append((i, i))

    recalibrate_days = SelectField('Recalibration Days', choices=choices1, coerce=int, default=7)

    volume_window_days = SelectField('Volume Lookback Days', choices=choices2, coerce=int, default=70)



    coin_universe_filter_number = SelectField('Top N Coins By Volume Universe ', choices=choices3, coerce=int, default=20)



    coin_allocation_number = SelectField('Top N Coins To Weight', choices=choices4, coerce=int, default=10)



    performance_window_days = SelectField('Momentum Lookback Days', choices=choices5, coerce=int, default=21)



    global_start_btc = SelectField('Amount Of BTC At Start', choices=choices6, coerce=int, default=1)


@application.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if request.method == 'POST' and form.validate():

        date_start_ = request.form['date_start']
        date_end_ = request.form['date_end']
        recalibrate_days_ = int(request.form['recalibrate_days'])
        volume_window_days_ = int(request.form['volume_window_days'])
        coin_universe_filter_number_ = int(request.form['coin_universe_filter_number'])
        coin_allocation_number_ = int(request.form['coin_allocation_number'])
        performance_window_days_ = int(request.form['performance_window_days'])
        global_start_btc_ = int(request.form['global_start_btc'])

        return redirect(url_for('results', date_start_ = date_start_, date_end_ = date_end_,
                    recalibrate_days_ = recalibrate_days_, volume_window_days_ = volume_window_days_,
                    coin_universe_filter_number_ = coin_universe_filter_number_,
                    coin_allocation_number_ = coin_allocation_number_,
                    performance_window_days_ = performance_window_days_,
                    global_start_btc_ = global_start_btc_))

    return render_template('index.html', form=form)


@application.route('/results/<date_start_>/<date_end_>/<int:recalibrate_days_>/'
                   '<int:volume_window_days_>/<int:coin_universe_filter_number_>/<int:coin_allocation_number_>'
                   '/<int:performance_window_days_>/<int:global_start_btc_>')
def results(date_start_,date_end_,recalibrate_days_,volume_window_days_,coin_universe_filter_number_,
            coin_allocation_number_,performance_window_days_,global_start_btc_):

    print(type(date_start_))
    print(type(date_end_))
    print(type(recalibrate_days_))
    print(type(volume_window_days_))


    print(date_start_)
    print(date_end_)
    print(recalibrate_days_)
    print(volume_window_days_)


    return render_template('results.html')












if __name__ == "__main__":
    application.jinja_env.auto_reload = True
    application.run(debug=True, threaded=True)



