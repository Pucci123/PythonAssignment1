import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('Assignment 1')

# Load the dataset
@st.cache_data()
def load_data():
    df = pd.read_csv("kickstarter.csv")
    return df

# 1. To filter only campaigns run in 2016
# Filter & display dataset in web
def filter_data(df):
    # Convert the 'Launched' column to datetime format and extract the year
    df['Launched'] = pd.to_datetime(df['Launched'])
    df['launch_year'] = df['Launched'].dt.year
    
    # Filter the dataset to only include rows where the year is 2016
    df_2016 = df[df['launch_year'] == 2016]
    
    return df_2016

# To give a view on the relation between amount pledged in each category
# Load and filter the data
df = load_data()
df_filtered = filter_data(df)

st.title('Campaigns in 2016')

# Display the filtered dataset
st.write(df_filtered)

# To view the amount pledged per Category
# Load the dataset
df = pd.read_csv('kickstarter_2016.csv')

# Group by 'Category' and sum the 'Pledged' amounts
pledged_by_category = df.groupby('Category')['Pledged'].sum() / 100  # Divide by 100 to display per $100

# Streamlit title
st.title("Pledged Amount by Category in Kickstarter 2016 (per $100)")

# Plotting the bar chart for pledged amounts by category using Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
pledged_by_category.plot(kind='bar', color='skyblue', ax=ax)

# Set the title and labels
ax.set_title('Pledged Amount by Category (per $100)')
ax.set_ylabel('Pledged Amount (in $100)')
ax.set_xlabel('Category')

# Rotate x-axis labels for better readability
ax.set_xticklabels(pledged_by_category.index, rotation=45, ha='right')

# Streamlit display
st.pyplot(fig)

# 2. To see  per category which campaign that despite had high amount of pledge, yet they did not success. 
# Load the dataset and cache it for performance
@st.cache_data
def load_data():
    df = pd.read_csv("kickstarter_2016.csv")
    return df

# Create a pie chart to show the percentage of anomalies in each category
def plot_pie_chart(anomalies):
    # Group the anomalies by category and count occurrences
    category_counts = anomalies['Category'].value_counts()

    # Generate a list of distinct colors
    num_categories = len(category_counts)
    colors = plt.cm.tab10(np.linspace(0, 1, num_categories))  # Using tab10 colormap for distinct colors

    # Create a pie chart with unique colors
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        category_counts, labels=None, autopct='%1.1f%%', startangle=90,
        pctdistance=0.85, wedgeprops={'linewidth': 1, 'edgecolor': 'black'},
        colors=colors  # Set the unique colors here
    )
    
    # Add a legend for category names
    ax.legend(wedges, category_counts.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Equal aspect ratio ensures the pie chart is drawn as a circle
    ax.axis('equal')
    
    # Adjust the appearance of the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    return fig

# Load data
df = load_data()

# Assuming anomalies are failed campaigns (you can adjust this filter as needed)
anomalies = df[df['State'] == 'Failed']

# Generate and display the pie chart in Streamlit
st.title('Anomalies by Category')

# Call the function to generate the chart and display it
fig = plot_pie_chart(anomalies)
st.pyplot(fig)


# 3. ANALYZE with exploration of ChatGPT on further anomaly in the data, based on Category, Duration of Campaign & Number of Backers

# Load the dataset
@st.cache_data()
def load_data():
    df = pd.read_csv("kickstarter_2016.csv")
    return df

# Analyze categories with failure rates for all data
def category_failure_rate(df):
    # Count total and failed campaigns by category
    category_counts = df['Category'].value_counts()
    failed_counts = df[df['State'] == 'Failed']['Category'].value_counts()
    
    # Calculate failure rates
    failure_rates = (failed_counts / category_counts).fillna(0)  # Avoid division by zero
    return failure_rates.sort_values(ascending=False)

# Analyze duration and failure rates in days for all data
def duration_failure_rate(df):
    # Calculate campaign duration in days
    df['Launched'] = pd.to_datetime(df['Launched'])
    df['Deadline'] = pd.to_datetime(df['Deadline'])
    df['Duration_days'] = (df['Deadline'] - df['Launched']).dt.days
    
    # Filter for failed campaigns
    failed_long_duration = df[df['State'] == 'Failed']
    
    # Return the top 20 durations with the highest failure counts
    return failed_long_duration['Duration_days'].value_counts().head(20)

# Analyze backers and failure rates for all data
def backer_failure_rate(df):
    # Filter failed campaigns
    failed_high_backers = df[df['State'] == 'Failed']
    
    # Get failed campaigns with highest backers, returning only the top 20
    return failed_high_backers['Backers'].value_counts().head(20)

# Function to plot pie charts with legends and indicators
def plot_pie_chart(data, title):
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab10.colors)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    
    # Adding legend next to the pie chart
    plt.legend(wedges, data.index, title="Categories", loc="upper right", bbox_to_anchor=(1.2, 1))
    
    # Annotating the pie chart with data values
    for i, a in enumerate(autotexts):
        a.set_text(f'{data.index[i]}: {a.get_text()}')  # Show both category and percentage
    
    st.pyplot(plt)

