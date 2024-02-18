import subprocess
import okx.Account_api as Account
# import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
# import okx.status_api as Status
# import okx.subAccount_api as SubAccount
# import okx.TradingData_api as TradingData
# import okx.Broker_api as Broker
# import okx.Convert_api as Convert
# import okx.FDBroker_api as FDBroker
# import okx.Rfq_api as Rfq
# import okx.TradingBot_api as TradingBot
# import okx.Finance_api as Finance
# import okx.Copytrading_api as Copytrading
# import okx.Recurring_api as Recurring
# import okx.SprdApi_api as Sprd
import sys
import tkinter as tk
from tkinter import ttk
# from tkinter import StringVar
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
# import pyautogui
import pyperclip
# import time
# import json
from config_run import Config
# from config_dev import Config



# option_var =  "Buy"# Variable 
default_side = "sell"
default_lever = 1
default_plr = "1"
default_riskUnit = "0"
default_riskLevel = 3 # unit in %
api_key = Config.API_KEY
secret_key = Config.SECRET_KEY 
passphrase = Config.PASSPHRASE
flag =Config.FLAG
tradeAPI   =     Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
marketAPI  =   Market.MarketAPI(api_key, secret_key, passphrase, True, flag)
publicAPI  =   Public.PublicAPI(api_key, secret_key, passphrase, False, flag)

# # init parameters
# side = default_side
# otyp = "limit"
pxlst = None
szlst = None
stopRatelst = None
outRatelst = None

def get_clipboard_price():
    try:
        # 使用xclip获取剪贴板文本
        clipboard_text = subprocess.check_output(['xclip', '-o', '-selection', 'clipboard'], text=True)
        clipboard_price = float(clipboard_text.strip())
        print("Got clipboard price:", clipboard_price)
        price_input.delete(0, tk.END)  # Clear the current input
        price_input.insert(0, clipboard_price)  # Set clipboard price in the input box
    except (subprocess.CalledProcessError, ValueError):
        # 如果剪贴板中没有有效的数字或发生错误，忽略它
        print("The clipboard doesn't contain a valid number")
        return

# Define a custom class to redirect standard output
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Append the message to the Text widget
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end to display the latest output

# selected_value_label.config(text=f"Selected Value: {selected_value}")
def on_scale_changed(event):
    selected_value = scale_var.get()
    plr_input.delete(0,tk.END)
    plr_input.insert(0,selected_value)

# 获取 result 返回 key 对应值
def extract_from_dict(data, key):
    # 处理数据模块 筛选目标值
    if key in data:
        return data[key]    
    # 遍历当前字典
    for k, v in data.items():
        # 如果值是字典，递归查找
        if isinstance(v, dict):
            item = extract_from_dict(v, key)
            if item is not None:
                return item
        # 如果值是列表，遍历列表中的每个字典
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    item = extract_from_dict(d, key)
                    if item is not None:
                        return item


# def parameter_collector():
#     instId = crypto_combobox.get()
#     sz = quantity_input.get()
#     riskUnit = risk_unit_input.get()
#     lever = lever_input.get()
#     side = option_var.get()

def get_balance():
    result = accountAPI.get_account('USDT')
    availEq = extract_from_dict(result,"availEq")
    BAL_input.delete(0,tk.END)
    BAL_input.insert(0,availEq)
    return availEq
    
# def get_position_quantity():
#       # 获取未成交订单列表  Get Order List
#     result = tradeAPI.get_order_list(instType = '', uly = '', instFamily = '', instId = '', ordType = '', state = '', after = '', before = '', limit = '')
#     return result
#      # 获取订单信息  Get Order Details
#      # result = tradeAPI.get_orders('BTC-USD-201225', '257173039968825345')
#      # print(extract_from_api_response(get_position_quantity(),"ordId"))

# def close_all_positions():
#     instId = crypto_combobox.get()
#     # 市价仓位全平  Close Positions
#     result = tradeAPI.close_positions(instId,posSide='net', mgnMode='cross',ccy='', autoCxl='true',clOrdId='',tag='')
#     return result

