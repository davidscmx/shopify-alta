
import shopify
import requests
import base64
import re
from pathlib import Path
from get_products import extract_product_info, extract_menu_links
from bing_image_downloader import downloader
from unidecode import unidecode
import os


def replace_spaces_with_underscore(string):
    return re.sub('\s+', '_', string)


def clean_string(string):
    print(repr(string))
    string = string.strip()
    string = string.replace("\n", " ")
    string = string.lower()
    string = string.replace('®', '')
    string = string.strip()
    string = string.replace('/', '_')

    string = replace_spaces_with_underscore(string)
    string = string.replace(" ", "_")
    string = unidecode(string)
    return string


def download_images(query, folder, additional_search, limit=10):
    print(query, folder, additional_search)
    downloader.download(query, folder, additional_search, limit=limit, output_dir="images",
                        adult_filter_off=True, force_replace=False, timeout=60)


def save_image_to_shopify(image_path, product_id, position=1):
    # Open the image file from your local directory and read its binary data
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Create a new product image using the image data
    new_image = shopify.Image.create({
        'product_id': product_id,
        'position': position,
        'attachment': base64.b64encode(image_data).decode('utf-8')
    })

    # Save the new image to the product
    new_image.save()


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

    collection = shopify.SmartCollection()
    collection.title = section

    collection.rules = {
        'column': 'type',
        'relation': 'equals',
        'condition': section
    },

    collection.save()
    # https://www.mitek-us.com/
    for product in products:
        product_title = product['product_name']
        if not product_title:
            continue
        product_title_cleaned = clean_string(product_title)

        # Create a new product
        new_product = shopify.Product()
        new_product.title = product_title
        new_product.product_type = section
        new_product.template_suffix = "sin-precio-ficha-tecnica"

        if len(product['file_paths']) > 0:
            pdf_url = old_website_url+"/"+product['file_paths'][0]
            new_product.body_html = new_product.body_html = (
                                    f'<p>{product["product_description"]}</p>\n\n'
                                    f'<p><a href={pdf_url} style="font-size: 1.875rem;" '
                                    f'target="_blank" rel="noopener noreferrer">'
                                    f'Descargar Ficha Técnica</a></p>')
        else:
            new_product.body_html = f'<p>{product["product_description"]}</p>'

        print("Saving product")
        new_product.save()
        if "tabla" in product_title_cleaned:
            additional_search = "USG"
        else:
            additional_search = None

        download_images(product_title, product_title_cleaned, additional_search, limit=10)
        for i, image in enumerate(Path(f"./images/{product_title_cleaned}/").iterdir()):
            save_image_to_shopify(f'{image}', new_product.id, position=i)

    break