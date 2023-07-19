import requests
import shopify
from pybase64 import b64encode

def upload_pdf_to_shopify(pdf_url, pdf_name):
    # Download the PDF from the URL
    response = requests.get(pdf_url)
    pdf_data = response.content
    # Encode the PDF using base64
    encoded_pdf = b64encode(pdf_data).decode("utf-8")

    # Create a new asset object and attach the encoded PDF to it
    asset = shopify.Asset()
    print(pdf_name)
    asset.key = pdf_name
    asset.attachment = encoded_pdf
    asset.save()

    # Retrieve the URL where the PDF now lives
    #pdf_url = f"https://enlineamateriales.myshopify.com{asset.public_url}"
    #return pdf_url