# 获取交易产品基础信息  Get instrument
# def get_pair_instrument():
#     result = publicAPI.get_instruments(instType = 'SWAP', uly = '', instFamily = 'TRB-USDT', instId = '')
#     return result
#     # print(get_pair_instrument())

# def cancel_order():
#     # 取消定单  Cancel Order
#     instId = crypto_combobox.get()
#     result = tradeAPI.cancel_order(instId, '623634878139396104')
#     return result
#     # print(cancel_order())
#     # 下单  Place Order

# def execute_trigger_order(TriggerPx,OrdPx,side):
#     instId = crypto_combobox.get()
#     px = price_input.get()
#     sz = quantity_input.get()
#     result = tradeAPI.place_order(instId =instId, tdMode='cross', side=side, sz=sz, px=px,posSide='',
#                                   ordType="limit",tgtCcy='',banAmend='',quickMgnType='auto_borrow',
#                                   tpTriggerPx = TriggerPx, tpOrdPx = OrdPx, slTriggerPx = TriggerPx, slOrdPx = OrdPx, 
#                                   tpTriggerPxType = 'index', slTriggerPxType = 'index')
#     return result

def execute_order():
    otyp = "limit"
    result = tradeAPI.place_order(instId = instId, tdMode='cross', side=side, sz=sz, px=px,posSide='',
                                  ordType=otyp,tgtCcy='',banAmend='',quickMgnType='auto_borrow',
                                  tpTriggerPx = '', tpOrdPx = '', slTriggerPx = '', slOrdPx = '', 
                                  tpTriggerPxType = '', slTriggerPxType = '')
          
    # stop loss stop loss market sell 
    # take profit
    # limit buy
    result = tradeAPI.place_order(instId =instId, tdMode='cross', side=side, sz=sz, px=px,posSide='',
                                  ordType=otyp,tgtCcy='',banAmend='',quickMgnType='auto_borrow',
                                  tpTriggerPx = '', tpOrdPx = '', slTriggerPx = '', slOrdPx = '', 
                                  tpTriggerPxType = '', slTriggerPxType = '')
    return result
    # print(execute_order())

def extract_from_dict(data, key):
    # 如果key在当前字典级别中
    if key in data:
        return data[key]
    
    # 遍历当前字典
    for k, v in data.items():
        # 如果值是字典，递归查找
        if isinstance(v, dict):
            item = extract_from_dict(v, key)
            if item is not None:
                return item
        # 如果值是列表，遍历列表中的每个字典
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    item = extract_from_dict(d, key)
                    if item is not None:
                        return item

def get_clipboard_price():
    try:
        clipboard_text = pyperclip.paste()
        try:
            clipboard_price  = float(clipboard_text)
            print("Got clipboard price:",clipboard_price)
            price_input.delete(0, tk.END)  # Clear the current input
            price_input.insert(0, clipboard_price)  # Set clipboard price in the input box
        except ValueError:
            # If the clipboard doesn't contain a valid number, ignore it
            print("The clipboard doesn't contain a valid number")
            return
    except :
        print("unknown error")


# strategy 
def calculate_parameters(stopRate):
        buyRate = get_pair_ticker()
        plr = plr_input.get()
        riskUnit = risk_unit_input.get()
        print(buyRate,stopRate,plr,riskUnit)     
        loss = float(buyRate)-float(stopRate)
        quantity = int(float(riskUnit) / loss)
        # outRate = float(plr)*marg + float(buyRate)
        outRate = round(
            (float(plr)*loss + float(buyRate)),len(str(buyRate).split('.')[1])
            )
        return buyRate,stopRate,outRate,quantity

