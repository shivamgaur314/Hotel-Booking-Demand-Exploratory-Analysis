#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Importing Packages:-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick


# In[10]:


#Importing Data:-
data= pd.read_csv(r"C:\Users\Shivangi\Desktop\data\hotel_bookings.csv")


# In[4]:


data.head()


# # Data Processing

# In[26]:


data1=data.copy()


# In[71]:


data1=data1.drop(['agent','company'],axis=1)


# In[72]:


# for missing children value, replace it with rounded mean value
data1['children'].fillna(round(data.children.mean()), inplace=True)


# In[73]:


data1[data1.adults+data1.babies+data1.children==0].shape


# In[74]:


## Drop Rows where there is no adult, baby and child
data1 = data1.drop(data1[(data1.adults+data1.babies+data1.children)==0].index)


# In[75]:


data1.dtypes


# In[76]:


## convert datatype of these columns from float to integer
data1[['children']] = data1[['children']].astype('int64')


# # EXPLORATORY DATA ANALYSIS

# 1. How many bookings were cancelled?

# In[77]:



def get_count(series, limit=None):
    
    if limit != None:
        series = series.value_counts()[:limit]
    else:
        series = series.value_counts()
    
    x = series.index
    y = series/series.sum()*100
    
    return x.values,y.values

x,y = get_count(data1['is_canceled'])
x,y


# In[78]:


def plot(x, y, x_label=None,y_label=None, title=None, figsize=(7,5), type='bar'):
    
    sns.set_style('darkgrid')
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    if x_label != None:
        ax.set_xlabel(x_label)
    
    if y_label != None:
        ax.set_ylabel(y_label)
        
    if title != None:
        ax.set_title(title)
    
    if type == 'bar':
        sns.barplot(x,y, ax = ax)
    elif type == 'line':
        sns.lineplot(x,y, ax = ax, sort=False)
        
    
    plt.show()
    
plot(x,y, x_label='Booking Cancelled (No = 0, Yes = 1)', y_label='Booking (%)')


# In[79]:


data1_not_canceled = data1[data1['is_canceled'] == 0]


# 2. What is the booking ratiion between Resort hotels and City hotels?

# In[80]:


x,y = get_count(data1_not_canceled['hotel'])
plot(x,y, x_label='Hotels', y_label='Total Booking (%)', title='Hotel comparison')


# 3. What is the percentage of booking in each year?

# In[81]:


x,y = get_count(data1_not_canceled['arrival_date_year'])
plot(x,y, x_label='Year', y_label='Total Booking (%)', title='Year comparison')


# In[82]:


plt.subplots(figsize=(7,5))
sns.countplot(x='arrival_date_year', hue='hotel',  data=data1_not_canceled);


# 4. Which is the busiest month of the hotel?

# In[83]:


## Order of months
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 
             'November', 'December']


## Select only City Hotel
sorted_months = data1_not_canceled.loc[data1.hotel=='City Hotel' ,'arrival_date_month'].value_counts().reindex(new_order)

x1 = sorted_months.index
y1 = sorted_months/sorted_months.sum()*100



## Select only Resort Hotel
sorted_months = data1_not_canceled.loc[data1.hotel=='Resort Hotel' ,'arrival_date_month'].value_counts().reindex(new_order)

x2 = sorted_months.index
y2 = sorted_months/sorted_months.sum()*100


fig, ax = plt.subplots(figsize=(18,6))

ax.set_xlabel('Months')
ax.set_ylabel('Booking (%)')
ax.set_title('Booking Trend (Monthly)')


sns.lineplot(x1, y1.values, label='City Hotel', sort=False)
sns.lineplot(x1, y2.values, label='Resort Hotel', sort=False)

plt.show()


# 5. Which was the most booked accommodation type (Single, Couple, Family)?

# In[84]:


# single   = data1_not_canceled[(data1_not_canceled.adults==1) & (data1_not_canceled.children==0) & (data1_not_canceled.babies==0)]
couple   = data1_not_canceled[(data1_not_canceled.adults==2) & (data1_not_canceled.children==0) & (data1_not_canceled.babies==0)]
family   = data1_not_canceled[data1_not_canceled.adults + data1_not_canceled.children + data1_not_canceled.babies > 2]



names = ['Single', 'Couple (No Children)', 'Family / Friends']
count = [single.shape[0],couple.shape[0], family.shape[0]]
count_percent = [x/data1_not_canceled.shape[0]*100 for x in count]


plot(names,count_percent,  y_label='Booking (%)', title='Accommodation Type', figsize=(10,7))


# In[ ]:




