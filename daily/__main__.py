from jinja2 import Template
import pandas as pd

import daily
chrome = daily.Chrome()
pinterest = daily.Pinterest(['Travel'])
quotes = daily.Quotes('https://www.goodreads.com/author/quotes/2622245.Lao_Tzu', 'Lao Tzu')
reddit = daily.Reddit(['tifu'])
tasks = daily.Tasks()

# Sample dataframes
df1 = chrome.get_bookmarks().head()
df2 = pinterest.get_pins().head()
df3 = quotes.get_quotes().head()

# Load the Jinja2 template
with open('template.html', 'r') as file:
    template = Template(file.read())

# Render the template with dataframes
html_content = template.render(
    dataframe1=df1,
    dataframe2=df2,
    dataframe3=df3
)

# Write to an HTML file
with open('output.html', 'w') as file:
    file.write(html_content)