def calculate_riskUnit(riskLevel= default_riskLevel):
    print(f"Using Risk Level {riskLevel}%")
    # riskLevel = 0.01
    availeq = extract_from_dict((accountAPI.get_account('USDT')),"availEq")
    riskUnit = riskLevel*float(availeq)*0.01
    BAL_input.delete(0,tk.END)
    BAL_input.insert(0,availeq)
    risk_unit_input.delete(0,tk.END)
    risk_unit_input.insert(0,riskUnit)

def get_pair_ticker():
    instId = crypto_combobox.get()
    result = marketAPI.get_ticker(instId)
    print(result)
    ticker_price = extract_from_dict(result,"bidPx")
    price_input.delete(0, tk.END)  # Clear the current input
    price_input.insert(0, ticker_price)  # Set clipboard price in the input box
    return ticker_price



# def get_quantity(side):
def  place_lmtorder():
    response = messagebox.askquestion("确认", "确定要执行此操作吗?")
    if response == "yes":
        # side = side_combobox.get()
        side = side_var.get()
        instId = crypto_combobox.get()
        plr = float(plr_input.get())
        riskUnit = float(risk_unit_input.get())
        stopRate = float(price_input.get())
    
        print(side)
        if side == "buy":
            buyRate = float(extract_from_dict(marketAPI.get_ticker(instId),"bidPx"))
            lost = buyRate-stopRate
            outRate = round((buyRate+plr*lost),len(str(buyRate).split('.')[1]))
            px = buyRate
        else:
            sellRate = float(extract_from_dict(marketAPI.get_ticker(instId),"askPx"))    
            lost = stopRate-sellRate
            outRate = round((sellRate-plr*lost),len(str(sellRate).split('.')[1]))
            px = sellRate
        quantity = int(riskUnit/lost)
        if quantity > 0:
            result = tradeAPI.place_order(
                    instId = instId, 
                    tdMode='cross',
                    side=side, 
                    sz=quantity, 
                    px=px,
                    posSide= '',
                    ordType= "limit",
                    tgtCcy= '',
                    banAmend='',
                    quickMgnType = 'auto_borrow',
                    tpTriggerPx = '', 
                    tpOrdPx = "", 
                    slTriggerPx = '',
                    slOrdPx = "",
                    tpTriggerPxType = '', 
                    slTriggerPxType = ''
                    )
            msg = extract_from_dict(result,'sMsg')
            riskUnit = lost*quantity
            if msg == 'Order placed':
                print('---------------------------')
                print(f'Side     : {side}')
                print(f'lost     : {lost}')
                print(f'Out Rate : {outRate}')
                print(f'Buy Rate : {px}')
                print(f'Stop Rate: {stopRate}')
                print(f'Qty      : {quantity}')
                print(f'PLR      : {plr}')
                print(f'Risk Unit: {riskUnit}')
                print(f'MSG      : {msg}')
                print(f'Done, Good luck!')
                quantity_input.delete(0, tk.END)  # Clear the current input
                quantity_input.insert(0, quantity)  # Set quantity in the input box
            else:
                print(result)
                print('+++++++++++++++++++++++++++++')

                    
        else :        
            print(f'Qty      : {quantity}')
            print('Please check parameters.')

            


def sltp_quantity():
    response = messagebox.askquestion("确认", "确定要执行此操作吗?")
    if response == "yes":
        # side = side_combobox.get()
        side = side_var.get()
        instId = crypto_combobox.get()
        plr = float(plr_input.get())
        riskUnit = float(risk_unit_input.get())
        stopRate = float(price_input.get())
        # if side == "sell" :
        #     side_key = "maxSell"
        # if side == "buy" :
        #     side_key = "maxBuy"
        # print(instId)
        # result = accountAPI.get_maximum_trade_size(instId, tdMode='cross',ccy='',px='',leverage=lever_input.get(),unSpotOffset='false')
        # print(result)
        # quantity = extract_from_dict(result,side_key)
        print(side)
        if side == "buy":
            buyRate = float(extract_from_dict(marketAPI.get_ticker(instId),"bidPx"))
            lost = buyRate-stopRate
            outRate = round((buyRate+plr*lost),len(str(buyRate).split('.')[1]))
        else:
            sellRate = float(extract_from_dict(marketAPI.get_ticker(instId),"askPx"))    
            lost = stopRate-sellRate
            outRate = round((sellRate-plr*lost),len(str(sellRate).split('.')[1]))
        quantity = int(riskUnit/lost)
        riskUnit = lost*quantity
            
        quantity_input.delete(0, tk.END)  # Clear the current input
        quantity_input.insert(0, quantity)  # Set quantity in the input box
 

