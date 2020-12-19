import requests
import pandas as pd
from datetime import datetime, timedelta, date
import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta
import numpy as np
import json
from csv import writer

class shopifydata:

    def __init__(self, auth:dict):
        self.apikey  = auth['apikey']
        self.appsecret = auth['appsecret']
        self.apppassword = auth['apppassword']
        self.shopname = auth["shopname"]
        self.startdate = auth['startdate']
        self.enddate = auth['enddate']
        self.total_customers = 0
        self.total_products = 0
        self.total_orders = 0
        self.since_id = 0
        self.df = pd.DataFrame()
        self.df_wanted_fields = pd.DataFrame()
        self.orders_id = []

    #--------------CUSTOMERS--------------#
    def get_all_customers(self):

        url = "https://%s:%s@%s.myshopify.com/admin/api/2020-07/customers.json?limit=250&created_at_min=%s&created_at_max=%s&since_id=%s" \
            %(self.apikey, self.apppassword, self.shopname, self.startdate, self.enddate, self.since_id)
        response = requests.get(url)

        raw = response.json()['customers']
        self.total_customers += len(raw)

        tmp_customers = pd.DataFrame(raw)
        self.df = self.df.append(tmp_customers)

        return self.df

    #--------------PRODUCTS--------------#
    def get_all_products(self):

        url = "https://%s:%s@%s.myshopify.com/admin/api/2020-07/products.json?limit=250&created_at_min=%s&created_at_max=%s&since_id=%s" \
            %(self.apikey, self.apppassword, self.shopname, self.startdate, self.enddate, self.since_id)
        response = requests.get(url)

        raw = response.json()['products']
        self.total_products += len(raw)

        tmp_products = pd.DataFrame(raw)
        self.df = self.df.append(tmp_products)

        return self.df

    #--------------ORDERS--------------#
    def get_all_orders(self):

        url = "https://%s:%s@%s.myshopify.com/admin/api/2020-07/orders.json?status=any&limit=250&created_at_min=%s&created_at_max=%s&since_id=%s" \
            %(self.apikey, self.apppassword, self.shopname, self.startdate, self.enddate, self.since_id)
        response = requests.get(url)

        raw = response.json()['orders']
        tmp_orders = pd.DataFrame(raw)
        self.df = self.df.append(tmp_orders)
        self.total_orders += len(raw)

        return self.df