# Load the data
df = load_data()

# Analyzing Category Failure Rates
failure_rates_by_category = category_failure_rate(df)
plot_pie_chart(failure_rates_by_category, 'Failure Rates by Category')

# Analyzing Duration Failure Rates
failure_rates_by_duration = duration_failure_rate(df)
plot_pie_chart(failure_rates_by_duration, 'Failure Rates by Campaign Duration (in Days)')

# Analyzing Backer Failure Rates
failed_high_backers = backer_failure_rate(df)
plot_pie_chart(failed_high_backers, 'Failure Rates by Number of Backers')


# ANALYZE Deeper on the Duration of Failure Rate

# Load the dataset
df = pd.read_csv('kickstarter_2016.csv')

# Convert the Launched and Deadline columns to datetime
df['Launched'] = pd.to_datetime(df['Launched'])
df['Deadline'] = pd.to_datetime(df['Deadline'])

# Calculate campaign duration in days
df['Duration_days'] = (df['Deadline'] - df['Launched']).dt.days

# Filter campaigns that failed and ran for exactly 29 days
failed_29_days = df[(df['State'] == 'Failed') & (df['Duration_days'] == 29)]

# Streamlit title
st.title("Analysis of Failed Kickstarter Campaigns that Ran for 29 Days")

# Section 1: Pie Chart of Categories for 29-day Failed Campaigns
st.subheader("Category Distribution of Failed 29-day Campaigns")

# Get the category distribution for the failed 29-day campaigns
category_counts = failed_29_days['Category'].value_counts()

# Plotting the pie chart for categories using Matplotlib
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)  # Use Streamlit to display the pie chart

# Section 2: Bar Chart of Pledge Amounts for 29-day Failed Campaigns
st.subheader("Total Pledged Amount by Category for Failed 29-day Campaigns")

# Get the total pledged amount by category for the failed 29-day campaigns
pledged_by_category = failed_29_days.groupby('Category')['Pledged'].sum()

# Plotting the bar chart for pledge amounts by category using Matplotlib
fig2, ax2 = plt.subplots(figsize=(10, 6))
pledged_by_category.plot(kind='bar', color='skyblue', ax=ax2)
ax2.set_title('Total Pledged Amount by Category')
ax2.set_ylabel('Pledged Amount ($)')
ax2.set_xlabel('Category')
ax2.set_xticklabels(pledged_by_category.index, rotation=45)
st.pyplot(fig2)  # Use Streamlit to display the bar chart

#4a. To explore the Top 3 Category of Successful Campaigns
# Filter for successful campaigns
successful_campaigns = df[df['State'] == 'Successful']

# Group by category and count the number of successful campaigns in each category
top_categories = successful_campaigns['Category'].value_counts().head(3)

