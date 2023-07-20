
import shopify
import requests
import base64
from pathlib import Path
from get_products import extract_product_info, extract_menu_links
from upload_pdf import upload_pdf_to_shopify
from bing_image_downloader import downloader
import os

def remove_non_ascii(string):
    """
    Remove non-ASCII characters from a string.
    
    Parameters:
        string (str): The input string.
        
    Returns:
        str: The string with non-ASCII characters removed.
    """
    return ''.join(char for char in string if ord(char) < 128)


def download_images(query, limit=10):
    downloader.download(query, limit=limit, output_dir="images", adult_filter_off=True, force_replace=False, timeout=60)

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

    for product in products:
        product_title = product['product_name']
        # Create a new product
        new_product = shopify.Product()
        new_product.title = product_title
        new_product.product_type = section

        if len(product['file_paths']) > 0:
            pdf_url = old_website_url+"/"+product['file_paths'][0]
            new_product.body_html = f'<p>{product["product_description"]}</p>\n\n<p><a href={pdf_url} style="font-size: 1.875rem;" target="_blank" rel="noopener noreferrer"> Descargar Ficha Técnica</a></p>'
        else:
            new_product.body_html = f'<p>{product["product_description"]}</p>'
        
        print("Saving product")
        new_product.save()

        query = product_title +" "+"USG"
        download_images(query, limit=10)
        for i, image in enumerate(Path(f"./images/{query}/").iterdir()):
            save_image_to_shopify(f'{image}', new_product.id, position=i)
            


