import pandas as pd
import flask
from flask import request, jsonify, redirect, url_for, render_template
import requests
from pandas.io import gbq
from flask_cors import CORS, cross_origin
import json
from helper import shopifydata

app = flask.Flask(__name__)
cors = CORS(app, resources = {r"/*": {"origins" : "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

@app.route('/orders', methods=["POST"])
@cross_origin()
def orders():
    try:
        api_key = request.args.get("api_key")
        secret = request.args.get("secret")
        password = request.args.get("password")
        shop = request.args.get("shop")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
    
        # api_key = "593b197053b69e47eddf888f385aa031"
        # secret = "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"
        # password = "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"
        # shop = "natura-malasia"
        # start_date = "2020-01-01"
        # end_date = "2020-03-01"

        # api_key = "962b7f897d3284cb320d4d194d27dccf"
        # secret = "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"
        # password = "a94cdaad05ee6bb41320f99735c04336"
        # shop = "harryandchewie"
        # start_date = "2018-01-01"
        # end_date = "2020-12-01"

        data = {
            "apikey": api_key,
            "appsecret" : secret,
            "apppassword" : password,
            "shopname": shop,
            "startdate" : start_date,
            "enddate" : end_date
        }
        
        shopify = shopifydata(data)
        shopify_orders = shopify.get_all_orders()
        return jsonify({"result": shopify_orders.to_dict(orient='records')})

    except Exception as e:
        return jsonify(error=str(e)), 404

@app.route('/customers', methods=["POST"])
@cross_origin()
def customers():
    try:
        api_key = request.args.get("api_key")
        secret = request.args.get("secret")
        password = request.args.get("password")
        shop = request.args.get("shop")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
    
        # api_key = "962b7f897d3284cb320d4d194d27dccf"
        # secret = "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"
        # password = "a94cdaad05ee6bb41320f99735c04336"
        # shop = "harryandchewie"
        # start_date = "2018-01-01"
        # end_date = "2020-12-01"

        data = {
            "apikey": api_key,
            "appsecret" : secret,
            "apppassword" : password,
            "shopname": shop,
            "startdate" : start_date,
            "enddate" : end_date
        }
        
        shopify = shopifydata(data)
        shopify_customers = shopify.get_all_customers()
        return jsonify({"result": shopify_customers.to_dict(orient='records')})

    except Exception as e:
        return jsonify(error=str(e)), 404

@app.route('/products', methods=["POST"])
@cross_origin()
def products():
    try:
        api_key = request.args.get("api_key")
        secret = request.args.get("secret")
        password = request.args.get("password")
        shop = request.args.get("shop")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
    
        # api_key = "962b7f897d3284cb320d4d194d27dccf"
        # secret = "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"
        # password = "a94cdaad05ee6bb41320f99735c04336"
        # shop = "harryandchewie"
        # start_date = "2018-01-01"
        # end_date = "2020-12-01"

        data = {
            "apikey": api_key,
            "appsecret" : secret,
            "apppassword" : password,
            "shopname": shop,
            "startdate" : start_date,
            "enddate" : end_date
        }
        
        shopify = shopifydata(data)
        shopify_products = shopify.get_all_products()
        return jsonify({"result": shopify_products.to_dict(orient='records')})

    except Exception as e:
        return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080, host= '0.0.0.0')

    # gcloud run deploy shopify-connector --image $DOCKER_IMG --platform managed --region $REGION --allow-unauthenticated