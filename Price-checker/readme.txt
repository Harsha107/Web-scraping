This is a simple Web Scrapping project where the program does the following:
  1) Goes through the given url of an Amazon product everyday
  2) Exports Title, Price, Rating, and date accessed into a csv file
  3) If the price is below the desired/mentioned price, it sends a mail informing that using smtplib library

APWSapp.py is a streamlit application for doing the above. Here the user inputs the URL, then the application displays the product details. It then asks if the user would like to track the product. If yes, then it asks the user to enter their email address and the maximum price they want it to be. The application then sends a mail to the user if the price drops below mentioned price.

https://hrsh-web-scraping.streamlit.app/ for partially working webpage.
