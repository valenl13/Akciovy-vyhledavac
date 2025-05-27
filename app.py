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

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        selected_period = request.form.get('period', '1mo')
        try:
            stock = Stock(ticker)
            stock_info = stock.get_info()
            chart_path = stock.create_price_chart(period=selected_period)
            if chart_path:
                chart_url = "/" + chart_path + f"?nocache={int(time.time())}"  # => přidá náhodný řetězec, aby se graf vždy načetl znovu
        except Exception as e:
            error = f"Chyba: {str(e)}"

    return render_template('index.html', stock_info=stock_info, error=error, chart_url=chart_url)

if __name__ == '__main__':
    app.run(debug=True)
