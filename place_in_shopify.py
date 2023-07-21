
import shopify
import requests
import base64
import re
from pathlib import Path

from bing_image_downloader import downloader
from unidecode import unidecode
import os


from get_products import extract_product_info, extract_menu_links
from get_vendor import get_product_vendor


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


def collection_exists(collection_title):
    # Use find() with the title query parameter to search for the collection directly
    existing_collections = shopify.CustomCollection.find(title=collection_title)
    return len(existing_collections) > 0


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
    collection.template_suffix = "sin-precio-ni-agotado"

    existing_collection = shopify.SmartCollection.find_first(title=collection.title)
    if not existing_collection:
        print("Collection does not exist, will create new")
        continue

        collection.published_scope = "global"

        collection.rules = {
            'column': 'type',
            'relation': 'equals',
            'condition': section
        },

        collection.save()

    for product in products:
        product_title = product['product_name']
        if not product_title:
            continue
        product_title_cleaned = clean_string(product_title)

        # Plafon
        if section == "plafones_usg":
            product_title = "Plafón "+product_title

        if product_title_cleaned == "aislantes":
            product_title = "Aislante "+product_title

        if product_title_cleaned == "conectores_para_madera":
            product_title = "USP  "+product_title

        # Create a new product
        new_product = shopify.Product()
        new_product.title = product_title

        # check if product exists
        existing_product = shopify.Product.find_first(title=new_product.title)
        if existing_product:
            print("Product already exists, will not add it again")
            continue

        new_product.vendor = get_product_vendor(section, product_title)
        new_product.product_type = section
        new_product.template_suffix = "sin-precio-ficha-tec"

        if len(product['file_paths']) > 0:
            pdf_url = old_website_url+"/"+product['file_paths'][0]
            print("before striping ", product["product_description"])
            product_description = product["product_description"].replace("DESCARGAR FICHA TÉCNICA","")
            print("before striping ", product_description)
            new_product.body_html = new_product.body_html = (
                                    f'<p>{product_description}</p>\n\n'
                                    f'<p><a href={pdf_url} style="font-size: 1.875rem;" '
                                    f'target="_blank" rel="noopener noreferrer">'
                                    f'Descargar Ficha Técnica</a></p>')
        else:
            new_product.body_html = f'<p>{product["product_description"]}</p>'

        print("Saving product")
        new_product.save()

        download_images(product_title, product_title_cleaned, new_product.vendor, limit=10)
        for i, image in enumerate(Path(f"./images/{product_title_cleaned}/").iterdir()):
            save_image_to_shopify(f'{image}', new_product.id, position=i)