def get_lever():
    instId = crypto_combobox.get()
    result = accountAPI.get_leverage(instId, 'cross')
    print(result)
    lever = extract_from_dict(result,"lever")
    lever_input.delete(0, tk.END)  # Clear the current input
    lever_input.insert(0, lever)  # Set quantity in the input box
def set_lever():
    instId = crypto_combobox.get()
    lever = lever_input.get()
    print(instId,lever)
    result = accountAPI.set_leverage(instId=instId,lever=lever, mgnMode='cross')
    print(result)

def plr_openPosition():
    instId = crypto_combobox.get()
    buyRate = extract_from_dict(marketAPI.get_ticker(instId),"bidPx")
    stopRate = price_input.get()
    plr = plr_input.get()
    riskUnit = risk_unit_input.get()
    side = option_var.get()
    print(buyRate,stopRate,plr,riskUnit)

    parameter_tuple = calculate_parameters(buyRate,stopRate,plr,riskUnit)

    # 止盈损委托价 -1代表市价委托 
    slOrdPx = "-1" 	    
    tpOrdPx = "-1"  
    # 止盈损触发价类型
    tpTriggerPxType= "last"
    slTriggerPxType= "last"

    px = buyRate                     #buyRate
    slTriggerPx = stopRate           #stopRate
    tpTriggerPx = parameter_tuple[2] #outRate
    sz = parameter_tuple[3]          #quantity
    print(parameter_tuple)
    # execute_order
    result = tradeAPI.place_order(instId = instId, tdMode='cross', side='buy', sz=sz, px= px ,posSide='',ordType="limit",tgtCcy='',banAmend='',quickMgnType='auto_borrow',tpTriggerPx = tpTriggerPx, tpOrdPx = tpOrdPx, slTriggerPx = slTriggerPx, slOrdPx = slOrdPx, tpTriggerPxType = tpTriggerPxType, slTriggerPxType = slTriggerPxType)
    global pxlst,szlst
    pxlst = px
    szlst = sz
    print(result)
    return 

    # result = tradeAPI.place_order(instId = instId, tdMode='cross', side='buy', sz=sz, px= px ,posSide='',ordType="limit",tgtCcy='',banAmend='',quickMgnType='auto_borrow',tpTriggerPx = tpTriggerPx, tpOrdPx = tpOrdPx, slTriggerPx = slTriggerPx, slOrdPx = slOrdPx, tpTriggerPxType = tpTriggerPxType, slTriggerPxType = slTriggerPxType)
    # print(result)
    # # 止盈损委托价 -1代表市价委托 
    # slOrdPx = "-1"
    # tpOrdPx = "-1"
    # # 止盈损触发价类型
    # tpTriggerPxType= "last"
    # slTriggerPxType= "last"
    # outRate = float(plr)*marg + float(buyRate)

