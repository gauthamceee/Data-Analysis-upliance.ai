#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import the libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Load the datasets
user_details = pd.read_excel('Data Analyst Intern Assignment - Excel.xlsx', sheet_name='UserDetails.csv')
cooking_sessions = pd.read_excel('Data Analyst Intern Assignment - Excel.xlsx', sheet_name='CookingSessions.csv')
order_details = pd.read_excel('Data Analyst Intern Assignment - Excel.xlsx', sheet_name='OrderDetails.csv')


# In[13]:


# Standardize column names (strip spaces and fix capitalization if necessary)
user_details.columns = user_details.columns.str.strip()
cooking_sessions.columns = cooking_sessions.columns.str.strip()
order_details.columns = order_details.columns.str.strip()


# In[14]:


# Handle missing values in the Rating column of OrderDetails
order_details['Rating'].fillna(order_details['Rating'].mean(), inplace=True)


# In[15]:


# Merge the datasets
merged_data_1 = pd.merge(cooking_sessions, user_details, on="User ID", how="outer")
merged_data = pd.merge(merged_data_1, order_details, on="Session ID", how="outer")


# In[16]:


merged_data.head(10)


# In[18]:


# Identify and remove duplicate columns (with "_x" and "_y" suffixes)
columns_to_keep = []
columns_to_remove = []

for column in merged_data.columns:
    if "_x" in column or "_y" in column:
        base_column = column.replace("_x", "").replace("_y", "")
        if base_column not in columns_to_keep:
            columns_to_keep.append(base_column)
        else:
            columns_to_remove.append(column)
    else:
        columns_to_keep.append(column)

# Drop the duplicate columns
final_data = merged_data.drop(columns=columns_to_remove)

# Rename columns to remove suffixes
final_data.columns = [col.replace("_x", "").replace("_y", "") for col in final_data.columns]

# Display the cleaned dataset
print(final_data.head())

# Save cleaned data to an Excel file if needed
final_data.to_excel("Cleaned_Data.xlsx", index=False)


# In[19]:


final_data.head(10)


# In[22]:


# Analyze popular dishes
popular_dishes = final_data['Dish Name'].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=popular_dishes.index, y=popular_dishes.values, palette='viridis')
plt.title('Top 10 Popular Dishes')
plt.xlabel('Dish Name')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.show()


# In[23]:


# Analyze demographic factors influencing user behavior
age_group_behavior = final_data.groupby(pd.cut(merged_data['Age'], bins=[0, 18, 25, 35, 50, 100])).size()
plt.figure(figsize=(8, 5))
age_group_behavior.plot(kind='bar', color='skyblue')
plt.title('User Behavior by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Users')
plt.show()


# In[24]:


# Analyze relationship between cooking sessions and orders
session_order_relation = final_data.groupby('User ID').agg({
    'Session Rating': 'mean',
    'Rating': 'mean'
}).dropna()
plt.figure(figsize=(8, 5))
sns.scatterplot(data=session_order_relation, x='Session Rating', y='Rating', color='green')
plt.title('Relationship Between Cooking Session Ratings and Order Ratings')
plt.xlabel('Session Rating')
plt.ylabel('Order Rating')
plt.show()


# In[25]:


# Create a summary report
summary = {
    "Total Users": len(user_details),
    "Total Cooking Sessions": len(cooking_sessions),
    "Total Orders": len(order_details),
    "Average Session Rating": cooking_sessions['Session Rating'].mean(),
    "Average Order Rating": order_details['Rating'].mean(),
    "Top Dish": popular_dishes.idxmax(),
}
print("Summary Report:")
for key, value in summary.items():
    print(f"{key}: {value}")


# In[26]:


# Business Recommendations:
print("\nBusiness Recommendations:")
print("1. Promote the top dish more prominently in marketing campaigns.")
print("2. Target age groups that show high activity for personalized promotions.")
print("3. Improve cooking session quality as it positively impacts order ratings.")


# In[ ]:




