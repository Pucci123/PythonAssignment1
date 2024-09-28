import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('Assignment 2')

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

# Load and filter the data
df = load_data()
df_filtered = filter_data(df)

st.title('Campaigns in 2016')

# Display the filtered dataset
st.write(df_filtered)

# To view the anomaly in the table where even high pledged still cannot bring the campaign to success
# Filter failed campaigns with high pledges
def detect_anomalies(df):
    # Filter campaigns that failed
    failed_campaigns = df[df['State'] == 'Failed']
    
    # Calculate the mean and standard deviation of the 'Pledged' column
    mean_pledged = failed_campaigns['Pledged'].mean()
    std_pledged = failed_campaigns['Pledged'].std()
    
    # Define an anomaly as a campaign where Pledged is significantly above the mean (e.g., more than 1 standard deviation)
    threshold = mean_pledged + std_pledged
    
    # Filter for anomalies where the Pledged amount is greater than the threshold
    anomalies = failed_campaigns[failed_campaigns['Pledged'] > threshold]
    
    return anomalies

# Load the data
df = load_data()

# Detect anomalies
anomalies = detect_anomalies(df)

# Display anomalies in Streamlit
st.title('Failed Campaigns with High Pledges')
st.write(anomalies)

# To see in pie chart what is the view per category of those anomaly campaigns
# Load the dataset
@st.cache_data()
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

# Generate and display the pie chart in Streamlit
st.title('Anomalies by Category')
fig = plot_pie_chart(anomalies)
st.pyplot(fig)

#ANALYZE

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
    
    return failed_long_duration['Duration_days'].value_counts()

# Analyze backers and failure rates for all data
def backer_failure_rate(df):
    # Filter failed campaigns
    failed_high_backers = df[df['State'] == 'Failed']
    
    # Get failed campaigns with highest backers
    return failed_high_backers['Backers'].value_counts()

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

def plot_failed_29_days_categories_pie(df):
    # Filter campaigns that failed and ran for exactly 29 days
    df['Launched'] = pd.to_datetime(df['Launched'])
    df['Deadline'] = pd.to_datetime(df['Deadline'])
    df['Duration_days'] = (df['Deadline'] - df['Launched']).dt.days
    failed_29_days = df[(df['State'] == 'Failed') & (df['Duration_days'] == 29)]
    
    # Group by Category and count occurrences
    category_counts = failed_29_days['Category'].value_counts()
    
    # Plot a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Categories for Failed Campaigns that Ran for 29 Days')
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    plt.show()

# Load data
df = load_data()

# Plot the pie chart for failed 29-day campaigns by category
plot_failed_29_days_categories_pie(df)