def plr_sltp(side): 
    instId = crypto_combobox.get()
    # lever = float(lever_input.get())
    plr = float(plr_input.get())
    riskUnit = float(risk_unit_input.get())
    stopRate = float(price_input.get())
    buyRate = float(extract_from_dict(marketAPI.get_ticker(instId),"bidPx"))    
    if side == "buy":
       lost = buyRate-stopRate
       outRate = round((buyRate+plr*lost),len(str(buyRate).split('.')[1]))
    else:
       lost = stopRate-buyRate
       outRate = round((buyRate-plr*lost),len(str(buyRate).split('.')[1]))
    quantity = int(riskUnit/lost)
    riskUnit = lost*quantity
    # execute_order
    if quantity > 0:
        result = tradeAPI.place_order(
                    instId = instId, 
                    tdMode='cross',
                    side=side, 
                    sz=quantity, 
                    px=buyRate,
                    posSide= '',
                    ordType= "limit",
                    tgtCcy= '',
                    banAmend='',
                    quickMgnType = 'auto_borrow',
                    tpTriggerPx = outRate, 
                    tpOrdPx = "-1", 
                    slTriggerPx = stopRate,
                    slOrdPx = "-1",
                    tpTriggerPxType = "last", 
                    slTriggerPxType = "last"
                    )
        # print(result)

        price_input.delete(0, tk.END)  # Clear the current input
        price_input.insert(0, stopRate)  # Set quantity in the input box
        
        print('---------------------------')
        print('Order Summary')
        print(f'Side     : {side}')
        print(f'lost     : {lost}')
        print(f'Out Rate : {outRate}')
        print(f'Buy Rate : {buyRate}')
        print(f'Stop Rate: {stopRate}')
        print(f'Qty      : {quantity}')
        print(f'PLR      : {plr}')
        print(f'Risk Unit: {riskUnit}')
        print(f'Done, Good luck!')
    else :        
        print(f'Qty      : {quantity}')
        print('Please check parameters.')

def handle_option():
    selected_option = option_var.get()
    print("Selected Option:", selected_option)

def confirm_action():
    # 弹出确认框，等待用户的响应
    response = messagebox.askquestion("确认", "确定要执行此操作吗?")
    if response == "yes":
        return True
    else:
        return False

def perform_action(action):
    if confirm_action():
        if action == "Limit Buy":
        #  limit price buy   
           side = "buy"
           execute_order("limit",side)
           print("Limit Buy executed")
           pass

        elif action == "Limit Sell":
            # limit price sell
            side = "sell"
            execute_order("limit",side)
            print("Limit Sell executed")
            pass

        elif action == "Limit TP":
            # limit price take profit
            side = "sell"
            execute_order("limit",side)
            print("Limit TP executed")
            pass

        elif action == "Market Buy":
            # market price buy
            side = "buy"
            execute_order("market",side)
            print("Market Buy executed")
            pass

        elif action == "Market Sell":
            side = "sell"
            # market price sell
            execute_order("market",side)
            print("Market Sell executed")
            pass

        elif action == "Market CP":
            # close_all_positions
            # close_all_positions(instId)
            print("CLose Positions executed")
            pass

        elif action == "BuyPLR":
            info =plr_sltp("buy")
            pass

        elif action == "SellPLR":
            info =plr_sltp("sell")
            pass



# Create the main window
window = tk.Tk()
window.title("Trade")


# Create and place widgets
frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

# crypto_label
crypto_label = tk.Label(frame, text="PR",width=2, height=1, justify=tk.LEFT)
crypto_label.grid(row=5, column=6, padx=0, pady=0)

# list of cryptocurrencies for the dropdown
crypto_list = ["WLD-USDT-SWAP","WLD-USDT-SWAP","BTC-USDT-SWAP","LTC-USDT-SWAP"]
crypto_combobox = ttk.Combobox(frame, values=crypto_list)
crypto_combobox.configure(width=20)
crypto_combobox.set(crypto_list[0])  # Set the default value    
crypto_combobox.grid(row=5, column=7, padx=0, pady=0,rowspan=1)

# get_pair_ticker_button
get_pair_ticker_button = tk.Button(frame, text="Ticker Price", command=get_pair_ticker)
get_pair_ticker_button.grid(row=1, column=3, padx=10, pady=10)

# get clipboard price
clipboard_button = tk.Button(frame, text="Paste", command=get_clipboard_price)
clipboard_button.grid(row=1, column=2, padx=0, pady=0)

# price label
price_label = tk.Label(frame, text="Price:")
price_label.grid(row=1, column=0, padx=10, pady=10)
price_input = tk.Entry(frame)
price_input.grid(row=1, column=1, padx=10, pady=10)

