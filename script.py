import ccxt

# Configure your exchange and API keys
exchange_id = 'binance'
api_key = 'YOUR_API_KEY'
secret = 'YOUR_SECRET_KEY'

exchange = getattr(ccxt, exchange_id)({
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
})

# Parameters (these would typically be dynamic or input by the user)
symbol = 'BTC/USDT'
risk_level = 0.01
risk_reward_ratio = 2.0
stop_loss_price = 30000  # Example stop loss price

# Function to get the balance
def get_balance():
    balance = exchange.fetch_balance()
    return balance['total']['USDT']  # Assuming we are trading against USDT

# Function to get the buy price from the order book
def get_buy_price():
    order_book = exchange.fetch_order_book(symbol)
    return order_book['asks'][0][0]  # Best ask price (sell price)

# Function to calculate the profit price
def calculate_profit_price(buy_price, stop_loss_price, risk_reward_ratio):
    return buy_price + (buy_price - stop_loss_price) * risk_reward_ratio

# Function to calculate the order quantity
def calculate_quantity(balance, risk_level, buy_price, stop_loss_price):
    return balance * risk_level / (buy_price - stop_loss_price)

# Main execution logic
def main():
    balance = get_balance()
    buy_price = get_buy_price()
    profit_price = calculate_profit_price(buy_price, stop_loss_price, risk_reward_ratio)
    quantity = calculate_quantity(balance, risk_level, buy_price, stop_loss_price)
    
    print(f"Balance: {balance} USDT")
    print(f"Buy Price: {buy_price} USDT")
    print(f"Stop Loss Price: {stop_loss_price} USDT")
    print(f"Profit Price: {profit_price} USDT")
    print(f"Order Quantity: {quantity} BTC")

    # Place the order
    order = exchange.create_order(
        symbol=symbol,
        type='limit',
        side='buy',
        amount=quantity,
        price=buy_price,
        params={
            'stopPrice': stop_loss_price,
            'takeProfitPrice': profit_price,
        }
    )
    
    print(f"Order placed: {order}")

if __name__ == "__main__":
    main()
