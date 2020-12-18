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

        if(len(raw)==250):
            self.since_id = raw[249]['id']
            self.get_all_customers()

        elif(len(raw)<250):
            last_customers_id = raw[len(raw)-1]['id']
            print("Last CUSTOMER ID is: " + str(last_customers_id))
            print("Total customers: " + str(self.total_customers))

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

        if(len(raw)==250):
            self.since_id = raw[249]['id']
            self.get_all_products()

        elif(len(raw)<250):
            last_products_id = raw[len(raw)-1]['id']
            print("Last PRODUCT ID is: " + str(last_products_id))
            print("Total products: " + str(self.total_products))

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

        # raw_wanted_fields = response.json()['orders']
        # i = len(raw_wanted_fields)
        # wanted_fields=["id", "email", "created_at", "updated_at", "total_price", "subtotal_price", "financial_status", "confirmed", \
        #         "name", "cancel_reason", "processed_at", "app_id", "discount_codes", "tags", "total_discounts_set", \
        #         "total_shipping_price_set", "billing_address", "customer", "cancelled_at"]
        # field_billing_address = ["address1", "phone", "city", "zip", "province", "country", "latitude", "longitude"]
        # while(i > 0):
        #     for c in wanted_fields:
        #         if c in raw_wanted_fields[i-1]:
        #             if c == 'total_discounts_set':
        #                 if 'amount' not in raw_wanted_fields[i-1][c]['shop_money']:
        #                     raw_wanted_fields[i-1][c]['shop_money']['amount'] = 'n/a'
        #             if c == 'total_shipping_price_set':
        #                 if 'amount' not in raw_wanted_fields[i-1][c]['shop_money']:
        #                     raw_wanted_fields[i-1][c]['shop_money']['amount'] = 'n/a'
        #             if c == 'customer':
        #                 if 'id' not in raw_wanted_fields[i-1][c]:
        #                     raw_wanted_fields[i-1][c]['id'] = 'n/a'
        #             if c == 'billing_address':
        #                 for o in field_billing_address:
        #                     if o not in raw_wanted_fields[i-1][c]:
        #                         raw_wanted_fields[i-1][c][o] = 'n/a'
        #         else:
        #             raw_wanted_fields[i-1][c]='n/a'
        #     i -= 1

        # tmp_orders_wanted_fields = pd.DataFrame(raw_wanted_fields)
        # self.df_wanted_fields = self.df_wanted_fields.append(tmp_orders_wanted_fields)
        #  #

        if(len(raw)==250):
            self.since_id = raw[249]['id']
            self.get_all_orders() 

        elif(len(raw)<250):
            last_orders_id = raw[len(raw)-1]['id']
            print("Last ORDER ID is: " + str(last_orders_id))
            print("Total orders: " + str(self.total_orders))

            return self.df

            # df_wanted_fields_to_dict = self.df_wanted_fields.to_dict(orient='records')
            # df_all_to_dict = self.df.to_dict(orient='records')
            # j = len(df_all_to_dict)
            # k = len(df_wanted_fields_to_dict)

            # node = []
            # j = len(df_all_to_dict)
            # header = ['id', 'lineitem_name', 'lineitem_product_id', 'lineitem_price', 'lineitem_sku', 'lineitem_quantity', 'lineitem_discount']
            # with open('shopify_orders_lineitem.csv', 'w', newline='') as write_obj_post:
            #     csv_writer = writer(write_obj_post)
            #     csv_writer.writerow(header)
            # while(j > 0):
            #     node.append(df_all_to_dict[j-1]['id'])
            #     for iems in df_all_to_dict[j-1]['line_items']:
            #         node.append(iems['title'])
            #         node.append(iems['product_id'])
            #         node.append(iems['price'])
            #         node.append(iems['sku'])
            #         node.append(iems['quantity'])
            #         node.append(iems['total_discount'])
            #         with open('shopify_orders_lineitem.csv', 'a+', newline='') as write_obj_post:
            #             csv_writer = writer(write_obj_post)
            #             csv_writer.writerow(node)
            #         node = []
            #         node.append(df_all_to_dict[j-1]['id'])
            #     node = []
            #     j -= 1
            # data_orders_lineitem = pd.read_csv("shopify_orders_lineitem.csv")
            #  #

            # return data_orders_lineitem