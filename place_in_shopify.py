
import shopify
import requests
from get_products import extract_product_info, extract_menu_links
from upload_pdf import upload_pdf_to_shopify
from bing_image_downloader import downloader
import os


def download_images(query):
    downloader.download(query, limit=5, output_dir='images', adult_filter_off=True, force_replace=False, timeout=60)


download_images("cute kittens")

website_url = "enlineamateriales.myshopify.com"
token = os.environ.get('SHOPIFY_TOKEN')

api_session = shopify.Session(website_url, "2023-04", token)
shopify.ShopifyResource.activate_session(api_session)

# Print the result
old_website_url = "https://www.altamateriales.com.mx"

for link in extract_menu_links(old_website_url):
    section = link[0]
    url = link[1]

    response = requests.get(url)
    products = extract_product_info(response.content)

    for product in products:

        pdf_urls = []
        for i, pdf_url in enumerate(product['file_paths']):
            pdf_url = old_website_url+"/"+pdf_url
            upload_pdf_to_shopify(pdf_url, f"{product['product_name']}_{i}")
            #pdf_urls.append(pdf_url)

#        # Create a new product
#        #new_product = shopify.Product()
#        #new_product.title = product_info['product_name']
#        #new_product.product_type = section
#        #new_product.body_html = f'<p>{product_info["product_description"]}</p>\nM<p>a href={pdf_url} style="font-size: 1.875rem;" target="_blank" rel="noopener noreferrer"> Descargar Ficha Técnica</a></p>'
#
#
#        #with open(path, "rb") as f:
#        #    filename = path.split("/")[-1:][0]
#        #    encoded = f.read()
#        #    image.attach_image(encoded, filename=filename)
#
#        #success = new_product.save() #returns false if the record is invalid
#        ## or
#        #if new_product.errors:
#        #    pass
#        ##something went wrong, see new_product.errors.full_messages() for example
##
#        # Update a product
#        #new_product.handle = "burton-snowboard"
#        #new_product.save()
#
#        break
#    break
#
#