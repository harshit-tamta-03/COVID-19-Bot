# imports:
import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading


# get html data of website
def get_html_data(url):
    data = requests.get(url)
    return data


# parsing html and extracting data
def get_corona_detail_of_india():
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_class = bs.find("div", class_="site-stats-count")
    class_list = ["bg-blue", "bg-green", "bg-red", "bg-orange"]
    info_date = info_class.find("div", class_="status-update")
    date = info_date.span.string
    all_details = "COVID-19 INDIA " + date + "\n\n"
    for class_var in class_list:
        info_sub_class = info_class.find("li", class_=class_var)
        count = info_sub_class.strong.string
        text = info_sub_class.span.string
        all_details = all_details + text + " : " + count + "\n\n"
    return all_details


# function use to reload the data from website
def refresh():
    newdata = get_corona_detail_of_india()
    print('Refreshing ...')
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID-19 cases of INDIA.",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon='icon.ico'
        )
        time.sleep(30)


# creating GUI:

root = tk.Tk()
root.geometry("510x625")
root.title('COVID-19 Bot -INDIA')
root.iconbitmap('icon.ico')
root.configure(background='white')
f = ("economica", 12, "normal")

banner = tk.PhotoImage(file="banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()

mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='white')
mainLabel.pack()

reBtn = tk.Button(root, text="Refresh", font=f, command=refresh)
reBtn.pack()

# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()
