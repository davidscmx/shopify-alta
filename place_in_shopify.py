
import shopify
from get_products import extract_product_info, extract_menu_links

import os

website_url = "enlineamateriales.myshopify.com"
token = os.environ.get('SHOPIFY_TOKEN')

api_session = shopify.Session(website_url, "2023-04", token)
shopify.ShopifyResource.activate_session(api_session)

products = shopify.Product.find()
products[0].title