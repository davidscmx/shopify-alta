import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from unidecode import unidecode

def extract_menu_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    menu_links = []
    td_tags = soup.find_all('td', class_='menu_lateral')
    for td_tag in td_tags:
        link_text = td_tag.text
        onclick_value = td_tag.get('onclick')
        if onclick_value:
            html_file = onclick_value.split("'")[1]
            absolute_url = urljoin(url, html_file)
            menu_links.append((link_text, absolute_url))

    return menu_links


def remove_non_alphanumeric(text):
    normalized_text = unidecode(text)

    # Use regex to remove all characters that are not numbers or letters
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_text)
    cleaned_text = cleaned_text.replace('\n', ' ')
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text


def clean_titles(text):
    text = text.strip()
    text = text.replace('\t', '')
    text = remove_non_alphanumeric(text)
    return text

def process_shingle_products(soup):

    product_element = soup.find(text="Shingle Classic")
    target_value = "20 años"
    descrition_element = soup.find(lambda element: target_value.lower() in element.get_text().lower(),
                                   class_="txt_productos_ancho")

    target_value = "Shingle"

    print(descrition_element)
    print(product_element)
    exit()

    #for p_table in parent_tables:
    #    product_element = parent_tables.find('td', class_=['txt_tabla_titulo'], text="Shingle Classic")

    #    product_element = p_table.find_all('td', class_=['txt_tabla_titulo'])
    #    variant_elements = p_table.find_all('td', class_=['bg_tabla', 'bg_tabla_sin_espacio'])
    #    description_element = p_table.find_all('td', class_=['txt_productos', 'txt_productos_ancho'])
#
    #    print(description_element, len(description_element))
    #    for i, p_el in enumerate(product_element):
#
    #        product_title = clean_titles(p_el.text)
#
    #        if description_element:
    #            description = clean_titles(description_element[i].text)
#
    #        print(product_title)
    #        print(description)
#
    #        #for var_el in variant_elements:
    #        #    var_name = var_el.find("td", class_="txt_caracteristicas_relleno")
    #        #    variants.append(var_name.text)
#
    #    #print(variants)
    #    #exit()
    #    #chars_elements = table.find_all('td', class_='txt_caracteristicas_relleno')
    #    #for characteristic_element in chars_elements:
    #    #       characteristic_element = characteristic_element.text.strip()
    #    #    characteristic_element = characteristic_element.replace('\t', '')
    #    #    characteristics.append(characteristic_element)
#
    #    #print(product_title)
    #    #print(description)
#
    #    #product_name = product_title
    #    ## Initialize variables for each product
    #    #product_description = ''
    #    #characteristics = description
    #    #images = []
    #    #file_paths = {}
##
    #    #    print(prod)
    #    exit()
#

def extract_product_info(html):
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize a list to store product information
    products = []

    # Find the parent table that contains the product information
    parent_table = soup.find('table', align='center', width='710')
    section = parent_table.find('td', class_=['txt_titulo_pagina'])

    if section.text == "SHINGLE":
        parent_tables = parent_table.find_all("table", align="center", width='340')
    else:
        parent_tables = [parent_table]

    #product_info = process_shingle_products(soup)
    for p_table in parent_tables:
        # Find all the child tables that represent individual products
        product_tables = p_table.find_all('td', class_=['bg_tabla', 'bg_tabla_sin_espacio'])

        # Iterate over each product table and extract the information
        for table in product_tables:

            # Initialize variables for each product
            product_name = ''
            product_description = ''
            characteristics = []
            images = []
            file_paths = {}

            title_element = table.find('td', class_=['txt_tabla_titulo', 'txt_titulo_pagina'])

            if title_element:
                product_name = title_element.text.strip()
                product_name = product_name.replace('\t', '')

            description_element = table.find('td', class_='txt_productos')
            description_element1 = table.find('td', class_='txt_productos_ancho')

            if description_element:
                product_description = description_element.text.strip()
                product_description = product_description.replace('\t', '')
            elif description_element1:
                product_description = description_element1.text.strip()
                product_description = product_description.replace('\t', '')

            characteristics_elements = table.find_all('td', class_='txt_caracteristicas_relleno')
            for characteristic_element in characteristics_elements:
                characteristic_element = characteristic_element.text.strip()
                characteristic_element = characteristic_element.replace('\t', '')
                characteristics.append(characteristic_element)

            image_element = table.find('img')
            if image_element:
                images.append(image_element['src'])

            file_elements = table.find_all('a')
            for file_element in file_elements:
                file_paths[file_element.text] = file_element['href']
            #print(file_paths)
            # Create a dictionary to store the extracted information
            product_info = {
                'product_name': product_name,
                'product_description': product_description,
                'characteristics': characteristics,
                'images': images,
                'file_paths': file_paths
            }

            # Add the product information to the list
            products.append(product_info)

    # Return the list of products
    return products


# URL of the website
#website_url = "https://www.altamateriales.com.mx"

# Print the result
#for link in extract_menu_links(website_url):
#    section = link[0]
#    url = link[1]
#
#    response = requests.get(url)
#
#    product_info = extract_product_info(response.content)
#
#    print(f'Products in {product_info}:')
#    break