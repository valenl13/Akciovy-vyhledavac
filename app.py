# app.py
from flask import Flask, render_template, request
from stock import Stock
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_info = None
    error = None
    chart_url = None
    selected_ticker = None
    selected_period = None

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        selected_period = request.form.get('period', '1mo')
        selected_ticker = ticker
        
        try:
            stock = Stock(ticker)
            stock_info = stock.get_info()
            chart_path = stock.create_price_chart(period=selected_period)
            if chart_path:
                chart_url = "/" + chart_path + f"?nocache={int(time.time())}"  # => přidá náhodný řetězec, aby se graf vždy načetl znovu
        except Exception as e:
            error = f"Chyba: {str(e)}"

    return render_template('index.html', stock_info=stock_info, error=error, chart_url=chart_url, selected_ticker=selected_ticker, selected_period=selected_period)

if __name__ == '__main__':
    app.run(debug=True)
