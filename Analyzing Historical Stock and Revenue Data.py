#!/usr/bin/env python
# coding: utf-8

# <h1>Analyzing Historical Stock/Revenue Data and Building a Dashboard</h1>

# You will be graded on the dashboards displaying the specified data and the screenshots you took during the final project lab questions. There are 12 possible points for this assignment. Here is the breakdown:
# 
# Question 1 - Extracting Tesla Stock Data Using yfinance - 2 Points
# 
# Question 2 - Extracting Tesla Revenue Data Using Webscraping - 1 Points
# 
# Question 3 - Extracting GameStop Stock Data Using yfinance - 2 Points
# 
# Question 4 - Extracting GameStop Revenue Data Using Webscraping - 1 Points
# 
# Question 5 - Tesla Stock and Revenue Dashboard - 2 Points
# 
# Question 6 - GameStop Stock and Revenue Dashboard- 2 Points
# 
# Question 7 - Sharing your Assignment Notebook - 2 Points

# In[1]:


get_ipython().system('python -m pip install yfinance')
get_ipython().system('pip install pandas==1.3.5')
get_ipython().system('python -m pip install requests')
get_ipython().system('python -m pip install bs4')
get_ipython().system('python -m pip install plotly')


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# <h1>Question 1: Use yfinance to Extract Stock Data</h1>
# 

# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.

# In[3]:


tesla = yf.Ticker('TSLA')


# Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to max so we get information for the maximum amount of time.

# In[4]:


tesla_data = tesla.history(period="max")


# In[5]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# <h1>Question 2: Use Webscraping to Extract Tesla Revenue Data</h1>
# 
# Use the requests library to download the webpage https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue. Save the text of the response as a variable named html_data.

# In[6]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text


# In[7]:


soup = BeautifulSoup(html_data,  "html.parser")
print(soup.prettify())


# In[8]:


tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[9]:


#Drop any null row that contains null values
tesla_revenue.dropna(axis=0, how='all', subset=['Revenue']) #drop NaN values
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""] #drop empty string values


# Display the last five rows of the tesla_revenue dataframe using the tail function. Upload a screenshot of the results.

# In[10]:


tesla_revenue.tail(5)


# <h1>Question 3: Use yfinance to Extract Stock Data</h1>

# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.

# In[11]:


gme = yf.Ticker('GME')


# Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to max so we get information for the maximum amount of time.

# In[12]:


gme_data = gme.history(period = "max")


# Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.

# In[13]:


gme_data.reset_index(inplace=True)
gme_data.head(5)


# <h1>Question 4: Use Webscraping to Extract GME Revenue Data</h1>

# In[14]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text


# In[15]:


soup = BeautifulSoup(html_data,  "html.parser")
print(soup.prettify())


# Using beautiful soup extract the table with GameStop Quarterly Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column using a method similar to what you did in Question 2.

# In[16]:


gme_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# Display the last five rows of the gme_revenue dataframe using the tail function. Upload a screenshot of the results.

# In[17]:


gme_revenue.tail(5)


# <h1>Question 5: Plot Tesla Stock Graph</h1>

# In[18]:


get_ipython().system('pip install jupyter')


# In[19]:


get_ipython().system('pip install nbformat')
get_ipython().system('pip install ipykernel')
get_ipython().system('pip install --upgrade nbformat')


# <h3>Define the make_graph function</h3>

# In[20]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph.

# In[21]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# <h1>Question 6: Plot GameStop Stock Graph</h1>
# 
# Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph.

# make_graph(gme_data, gme_revenue, 'GameStop')

# In[ ]:




