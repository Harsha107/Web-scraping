import streamlit as st
import requests
from bs4 import BeautifulSoup
import smtplib

def send_mail(product_title, product_price, target_price, product_url, sender_mail):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('Lane89@gmail.com', 'Lane89ismyname')
    
    subject = f"The product '{product_title}' is below your target price!"
    body = f"The product you wanted to buy is now below {target_price} AED!\n\nCurrent price: {product_price} AED\n\nLink to the product: {product_url}"
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail('Lane89@gmail.com', sender_mail, msg)
    server.quit()

def check_price(url, target_price=None, sender_mail=None):
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    
    page = requests.get(url, headers=custom_headers)
    soup = BeautifulSoup(page.content, "html.parser")
    
    try:
        title = soup.find(id='productTitle').get_text().strip()
        price = float(soup.find(class_='a-offscreen').get_text().replace("AED", "").replace(",", "").strip())
        ratings = soup.find(class_='a-icon-alt').get_text().strip()
    except AttributeError:
        st.error("Could not retrieve product information. Please check the URL.")
        return None, None, None

    st.write("### Product Details")
    st.write(f"**Title**: {title}")
    st.write(f"**Price**: AED {price}")
    st.write(f"**Ratings**: {ratings}")
    
    if target_price and price < target_price:
        send_mail(title, price, target_price, url, sender_mail)
        st.success(f"Email sent! The product '{title}' is now below AED {target_price}.")
    
    return title, price, ratings

st.title("Amazon Price Tracker")

product_url = st.text_input("Enter the Amazon product URL")

if st.button("Check Price"):
    if product_url:
        title, price, ratings = check_price(product_url)
        
        if title and price:
            if "monitor_checkbox" not in st.session_state:
                st.session_state.monitor_checkbox = False
            
            if st.checkbox("Would you like to monitor this product for price drops?", key="monitor_checkbox"):
                target_price = st.number_input("Enter your target price in AED", min_value=0.0, key="target_price")
                sender_mail = st.text_input("Enter your Email address for notifications", key="sender_mail")

                if st.button("Start Monitoring"):
                    if sender_mail:
                        check_price(product_url, target_price, sender_mail)
                    else:
                        st.warning("Please enter a valid email address for notifications.")
    else:
        st.warning("Please enter a valid Amazon URL.")