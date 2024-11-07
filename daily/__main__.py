# from jinja2 import Template
# import pandas as pd

# import daily
# chrome = daily.Chrome()
# pinterest = daily.Pinterest(['Travel'])
# quotes = daily.Quotes('https://www.goodreads.com/author/quotes/2622245.Lao_Tzu', 'Lao Tzu')
# reddit = daily.Reddit(['tifu'])
# tasks = daily.Tasks()

# # Sample dataframes
# df1 = chrome.get_bookmarks().head()
# df2 = pinterest.get_pins().head()
# df3 = quotes.get_quotes().head()

# # Load the Jinja2 template
# with open('template.html', 'r') as file:
#     template = Template(file.read())

# # Render the template with dataframes
# html_content = template.render(
#     dataframe1=df1,
#     dataframe2=df2,
#     dataframe3=df3
# )

# # Write to an HTML file
# with open('output.html', 'w') as file:
#     file.write(html_content)

# import pandas as pd
# import random
# from jinja2 import Environment, FileSystemLoader

# import daily
# chrome = daily.Chrome()

# # Sample dataframe
# df = chrome.get_bookmarks()

# # Select 5 random rows
# sample_df = df.sample(n=5)

# # Convert to dictionary for Jinja
# data = sample_df.to_dict(orient='records')

# # Jinja template setup (assuming your HTML file is located in the 'templates' folder)
# env = Environment(loader=FileSystemLoader('templates'))
# template = env.get_template('template.html')

# # Render the template with the selected data
# html_output = template.render(items=data)

# # Write the output to an HTML file
# with open('output.html', 'w') as f:
#     f.write(html_output)

import pandas as pd
import random
from jinja2 import Environment, FileSystemLoader
import daily
chrome = daily.Chrome()
instagram = daily.Instagram()


# Sample dataframe for the first table
df1 = chrome.get_bookmarks()

# Sample dataframe for the second table
df2 = instagram.get_posts()

# Select 5 random rows from both dataframes
sample_df1 = df1.sample(n=5)
sample_df2 = df2.sample(n=2)

# Convert to dictionary for Jinja
data1 = sample_df1.to_dict(orient='records')
data2 = sample_df2.to_dict(orient='records')

# Jinja template setup (assuming your HTML file is located in the 'templates' folder)
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

# Render the template with the selected data
html_output = template.render(items1=data1, items2=data2)

# Write the output to an HTML file
with open('output.html', 'w') as f:
    f.write(html_output)