# quantity
quantity_label = tk.Label(frame, text="Qty:",height=1,justify=tk.LEFT)
quantity_label.grid(row=2, column=0, padx=10, pady=10)
quantity_input = tk.Entry(frame)
quantity_input.grid(row=2, column=1, padx=10, pady=10,rowspan=1)
get_quantity_button = tk.Button(frame, text="RU OP", command=place_lmtorder)
get_quantity_button.grid(row=0, column=0, padx=10, pady=10)
get_quantity_button = tk.Button(frame, text="SLTP", command=sltp_quantity)
get_quantity_button.grid(row=2, column=3, padx=10, pady=10)

# risk unit  
risk_unit_label = tk.Label(frame, text="Risk Unit",height=1,justify=tk.LEFT)
risk_unit_label.grid(row=0, column=5, padx=10, pady=10)
risk_unit_input = tk.Entry(frame)
risk_unit_input.insert(0, default_riskUnit)  # 插入默认值
risk_unit_input.grid(row=0, column=6, padx=10, pady=10,rowspan=1)
get_risk_lot_button = tk.Button(frame, text="Get RU", command=calculate_riskUnit)
get_risk_lot_button.grid(row=0, column=1, padx=10, pady=10)

# BAL
BAL_label = tk.Label(frame, text="BAL:")
BAL_label.grid(row=1, column=5, padx=10, pady=10)
BAL_input = tk.Entry(frame)
# BAL_input.insert(0, default_BAL)  # 插入默认值
BAL_input.grid(row=1, column=6, padx=10, pady=10)
get_risk_lot_button = tk.Button(frame, text="Get BAL", command=get_balance)
get_risk_lot_button.grid(row=1, column=7, padx=10, pady=10)

# PLR
plr_label = tk.Label(frame, text="PLR:")
plr_label.grid(row=2, column=5, padx=10, pady=10)
plr_input = tk.Entry(frame)
plr_input.insert(0, default_plr)  # 插入默认值
plr_input.grid(row=2, column=6, padx=10, pady=10)

# # 创建一个标签来显示当前选择的值
# selected_value_label = tk.Label(frame, text="Selected Value: 0")
# selected_value_label.grid(row=4, column=7, padx=10, pady=10)

# 创建一个滑动条
# #####################
scale_var = tk.IntVar()
scale = ttk.Scale(frame, from_=1, to=5, variable=scale_var, orient="horizontal", command=on_scale_changed)
scale.grid(row=2, column=7, padx=10, pady=10)
# #####################

lever_label = tk.Label(frame, text="Lev:",height=1,justify=tk.LEFT)
lever_label.grid(row=3, column=0, padx=10, pady=10)
lever_input = tk.Entry(frame)
lever_input.insert(0, "PLEASE CONFIRM LEVELAGE")  # 插入默认值
lever_input.grid(row=3, column=1, padx=10, pady=10,rowspan=1)
get_lever_button = tk.Button(frame, text="Get Lever", command=get_lever)
get_lever_button.grid(row=3, column=2, padx=10, pady=10)
set_lever_button = tk.Button(frame, text="Set Lever", command=set_lever)
set_lever_button.grid(row=3, column=3, padx=10, pady=10)

# list of order types for the dropdown
order_type_list = ["limit", "market","SL","TP"]
order_type_combobox = ttk.Combobox(frame,values=order_type_list,justify='right')
order_type_combobox.configure(width=8)
order_type_combobox.set(order_type_list[0])  # Set the default value
order_type_combobox.grid(row=5, column=1, padx=10, pady=10,rowspan=1)

# list of mrkt types for the dropdown
mrkt_type_list = ["B_SWAP", "S_SWAP","B_SPOT","S_SPOT"]
mrkt_type_combobox = ttk.Combobox(frame,values=mrkt_type_list,justify='right')
mrkt_type_combobox.configure(width=8)
mrkt_type_combobox.set(mrkt_type_list[0])  # Set the default value
mrkt_type_combobox.grid(row=5, column=0, padx=0, pady=0,rowspan=1)

