from bs4 import BeautifulSoup
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
import platform

# Get OpenAI API key
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
  api_key=key,
)

# Input the job posting link and get the HTML content
link = input("Enter the job posting link: ")
website = requests.get(link)
website.raise_for_status()
html_content = website.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Search for Job Title and Company Name
job_title = soup.find('h1', {'class': 'app-title'}).text.strip()
company_name = soup.find('span', {'class': 'company-name'}).text.strip()
description_raw = soup.find('div', {'id': 'content'})
description = ''

for elem in description_raw:
    text = elem.get_text(separator='\n', strip=True)
    description += text + '\n'

# Saving the File
def sanitize_filename(name):
    return "".join([c if c.isalnum() or c in " _-()" else " " for c in name])

file_name = sanitize_filename(f"{job_title} {company_name}") + ".txt"
downloads_path = os.path.join(os.getcwd(), 'jobs')
full_path = os.path.join(downloads_path, file_name)

with open(full_path, 'w') as file:
    file.write(description.strip())

print(f"File saved to {full_path}")