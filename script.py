from requests_html import HTMLSession 
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
s = HTMLSession()
url_base = "https://www.gvscosmetics.com.ua/"
processed_urls = set()
file_name = os.getenv('file_name')
assistant_id = os.getenv('assistant_id')
api_key_var = os.getenv('api_key_var')
org_id = os.getenv('org_id')
# Print all the text
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def scrape_pro_nac(url):
    global file_name
    soup = getdata(url)

# Find the div with a specific class
    div_with_class = soup.find('div', {'class': 'col-sm-12'})

    # Find all the p tags within that div
    p_tags = div_with_class.find_all('p')

    # Now, p_tags will be a list containing all the p tags within the specified div
    for p_tag in p_tags:
        with open(file_name, 'a', encoding='utf-8') as file:
            if p_tag.text:
                file.write(f"{p_tag.text}")

def scrape_opt_program(url):
    global file_name
    soup = getdata(url)

    div_with_class = soup.find('div', {'class': 'col-sm-12'})
    p_tags = div_with_class.find_all('p')

    for p_tag in p_tags:
        span_tag = p_tag.find('span')
        
        # Check if a span tag is found before trying to access its text content
        if span_tag:
            span_text = span_tag.text
            with open(file_name, 'a', encoding='utf-8') as file:
                if span_text:
                    file.write(f"{span_text}")

def scrape_delivery(url):
    global file_name
    soup = getdata(url)

# Find the div with a specific class
    div_with_class = soup.find('div', {'class': 'col-sm-12'})

    # Find all the p tags within that div
    p_tags = div_with_class.find_all('p')

    # Now, p_tags will be a list containing all the p tags within the specified div
    for p_tag in p_tags:
        with open(file_name, 'a', encoding='utf-8') as file:
            if p_tag.text:
                file.write(f"{p_tag.text}")

def payment_terms(url):
    global file_name
    soup = getdata(url)
    
    div_with_class = soup.find('div', {'class': 'col-sm-12'})
    div_tags = div_with_class.find_all('div')

    for div_tag in div_tags:
        span_tag = div_tag.find('span')
        
        # Check if a span tag is found before trying to access its text content
        if span_tag:
            span_text = span_tag.text
            with open(file_name, 'a', encoding='utf-8') as file:
                if span_text:
                    file.write(f"{span_text}")

# def scrape_contacts(url):
#     soup = get_data(url)
#     div_with_class = soup.find('div', {'class': 'contacts__info-inner'})
#     div_tags = div_with_class.find_all('div', {'class': 'contacts__info-item'})
#     for div_tag in div_tags:
#         address_tag = div_tag.find('address')


#Scrape info about company 
def scrape_info(soup):
    global file_name
    div_with_class_a = soup.find('ul', {'class': 'nav-top__list'})

    # Find all the li tags within that ul
    li_tags = div_with_class_a.find_all('li')

    # Create a list to store 'a' tags
    a_tags_list = []

    # Iterate through li tags
    for li_tag in li_tags:
        # Print the text content of each li tag
        print(li_tag.text)

        # Find the 'a' tag within the current li tag
        a_tag = li_tag.find('a', {'class': 'nav-top__link'})

        # Check if 'a' tag exists before accessing the 'href' attribute
        if a_tag:
            # Append the 'a' tag to the list
            a_tags_list.append(a_tag)

    # Print the first 'a' tag from the list
    if a_tags_list:
        first_a_tag = a_tags_list[0]
        print('THE FIRST ABOUT US LINK IS: ' + first_a_tag['href'])
        scrape_pro_nac(first_a_tag['href'])
        second_a_tag = a_tags_list[1]
        print('THE SECOND OPT PROGRAM LINK IS: ' + second_a_tag['href'])
        scrape_opt_program(second_a_tag['href'])
        third_a_tag = a_tags_list[2]
        scrape_delivery(third_a_tag['href'])
        forth_a_tag = a_tags_list[3]
        payment_terms(forth_a_tag['href'])
    else:
        print('No links found.')

