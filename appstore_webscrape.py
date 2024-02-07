## TODO: create a similarity search between the description and company's feature list

# Web scrapping
from bs4 import BeautifulSoup
import requests

# openAI
from openai import ChatCompletion
import openai

# retrieve .env
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Replace 'your_url_here' with the actual URL you want to scrape
# url = 'https://apps.apple.com/us/app/facebook/id284882215'
url = 'https://apps.apple.com/us/app/mobile-legends-bang-bang/id1160056295'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

def scrape_appstore_name(soup):
    '''
    Get the Title and remove the age tag
    '''
    app_name = soup.find("h1", class_="product-header__title app-header__title")
    if app_name:
        # Get text with no separator to ensure contiguous string, then strip leading/trailing spaces
        app_name_text = app_name.get_text(separator=' ', strip=True)
        # Split by spaces to work with individual words
        words = app_name_text.split()
        # Retain words that are purely alphabetic, discarding age tags or other numeric/alphanumeric parts
        filtered_words = [word for word in words if word.isalpha()]
        # Join the filtered words back into a string
        output = ' '.join(filtered_words)
    else:
        print("no title found")
        output = ""
    return output

def scrape_appstore_description(soup):
    '''
    Get the text from the paragraph, this should exclude the visuallyhidden heading
    '''
    app_description_div = soup.find("div", class_="section__description")
    if app_description_div:
        app_description_p = app_description_div.find("p")
        output = ' '.join(app_description_p.get_text(separator=' ').split())
    else:
        print("no description found")
        output = ""
    return output

def scrape_appstore_information(soup, search_label):
    '''
    Retrieve information on Seller, Size, Category, Languages, Price from the App Store page.
    Additionally, extract supported platforms if search_label is 'Compatibility'.
    '''
    # General information extraction
    if search_label != 'Compatibility':
        category_label = soup.find('dt', string=search_label)
        if category_label:
            category_definition = category_label.find_next_sibling('dd', class_='information-list__item__definition')
            if category_definition:
                output = category_definition.text.strip()
                return output
        else:
            print("no info found via the search label")
            return ""
    # Special handling for 'Compatibility'
    elif search_label == 'Compatibility':
        terms = soup.find_all('dt', class_='information-list__item__definition__item__term')
        if terms:
            device_names = [term.text.replace('\xa0', ' ').strip() for term in terms]
            return device_names # returns array
        else:
            print("nothing found for compatibility")
            return ""

def scrape_appstore_in_app_purchases(soup):
    '''
    Scrape in-app purchases under information section and return a dictionary
    Does not return duplicates; returns the latest name and price of the duplicated entity
    '''
    purchases = {}
    in_app_purchases = soup.find_all('li', class_='list-with-numbers__item')
    if in_app_purchases:
        for item in in_app_purchases:
            title_span = item.find('span', class_='list-with-numbers__item__title')
            price_span = item.find('span', class_='list-with-numbers__item__price')
            if title_span and price_span:
                title = title_span.text.strip()
                price = price_span.text.strip()
                purchases[title] = price
        return purchases # returns dictionary
    else:
        return ""

def scrape_appstore_contact_info(soup):
    '''
    Scrape the url links for Developer Website & App Support
    '''
    contact_info = {}

    # Finding all 'a' tags that contain the text we're interested in.
    all_links = soup.find_all('a', class_='link')
    for link in all_links:
        if 'Developer Website' in link.text:
            contact_info['developer_website'] = link.get('href')
        elif 'App Support' in link.text:
            contact_info['app_support'] = link.get('href')

    return contact_info # returns dictionary

product_name = scrape_appstore_name(soup)
product_description = scrape_appstore_description(soup)
print("Product name: " + product_name)
print("Product description: " + product_description + "\n\n")

def generate_feature_list(name, description):
    '''
    Takes in product name and description to generate a generic feature list of the application.
    Generation is managed by OpenAI.
    '''
    # Initialize the OpenAI API
    openai.api_key = openai_api_key

    example_list = [
            "User Profile",
            "News Feed",
            "Friend System",
            "Status Updates",
            "Likes and Reactions",
            "Comments",
            "Messenger",
            "Notifications",
            "Events",
            "Groups",
            "Pages",
            "Marketplace",
            "Gaming",
            "Privacy Settings",
            "Search",
            "Live Video",
            "Photo and Video Sharing",
            "Profile Customization",
            "Marketplace",
            "Advertising",
            "Fundraisers",
            "Check-Ins"
        ]

    # Define the product name and its description
    name = "Social Networking Platform"
    description = ("A comprehensive social media platform allowing users to connect with friends and family, "
                "share updates, photos, and videos, join communities of interest, and discover content. "
                "Enables businesses to create pages, advertise products, and engage with their audience. "
                "Features include real-time messaging, event planning, marketplace for buying and selling goods, "
                "gaming, live streaming, and privacy controls to manage visibility and interactions.")

    # Formulate the few-shot prompt
    prompt = (f"Given the description of '{name}', a '{description}', generate a list of potential features. "
            f"Here are some examples of features for similar platforms: \n"
            f"{example_list} \n"
            f"Based on the {product_name} and {product_description}, what are other features that might be considered? "
            f"Make sure these features are within the contact of website and application development."
            f"List them in a similar, concise manner. Output should be a Python list of strings, each representing a feature.")

    # Use ChatCompletion or an equivalent method to generate the response
    try:
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with your preferred model version
            messages=[{"role": "system", "content": "Extract a feature list from a product description."},
                      {"role": "user", "content": prompt}],
                      temperature=0.0
        )

        # Extracting the feature list from the response
        feature_string = response.choices[0].message['content']
        feature_list = [feature.strip().replace('- ', '') for feature in feature_string.split('\n') if feature.strip()]
        return feature_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
feature_list = generate_feature_list(product_name, product_description)
print("Feature List: \n")
print(feature_list)
