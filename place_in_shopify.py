
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


def download_images(query, folder, additional_search, limit=14):
    print(query, folder, additional_search, limit)
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

    # Save the new image to the productbreak
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

#def get_additional_search_term(product_title, section):
def create_list_from_newlines(input_list):
    # Create an empty list to store the result
    result_list = []

    # Iterate through each string in the input list
    for string in input_list:
        # Split the string into substrings using the new line character '\n' as the delimiter
        substrings = string.split('\n')

        # Extend the result_list with the substrings to add them as separate elements
        result_list.extend(substrings)

    return result_list


def improve_titles(section, product_title, product_title_cleaned):
    # Plafon
    if section == "PLAFONES USG":
        product_title = "Plafón "+product_title+" USG"
    if section == "AISLANTES":
        product_title = "Aislante "+product_title
    if product_title_cleaned == "CONECTORES PARA MADERA":
        product_title = "USP  "+product_title

    return product_title


def join_elements_with_space(input_list):
    # Ensure the list has an even number of elements
    if len(input_list) % 2 != 0:
        input_list = [item.replace('\xa0', '') for item in input_list]

        return input_list

    # Initialize an empty list to store the joined strings
    joined_list = []

    # Iterate over the input_list by steps of 2
    for i in range(0, len(input_list), 2):
        input_list[i] = input_list[i].replace('\xa0', '')
        input_list[i + 1] = input_list[i + 1].replace('\xa0', '')

        joined_string = input_list[i] + " " + input_list[i + 1]
        joined_list.append(joined_string)

    return joined_list

def remove_from_descargar(text):
    index_descargar = text.find('DESCARGAR')
    if index_descargar != -1:
        # If 'DESCARGAR' is found, remove everything from its position onward
        result = text[:index_descargar]
    else:
        # If 'DESCARGAR' is not found, return the original text
        result = text
    return result.strip()  # Remove leading and trailing whitespaces (optional)


def create_collection(section):
    collection = shopify.SmartCollection()
    collection.title = section
    collection.template_suffix = "sin-precio-ni-agotado"

    existing_collection = shopify.SmartCollection.find_first(title=collection.title)
    if not existing_collection:
        print("Collection does not exist, will create new")
        collection.published_scope = "global"

        collection.rules = {
            'column': 'type',
            'relation': 'equals',
            'condition': section
        },

        collection.save()
    else:
        print("Collection already exists.")


def process_string_cal(s):
    # Replace commas and "y" with spaces to simplify splitting
    s = s.replace(',', '').replace(' y ', ' ').replace(".", "")
    # Split the string into words
    words = s.split()
    # Prepare a list to store the results
    result = []

    # Iterate over the words
    for i in range(len(words)):
        # Check if the word is numeric
        if words[i].isdigit():
            # Combine "Cal." with the number and add to the results
            result.append("Cal. " + words[i])

    return result

already_processed = ["TABLAROCA", "PERFILES METÁLICOS USG"]

for link_number, link in enumerate(extract_menu_links(old_website_url)):
    
    section = link[0]
    url = link[1]
    
    if section in already_processed:
        continue
    
    response = requests.get(url)
    products = extract_product_info(response.content)

    create_collection(section)

    for product in products:
        product_title = product['product_name']
        print("original ", product["characteristics"])
        possible_variant = create_list_from_newlines(product["characteristics"])
        
        if section == "PERFILES METÁLICOS USG":
            possible_variant = join_elements_with_space(possible_variant)
            if product_title == "Alambre Galvanizado":
                possible_variant = process_string_cal(possible_variant[0])
        if section == "ADHESIVOS Y COMPUESTOS":
            
            if product_title == "Cinta Para DUROCK®":
                possible_variant = [item for item in possible_variant if item != '']
            else:
                possible_variant = join_elements_with_space(possible_variant)

        print(product_title)
        print(possible_variant)

        
        if not product_title:
            continue
        product_title_cleaned = clean_string(product_title)

        # Create a new product
        new_product = shopify.Product()
        new_product.title = product_title

        # check if product exists
        existing_product = shopify.Product.find_first(title=new_product.title)
        if existing_product:
            print("Product already exists, will not add it again")
            continue

        new_product.options = [
           {'name': 'Size'},  # Option 1
        ]
        new_product.vendor = get_product_vendor(section, product_title)
        print(new_product.vendor)
        new_product.product_type = section
        new_product.template_suffix = "sin-precio-ficha-tec"
        
        product_description = remove_from_descargar(product["product_description"])
        html_string = f'<p>{product_description}</p>'                            
        
        if len(product['file_paths']) > 0:
            for pdf_name, pdf_url in product['file_paths'].items(): 
                pdf_url = old_website_url+"/"+pdf_url
                pdf_name = pdf_name.replace("DESCARGAR FICHA TÉCNICA","").title()
                
                str_to_be_added = (f'\n\n<p><a href={pdf_url} style="font-size: 1.875rem;" '
                                  f'target="_blank" rel="noopener noreferrer">'
                                  f'Descargar Ficha Técnica{pdf_name}</a></p>\n')

                html_string+= str_to_be_added
          
        new_product.body_html = html_string

        new_product.options = [
           {'name': 'Size'},  # Option 1
        ]
        new_product.save()

        if new_product.errors:
            print("Product was not saved successfully.")
            print(new_product.errors.full_messages())
        else:
            print("Product was saved successfully.")

        variants = []
        for my_var in possible_variant:
            if "Medida:" in my_var:
                my_var = my_var.replace("Medida: ", "")

            variant = shopify.Variant()
            variant.product_id = new_product.id
            variant.option1 = my_var

            if variant.save():
                print('Successfully created a variant')
            else:
                print('Failed to create a variant')
                print(variant.errors.full_messages())

        # Delete the default variant
        default_variant = [v for v in new_product.variants if v.title == 'Default Title']
        if default_variant:
            default_variant[0].destroy()

        additional_search_str = None
        if section == "TABLAROCA" or section == "PERFILES METÁLICOS USG" or section=="ADHESIVOS Y COMPUESTOS":
            additional_search_str = "USG"

        download_images(product_title, product_title_cleaned, additional_search_str)
        for i, image in enumerate(Path(f"./images/{product_title_cleaned}/").iterdir()):
            save_image_to_shopify(f'{image}', new_product.id, position=i)
        
    break