# list of side selection for the dropdown
side_list = ["buy", "sell","B_SPOT","S_SPOT"]
side_combobox = ttk.Combobox(frame,values=side_list,justify='right')
side_combobox.configure(width=8)
side_combobox.set(side_list[0])  # Set the default value
side_combobox.grid(row=5, column=2, padx=0, pady=0,rowspan=1)

    # actions = [
    #     "Limit Buy", "Limit Sell", "Limit CP",
    #     "SetLevel", "Market Sell", "Market CP",
    #     "Buy PLR SLTP", "Sell PLR SLTP"
    # ]
    # row_index = 4
    # column_index = 2
    # for action in actions:
    #     action_button = tk.Button(frame, text=action, command=lambda a=action: perform_action(a))
    #     action_button.grid(row=row_index, column=column_index, padx=5, pady=5)
        
    #     column_index += 1
    #     if column_index > 3:
    #         column_index = 2
    #         row_index += 1

actions = [
    "LmtBuy",   "LmtSell",    "LmtCP",
    "SetLevel", "MrktSell", "MrktCP",
    "BuyPLR", "SellPLR"
]
row_index = 3
column_index = 4
for action in actions:
    action_button = tk.Button(frame, text=action, command=lambda a=action: perform_action(a))
    action_button.grid(row=row_index, column=column_index, padx=5, pady=5)
    
    column_index += 1
    if column_index > 7:
        column_index = 4
        row_index += 1
# CCY conrtol [USDT/SPOT]
option_var = tk.StringVar(value="USDT")  # Variable to store the selected option
spotId = crypto_combobox.get().split('-')[0]
buy_radio = tk.Radiobutton(frame, text="USDT", variable=option_var, value="USDT", command=handle_option,width=5, height=2)
sell_radio = tk.Radiobutton(frame, text="SPOT", variable=option_var, value=spotId, command=handle_option)
buy_radio.grid(row=6, column=1, padx=10, pady=10)
sell_radio.grid(row=6, column=3, padx=10, pady=10)
# side conrtol [buy/sell]
side_var = tk.StringVar(value=default_side)  # Variable to store the selected option
b_radio = tk.Radiobutton(frame, text="BUY", variable=side_var, value="buy")
s_radio = tk.Radiobutton(frame, text="SELL", variable=side_var, value="sell")
b_radio.grid(row=0, column=2, padx=0, pady=0)
s_radio.grid(row=0, column=3, padx=0, pady=0)


# Create an instance of the custom StdoutRedirector class
output_text = tk.Text(frame, width=100, height=20, bg="black", fg="white", font=("Courier", 12))
output_text.grid(row=9, column=0, columnspan=8, padx=0, pady=0)
            # output_text = tk.Text(frame, wrap=tk.WORD, width=80, height=10)
            # output_window = ScrolledText(frame, width=80, height=10, bg="black", fg="white", font=("Courier", 12))

stdout_redirector = StdoutRedirector(output_text)
# Redirect standard output to the Text widget
sys.stdout = stdout_redirector

# Start the GUI event loop
window.mainloop()



















# tcrypto_list = ["WLD-USDT-SWAP", "BTC-USDT-SWAP", "TRB-USDT-SWAP", "Litecoin (LTC)"]
# tselected_crypto = StringVar()
# tcrypto_combobox = ttk.Combobox(frame, textvariable=tselected_crypto, values=tcrypto_list)
# tselected_crypto.set(tcrypto_list[0])  # 设置默认选择项
# tcrypto_combobox.grid(row=5, column=0, padx=5, pady=5)

# get parameters
# px = price_input.get()
# px = price_input.get()
# sz = quantity_input.get()

# Create buttons for trading actionsv
# actions = [
#     "Buy", "Sell", "Market Sell", "Market CP",
#     "Cancel", "Cxl All"
# ]
