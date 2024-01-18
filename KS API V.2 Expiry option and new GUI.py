from ks_api_client import ks_api
import requests
from tkinter import *
import tkinter
import pandas as pd
import time
import threading


# Login_Data
consumerkey = ""
app_id = ""
accesstoken = ""

userid = ""
password = ""
otp = ""

# Login process
client = ks_api.KSTradeApi(access_token = accesstoken, userid = userid, \
                consumer_key = consumerkey, ip = "127.0.0.1", app_id = app_id)

client.login(password = password)
client.session_2fa(access_code = otp)

# Request for Instruments
url = 'https://tradeapi.kotaksecurities.com/apim/scripmaster/1.1/filename'
headers = {'accept': 'application/json', "consumerKey": f"{consumerkey}" , "Authorization": f"Bearer {accesstoken}" }
res = requests.get(url , headers=headers).json()
cashurl = res['Success']['cash']
fnourl =  res['Success']['fno']

# Pandas for token reading 
fnopdf = pd.read_csv(fnourl, sep="|")


#Margin Reading
url2 = 'https://tradeapi.kotaksecurities.com/apim/margin/1.0/margin'
headers2 = {'accept': 'application/json', "consumerKey": f"{consumerkey}" , "sessiontoken": client.session_token , "Authorization": f"Bearer {accesstoken}" }
res2 = requests.get(url2 , headers=headers2).json()

# Background loop to maintain connetion
def background():
    while True:
        client.positions(position_type = "TODAYS")
        time.sleep(5)

#-________________________________________________________________GUI____________________________________________________________________-

def foreground():
    # foreground -GUI WORK
    
    app = tkinter.Tk()
    app.title("FASTASS KOTAK")
    app.geometry("400x150")

    # DEF funtion

        # CE def
    def CE_buy():
        strick = int(CE.get())
        otype = o_type.get()
        qtty = int(qty.get())
        sybl = symbol.get()
        exry = expiry.get()
        vrty = variety.get()  
              
        token = int(fnopdf[(fnopdf.exchange =='NSE') & (fnopdf.instrumentName == sybl) & 
                 (fnopdf.expiry == exry) & (fnopdf.strike == strick) & (fnopdf.optionType == 'CE')
                 ].iloc[0,0])

        buy_order = client.place_order(order_type = otype, instrument_token = token, transaction_type = "BUY",\
                        quantity = qtty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = vrty, tag = "string")
        print(buy_order)

    def CE_sell():
        strick = int(CE.get())
        otype = o_type.get()
        qtty = int(qty.get())
        sybl = symbol.get()
        exry = expiry.get()
        vrty = variety.get()
        
        token = int(fnopdf[(fnopdf.exchange =='NSE') & (fnopdf.instrumentName == sybl) & 
                 (fnopdf.expiry == exry) & (fnopdf.strike == strick) & (fnopdf.optionType == 'CE')
                 ].iloc[0,0])

        sell_order = client.place_order(order_type = otype, instrument_token = token, transaction_type = "SELL",\
                        quantity = qtty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = vrty, tag = "string")
        print(sell_order)
        vrty = variety.get()
        # PE def
    def PE_buy():
        strick = int(PE.get())
        otype = o_type.get()
        qtty = int(qty.get())
        sybl = symbol.get()
        exry = expiry.get()
        vrty = variety.get()  
              
        token = int(fnopdf[(fnopdf.exchange =='NSE') & (fnopdf.instrumentName == sybl) & 
                 (fnopdf.expiry == exry) & (fnopdf.strike == strick) & (fnopdf.optionType == 'PE')
                 ].iloc[0,0])

        buy_order = client.place_order(order_type = otype, instrument_token = token, transaction_type = "BUY",\
                        quantity = qtty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = vrty, tag = "string")
        print(buy_order)

    def PE_sell():
        strick = int(PE.get())
        otype = o_type.get()
        qtty = int(qty.get())
        sybl = symbol.get()
        exry = expiry.get()
        vrty = variety.get()
        
        token = int(fnopdf[(fnopdf.exchange =='NSE') & (fnopdf.instrumentName == sybl) & 
                 (fnopdf.expiry == exry) & (fnopdf.strike == strick) & (fnopdf.optionType == 'PE')
                 ].iloc[0,0])

        sell_order = client.place_order(order_type = otype, instrument_token = token, transaction_type = "SELL",\
                        quantity = qtty, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = vrty, tag = "string")
        print(sell_order)


     


    # Selecting of Order type,Expiry,Symbol
    symbol = StringVar()
    symbol.set('BANKNIFTY')
    drop= OptionMenu(app, symbol,'BANKNIFTY','NIFTY')
    drop.grid(row=1,column=1,padx=5,pady=10)
    
    expiry = StringVar()
    expiry.set('23MAR23')
    drop= OptionMenu(app, expiry,'23MAR23','29MAR23','06APR23','13APR23')
    drop.grid(row=1,column=2,padx=7,pady=10)
    
    o_type = StringVar()
    o_type.set('N')
    drop= OptionMenu(app, o_type,'N','MIS')
    drop.grid(row=1,column=3,padx=10,pady=10)
    
    variety = StringVar()
    variety.set('REGULAR')
    drop= OptionMenu(app, variety,'REGULAR','AMO')
    drop.grid(row=1,column=4,padx=5,pady=10)
    
    qt = Label(app,text= "Quantity:")
    qt.grid(row=2,column=1,padx=5)
    qty = Entry(bd = 4, width=10)
    qty.grid(row=2,column=2)
    
    
    # Input for token
    CET = Label(app,text= "CE:")
    CET.grid(row=3,column=1,padx=5,pady=5)
    CE = Entry(bd = 4, width=10)
    CE.grid(row=3,column=2,pady=5)

    PET = Label(app,text= "PE:")
    PET.grid(row=3,column=3,padx=5,pady=5)
    PE = Entry(bd = 4, width=10)
    PE.grid(row=3,column=4,pady=5)
    
    # Button
    greenbutton = Button(app, text = "CE BUY", fg="Green", width=9,height=1,bd=3, command= CE_buy)
    greenbutton.grid(row=4,column=1,pady=5,padx=2)
    redbutton = Button(app, text = "CE SELL", fg = "Green", width=9,height=1,bd=3, command= CE_sell)
    redbutton.grid(row=4,column=2,pady=5,padx=2)
    
    redbutton = Button(app, text = "PE BUY", fg = "Red", width=9,height=1,bd=3, command= PE_buy)
    redbutton.grid(row=4,column=3,pady=5,padx=2)
    greenbutton = Button(app, text = "PE SELL", fg="Red", width=9,height=1,bd=3, command= PE_sell )
    greenbutton.grid(row=4,column=4,pady=5,padx=2)

    app.mainloop()
    # GUI ends here     


# Multi threading 
fore = threading.Thread(name='foreground', target=foreground)
back = threading.Thread(name='background', target=background)

back.start()
fore.start()