# Get info about products
def scrape_product_details(url, file_path):
    global file_name
    r = s.get(url)
    product_soup = BeautifulSoup(r.text, 'html.parser')

    name = product_soup.find('h1', {'class': 'catalogue__product-name'})
    name_text = name.text.strip() if name else ''

    brand = product_soup.find('a', itemprop="brand")
    brand_text = brand.text.strip() if brand else ''

    description = product_soup.find('div', {'class': 'short-descr editor'}).find('p')
    description_text = description.text.strip() if description else ''

    price = product_soup.find('span', itemprop='price')
    price_text = price.text.strip() if price else ''

    availability_span = product_soup.find('span', {'class': 'products-full-list__status status instock'})
    if availability_span:
        availability = availability_span.text.strip()
        availability_text = 'Є в наявності'
    else:
        availability_text = 'Немає в наявності'

    sku = product_soup.find('span', itemprop='sku')
    sku_text = sku.text.strip() if sku else ''

    mark_span = product_soup.find('div', {'class': 'products-list__label'})
    if mark_span:
        spans = mark_span.find_all('span')
        mark_text = ' '.join(span.text.strip() for span in spans) if spans else ''
    else:
        mark_text = ''

    # Open the file in append mode and write the details
    with open(file_path, 'a', encoding='utf-8') as file:
            if name_text:
                file.write(f"Назва: {name_text}\n")
            if brand_text:
                file.write(f"Бренд: {brand_text}\n")
            if description_text:
                file.write(f"Опис: {description_text}\n")
            if price_text:
                file.write(f"Ціна: {price_text}\n")
            if availability_text:
                file.write(f"Наявність: {availability_text}\n")
            if sku_text:
                file.write(f"Модель: {sku_text}\n")
            if mark_text:
                file.write(f"Відмітка: {mark_text}\n")
            file.write(f"Посилання: {url}\n\n")


def getnewproducts(soup):
    global file_name
    new_products = soup.find('ul', {'class': 'catalogue__products-list catalogue__products-list--four'})
    if new_products:
        a_tags = new_products.find_all('a', {'class': 'products-list__img'})

        for a_tag in a_tags:
            href = a_tag['href']

            if href not in processed_urls:
                print("New Products URL: ", href)
                scrape_product_details(href, file_name)
                processed_urls.add(href)
            else:
                print('Skipping duplicate URL: ', href)

    new_title = soup.find('span', {'class': 'h2'})

    with open(file_name, 'a', encoding='utf-8') as file:
        if new_title:
            file.write(f"{new_title}")

    print(new_title)


def get_products(soup):
    global file_name
    items = soup.find('ul', {'class': 'catalogue__products-list'})

    if items:
        a_tags = items.find_all('a', {'class': 'products-list__img-item'})

        for a_tag in a_tags:
            href = a_tag['href']

            # Check if the URL is already processed
            if href not in processed_urls:
                print("Product URL:", href)
                scrape_product_details(href, file_name)
                processed_urls.add(href)
            else:
                print("Skipping duplicate URL:", href)

def get_next_link(soup):
    global file_name
    nextlink = soup.find('ul', {'class': 'pagination'})
    if nextlink:
        li_tags = nextlink.find_all('li')
        for li_tag in li_tags:
            a_tag = li_tag.find('a', href=True)
            if a_tag:
                url = a_tag['href']
                if url not in processed_urls:
                    print('THE NEXT PAGE IS:', url)
                    soup = getdata(url)
                    get_products(soup)
                    processed_urls.add(url)
            else:
                print("Error: 'a' tag not found within 'li' tag or missing 'href' attribute.")
    else:
        print("Error: 'ul' tag with class 'pagination' not found.")

client = OpenAI(
  organization=org_id,
  api_key = api_key_var
)

def main():
    global file_name
# list the assistant's files
    assistant_files = client.beta.assistants.files.list(
        assistant_id=assistant_id
    )

    fileId = assistant_files.data[0].id
    print('The listed files: ' + fileId)

    # # delete the existing file
    client.beta.assistants.files.delete(
        assistant_id=assistant_id,
        file_id=fileId
    )

    print('File deleted from assistant')

    client.files.delete(fileId)

    print('The file is deleted from OpenAI')
    # upload a file to openai
    file = client.files.create(
        file=open(file_name, "rb"),
        purpose='assistants'
    )

    fileId = file.id
    print('File upload: ' + fileId)

    # # attach the file to an assistant
    assistant_file = client.beta.assistants.files.create(
        assistant_id=assistant_id,
        file_id=fileId
    )
    print(assistant_file)
    print('File created for assistant')


if __name__ == "__main__":
        with open(file_name, 'w', encoding='utf-8') as file:
            pass
        start_url = "https://www.gvscosmetics.com.ua/katalog/?limit=100"
        soup_all = getdata(url_base)
        soup_products_pages = getdata(start_url)
        scrape_info(soup_all)
        getnewproducts(soup_all)
        get_products(soup_products_pages)
        get_next_link(soup_products_pages)
 
        main()

