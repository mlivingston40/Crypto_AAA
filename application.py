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

from Math.trade_days import *
from Math.trades import *
# from Data.poloniex import *
from Data.mysql_poloniex import *
import numpy as np
import pandas as pd
import time


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


# @application.route('/results/<date_start_>/<date_end_>/<int:recalibrate_days_>/'
#                    '<int:volume_window_days_>/<int:coin_universe_filter_number_>/<int:coin_allocation_number_>'
#                    '/<int:performance_window_days_>/<int:global_start_btc_>')
# def results(date_start_,date_end_,recalibrate_days_,volume_window_days_,coin_universe_filter_number_,
#             coin_allocation_number_,performance_window_days_,global_start_btc_):
#
#
#
#
#     TD = TradeDays(date_start_,date_end_,volume_window_days_,performance_window_days_,recalibrate_days_).trade_days_df()
#
#
#
#
#
#
#     return render_template('results.html')



@application.route('/results/<date_start_>/<date_end_>/<int:recalibrate_days_>/'
                   '<int:volume_window_days_>/<int:coin_universe_filter_number_>/<int:coin_allocation_number_>'
                   '/<int:performance_window_days_>/<int:global_start_btc_>')
def results(date_start_,date_end_,recalibrate_days_,volume_window_days_,coin_universe_filter_number_,
            coin_allocation_number_,performance_window_days_,global_start_btc_):

    start = time.time()

    master_data = Data(date_start_, date_end_, volume_window_days_).master_df()
    print("done getting data")

    trades_days_df = TradeDays(date_start_,date_end_,volume_window_days_,performance_window_days_,recalibrate_days_).trade_days_df()

    trades = Trades(master_data,date_start_,date_end_,volume_window_days_,performance_window_days_,coin_universe_filter_number_,coin_allocation_number_,global_start_btc_)

    first_allocation = trades.first_position()
    print("done w/ first allocation")

    for i in range(0, len(trades_days_df)):

        if i == 0:

            trade_ports, btc_bag = trades.position_profit(trades.global_date_start_datetime_ts,
                                                         trades_days_df.Trade_Date_ts[0].item(), first_allocation)
            trade_ports['Week'] = trades_days_df.Trade_Number[0]
            allocation = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[0].item(), trades_days_df.Trade_Date_ts[0].item(),
                                                trades_days_df.Performance_LB_Start_ts[0].item(), trades_days_df.Trade_Date_ts[0].item(),
                                                btc_bag)

        elif i == len(trades_days_df)-1:

            trade_port, btc_bag = trades.position_profit(trades_days_df.Trade_Date_ts[i - 1].item(),
                                                         trades_days_df.Trade_Date_ts[i], allocation)
            trade_port['Week'] = trades_days_df.Trade_Number[i]
            trade_ports = trade_ports.append(trade_port)
            allocation = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[i].item(), trades_days_df.Trade_Date_ts[i].item(),
                                                trades_days_df.Performance_LB_Start_ts[i].item(), trades_days_df.Trade_Date_ts[i].item(),
                                                btc_bag)

            trade_port, final_btc_bag = trades.last_position_profit(allocation, trades_days_df.Trade_Date_ts.tail(1).item())
            trade_port['Week'] = trades_days_df.Trade_Number[i] + 1
            trade_ports = trade_ports.append(trade_port)


        else:

            trade_port, btc_bag = trades.position_profit(trades_days_df.Trade_Date_ts[i - 1].item(),
                                                         trades_days_df.Trade_Date_ts[i], allocation)
            trade_port['Week'] = trades_days_df.Trade_Number[i]
            trade_ports = trade_ports.append(trade_port)
            allocation = trades.trade_positions(trades_days_df.Volume_LB_Start_ts[i].item(), trades_days_df.Trade_Date_ts[i].item(),
                                                trades_days_df.Performance_LB_Start_ts[i].item(), trades_days_df.Trade_Date_ts[i].item(),
                                                btc_bag)

    end = time.time()
    print(end - start)
    print(final_btc_bag)
    return trade_ports.to_html()



# @app.route('/analysis/<filename>')
# def analysis(filename):
#     x = pd.DataFrame(np.random.randn(20, 5))
#     return render_template("analysis.html", name=filename, data=x.to_html())
#                                                                 # ^^^^^^^^^





if __name__ == "__main__":
    application.jinja_env.auto_reload = True
    application.run(debug=True, threaded=True)