# Plotting the pie chart
fig, ax = plt.subplots()
ax.pie(top_categories, labels=top_categories.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display in Streamlit
st.title('Top 3 Categories of Successful Kickstarter Campaigns')
st.pyplot(fig)

# To provide details of the sub-segment of the top 3 category
# Filter for successful campaigns
successful_campaigns = df[df['State'] == 'Successful']

# Get top 3 categories
top_categories = successful_campaigns['Category'].value_counts().head(3)

# Filter data to include only the top 3 categories
filtered_data = successful_campaigns[successful_campaigns['Category'].isin(top_categories.index)]

# Create subcategory counts for each of the top categories
fig, axes = plt.subplots(1, 3, figsize=(20, 8))

colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

for i, category in enumerate(top_categories.index):
    # Filter and get the top 10 subcategories for the current category
    subcategory_data = filtered_data[filtered_data['Category'] == category]['Subcategory'].value_counts().head(10)
    
    # Explode all subcategories slightly for emphasis
    explode = [0.05] * len(subcategory_data)
    
    # Plot pie chart for top 10 subcategories of each top category
    axes[i].pie(subcategory_data, labels=subcategory_data.index, autopct='%1.1f%%',
                explode=explode, startangle=90, colors=colors[:len(subcategory_data)])
    axes[i].set_title(f'{category} - Top 10 Subcategories')

# Ensure the pie charts are equally sized
for ax in axes:
    ax.axis('equal')

# Display the visualization in Streamlit
st.title('Top 3 Categories with Exploded Top 10 Subcategories for Successful Kickstarter Campaigns')
st.pyplot(fig)

#4b. To explore the Top 3 Category of Unsuccessful Campaigns
# Filter for unsuccessful campaigns (those that are 'Failed')
failed_campaigns = df[df['State'] == 'Failed']

# Get top 3 categories with the most failed campaigns
top_failed_categories = failed_campaigns['Category'].value_counts().head(3)

# Plotting the pie chart
fig, ax = plt.subplots()
colors = ['#ff9999', '#66b3ff', '#99ff99']  # Customize colors as needed

ax.pie(top_failed_categories, labels=top_failed_categories.index, autopct='%1.1f%%',
       startangle=90, colors=colors)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Top 3 Categories of Failed Kickstarter Campaigns')

# Display the pie chart in Streamlit
st.title('Top 3 Categories of Failed Kickstarter Campaigns')
st.pyplot(fig)

# To provide details of the sub-segment of the top 3 category
# Filter for unsuccessful campaigns (those that are 'Failed')
failed_campaigns = df[df['State'] == 'Failed']

# Get top 3 categories with the most failed campaigns
top_failed_categories = failed_campaigns['Category'].value_counts().head(3)

# Filter data to include only the top 3 failed categories
filtered_failed_data = failed_campaigns[failed_campaigns['Category'].isin(top_failed_categories.index)]

# Create subcategory counts for each of the top categories
fig, axes = plt.subplots(1, 3, figsize=(20, 8))

colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

for i, category in enumerate(top_failed_categories.index):
    # Get the top 10 subcategories for the current failed category
    subcategory_data = filtered_failed_data[filtered_failed_data['Category'] == category]['Subcategory'].value_counts().head(10)
    
    # Explode all subcategories slightly for emphasis
    explode = [0.05] * len(subcategory_data)
    
    # Plot pie chart for top 10 subcategories of each failed category
    axes[i].pie(subcategory_data, labels=subcategory_data.index, autopct='%1.1f%%',
                explode=explode, startangle=90, colors=colors[:len(subcategory_data)])
    axes[i].set_title(f'{category} - Top 10 Failed Subcategories')

# Ensure the pie charts are equally sized
for ax in axes:
    ax.axis('equal')

# Display the visualization in Streamlit
st.title('Top 3 Failed Categories with Exploded Top 10 Subcategories')
st.pyplot(fig)


#5. To show the distribution of funding goal
# Load the dataset and cache it for performance
@st.cache_data
def load_data():
    st.write("Loading data...")
    df = pd.read_csv("kickstarter_2016.csv")  # Ensure this path is correct
    st.write("Data loaded successfully.")
    return df

# Load the dataset
df = load_data()

# Display the first few rows of the dataset
st.write("### Dataset Preview:")
st.write(df.head())

# Check if the 'Goal' column exists and filter out campaigns with missing or invalid goals
if 'Goal' in df.columns:
    # Filter out missing values and goals <= 0 (since log10 is undefined for those)
    df = df[df['Goal'].notna() & (df['Goal'] > 0)]

    # Apply log transformation to the funding goals (log base 10)
    df['Log_Goal'] = np.log10(df['Goal'])

    # Plotting the distribution of the log-transformed funding goals
    plt.figure(figsize=(10, 6))
    plt.hist(df['Log_Goal'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Log-Transformed Funding Goals')
    plt.xlabel('Log10 of Funding Goal Amount')
    plt.ylabel('Number of Campaigns')
    plt.grid(axis='y', alpha=0.75)

    # Display the plot in Streamlit
    st.title('Distribution of Funding Goals (Log-Transformed)')
    st.pyplot(plt)

    # Clear the current figure to prevent overlap in future plots
    plt.clf()

    # Describe the distribution
    st.write("### Distribution Description:")
    st.write("The distribution of log-transformed funding goals shows a skew towards lower values, indicating that most campaigns have relatively modest funding goals. This transformation helps to minimize the impact of a small number of campaigns with very high funding goals, allowing for a clearer view of the majority of campaigns.")
else:
    st.error("The 'Goal' column is missing from the dataset.")

#To see the category of top 10 highest funding
# Load the dataset and cache it for performance
@st.cache_data
def load_data():
    df = pd.read_csv("kickstarter_2016.csv")  # Ensure this path is correct
    return df

# Load the dataset
df = load_data()

# Check if the 'Goal', 'Category', and 'Country' columns exist
if 'Goal' in df.columns and 'Category' in df.columns and 'Country' in df.columns:
    # Filter out campaigns with missing or invalid goals
    df = df[df['Goal'].notna() & (df['Goal'] > 0)]
    
    # Sort the data by the 'Goal' column in descending order to get the top 10 campaigns with the highest funding goals
    top_10_campaigns = df.nlargest(10, 'Goal')
    
    # Extract the 'Category' and 'Country' columns for the top 10 campaigns
    top_10_categories = top_10_campaigns['Category']
    top_10_countries = top_10_campaigns['Country']
    
    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    top_10_campaigns.groupby(['Category', 'Country']).size().unstack().plot(kind='bar', stacked=True, ax=ax)
    
    # Adding labels and title
    plt.title('Top 10 Categories of Highest Funding Campaigns by Country')
    plt.xlabel('Category')
    plt.ylabel('Number of Campaigns')
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Display the bar chart in Streamlit
    st.title('Top 10 Categories and Countries of Highest Funding Campaigns')
    st.pyplot(fig)

    # Display the data of the top 10 campaigns
    st.write("### Top 10 Highest Funding Campaigns:")
    st.write(top_10_campaigns[['Category', 'Country', 'Goal']])
else:
    st.error("The 'Goal', 'Category', or 'Country' column is missing from the dataset.")










