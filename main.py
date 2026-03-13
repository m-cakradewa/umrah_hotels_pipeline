from xvfbwrapper import Xvfb
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
import random
from bs4 import BeautifulSoup as bs4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import psycopg2
import os

# from dotenv import load_dotenv
# load_dotenv()
logs = []
error_message = None
for i in range(15):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        print("DB connected")
        break
    except psycopg2.OperationalError as e:
        error_message = "Postgres not ready: "+str(e)
        print(f"Retry DB {i+1}/15", flush=True)
        time.sleep(2)
else:
    run_time = datetime.utcnow().isoformat()
    status = "failed"
    rows_inserted = 0
    logs.append((run_time, status, rows_inserted, error_message))
    raise RuntimeError("Postgres not ready.")

today = date.today()
offsets = [3,4,5,6,7,14,21,28,30,60,90,120,150,180,210,240,270,300,330,365]
checkin_list, checkout_list = [],[]
for i in offsets:
    checkin = today + timedelta(days=i)
    checkout = checkin + timedelta(days=1)
    checkin = checkin.strftime("%Y-%m-%d")
    checkout = checkout.strftime("%Y-%m-%d")
    checkin_list.append(checkin)
    checkout_list.append(checkout)

URL = "https://www.umrahme.com/hotel/en-eu/listing?checkin=2026-03-13&checkout=2026-03-14&destinationId=235565&destination=Makkah,%20Saudi%20Arabia&occupancy=1_1_&orderby=price&sortby=asc&starrating=[5,4,3,2]"
names, stars, distances, prices, links, ratings,scrape_date,checkin_date  = [],[],[],[],[],[],[],[]

vdisplay = Xvfb()
vdisplay.start()

#url = "https://www.agoda.com/search?city=78591&locale=en-us&currency=EUR&checkIn=2026-03-11&checkOut=2026-03-12&rooms=1&adults=1&children=0&textToSearch=Mecca"
for checkin,checkout in zip(checkin_list,checkout_list):
    parsed = urlparse(URL)
    params = parse_qs(parsed.query)
    params["checkin"] = checkin
    params["checkout"] = checkout
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.google.com")
        time.sleep(1)
        driver.get(new_url)
        print("LOADED: ", new_url, flush=True)
        time.sleep(1)
        print("scraping page..")
    except Exception as e:
        run_time = datetime.utcnow().isoformat()
        error_message = str(e)
        status = "failed"
        rows_inserted = 0
        logs.append((run_time, status, rows_inserted, error_message))
        raise RuntimeError(e)
        break

    count = 0
    while True:
        print(f"total items found: {count}")
        for i in range(0,12):
            driver.execute_script(f"window.scrollBy(0, {random.randint(450,700)});")
            time.sleep(random.uniform(.5,2))
        html = driver.page_source
        time.sleep(2)
        soup = bs4(html, "html.parser")
        cards = soup.find_all("div",{"class":"card-body p-0"})
        if len(cards) == count:
            for i in cards:
                try:
                    name = i.find("h3",{"class":"text-dark fs-2 fw-medium pt-one mb-nine"}).text
                except:
                    name = ""
                try:
                    star = i.find("span",{"class":"badge badge-light-warning fs-5 lh-0 w-50px"}).text
                except:
                    star = ""
                try:
                    dist = i.find("span",{"class":"fs-base fs-md-7 fs-xl-seven text-secondary ps-nine"}).text
                except:
                    dist = ""
                try:
                    price= i.find("span",{"class":"ps-1"}).text
                except:
                    price = ""
                try:
                    link = i.find("a",{"class":"btn btn-primary text-white w-100 fs-4 w-md-175px w-xl-200px mb-lg-7 mb-md-4 btn-detail"}).get("href")
                except:
                    link = ""
                try:
                    rating = i.find("div",{"class":"d-flex align-items-center text-white w-30px h-30px bg-purple p-2 rating-radius fs-7 me-3 fw-bold"}).text
                except:
                    rating = ""

                names.append(name.strip())
                stars.append(star.strip())
                distances.append(dist.strip())
                prices.append(price.strip())
                links.append(link.strip())
                scrape_date.append(today)
                checkin_date.append(checkin)
            break
        count = len(cards)  # langsung list of cards
    time.sleep(.5)
    driver.quit()
    time.sleep(1)

vdisplay.stop()
print("total items scraped:", str(len(names)))

data = list(zip(scrape_date,checkin_date,names,prices,stars,distances,links))
rows_inserted = 0
status = "success"
error_message = None
try:
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO bronze.hotel_prices
            (scrape_date, checkin_date, hotel_name, price, stars, dist_to_haram, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            data
        )
        conn.commit()
        print("rows successfully inserted to database: umrah_db")
    run_time = datetime.utcnow().isoformat()
    rows_inserted = len(data)
    logs.append((run_time, status, rows_inserted, error_message))
except Exception as e:
    status = "failed"
    error_message = str(e)
    run_time = datetime.utcnow().isoformat()
    logs.append((run_time, status, rows_inserted, error_message))

with conn.cursor() as cur:
    cur.executemany(
        """
        insert into bronze.scrape_logs
        (run_time, status, rows_inserted, error_message)
        values (%s,%s,%s,%s)
        """,
        logs
    )
    conn.commit()