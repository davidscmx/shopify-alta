
import shopify
import requests
from get_products import extract_product_info, extract_menu_links
from upload_pdf import upload_pdf_to_shopify
import os

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

    products_info = extract_product_info(response.content)

    for product_info in products_info:
        print(product_info)
        print(f'Products in {product_info}:')

        pdf_urls = []
        for i, pdf_url in enumerate(product_info['file_paths']):
            pdf_url = old_website_url+"/"+pdf_url
            upload_pdf_to_shopify(pdf_url, f"{product_info['product_name']}_{i}")
            pdf_urls.append(pdf_url)

        # Create a new product
        #new_product = shopify.Product()
        #new_product.title = product_info['product_name']
        #new_product.product_type = section 
        #new_product.body_html = f'<p>{product_info["product_description"]}</p>\nM<p>a href={pdf_url} style="font-size: 1.875rem;" target="_blank" rel="noopener noreferrer"> Descargar Ficha Técnica</a></p>'
        
        
        #with open(path, "rb") as f:
        #    filename = path.split("/")[-1:][0]
        #    encoded = f.read()
        #    image.attach_image(encoded, filename=filename)
        
        #success = new_product.save() #returns false if the record is invalid
        ## or
        #if new_product.errors:
        #    pass
        ##something went wrong, see new_product.errors.full_messages() for example
#
        # Update a product
        #new_product.handle = "burton-snowboard"
        #new_product.save()

        break
    break

#products = shopify.Product.find()
#print(products[0].attributes)
#print(products[0].title)

#print(products[0].body_html)
