from bs4 import BeautifulSoup
import requests
import openai

openai.api_key = ""

# Input the job posting link and get the HTML content
link = input("Enter the job posting link: ")
website = requests.get(link)
html_content = website.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Search for Job Title and Company Name
job_title = soup.find('h1', {'class': 'app-title'}).text.strip()
company_name = soup.find('span', {'class': 'company-name'}).text.strip()

# Search for Description without Misc Details
description_raw = soup.find('div', {'id': 'content'})

for elem in description_raw.find_all(['div', 'p'], recursive=False):
    if 'COMPENSATION AND BENEFITS' in elem.text:
        elem.decompose()
        
description = description_raw.text.strip()

# Generate a Cover Letter
response = openai.Completion.create(
    engine="",
    prompt=f"Write a cover letter for the following job description:\n{description}\n\n",
)

cover_letter = response.choices[0].text
print(cover_letter)