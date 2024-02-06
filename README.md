# App Store Web Scraper with BS4 and LLM for feature extraction

## Description
This project consists of a Python-based web scraper designed to extract information from App Store listings. It fetches details such as app name, description, and features, and is ideal for those looking to gather data about apps listed on the App Store.

## Getting Started

### Dependencies
- Python 3.x
- Libraries: `requests`, `beautifulsoup4`, `openai`, `python-dotenv`
- An API key from OpenAI (for GPT-3 or compatible models)

### Installing
1. **Clone the repository**
   Use Git to clone the project's repository to your local machine.

```
git clone https://github.com/yeo-menghan/web_scrapping.git
cd appstore-webscraper
```

2. **Set up a Python virtual environment (Optional but recommended)**
This step is optional but recommended to keep dependencies isolated.

```
python -m venv venv
source venv/bin/activate # On Linux/macOS
venv\Scripts\activate # On Windows
```

3. **Install the required packages**
Install the required Python packages using the `requirements.txt` file.
```
pip install -r requirements.txt
```

### Setting up the environment
**Create an `.env` file**
This file should contain your OpenAI API key.

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

### Running the Application
To run the app, use the following command:

```
python appstore_webscrape.py
```

## Usage
After running the script, it will prompt you for a URL or perform actions based on the predefined tasks in the script. Ensure that the URL is a valid App Store product page for accurate results.

The script utilizes the GPT-3.5 Turbo model provided by OpenAI for natural language processing. This model is optimized for generating human-like text responses.

The temperature parameter controls the randomness of the model's output. A higher value, such as 0.8, makes the output more diverse but potentially less coherent, while a lower value, such as 0.2, produces more focused and deterministic responses. You can adjust the temperature in the script to suit your preference and the desired level of variation in the generated feature list.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes.
