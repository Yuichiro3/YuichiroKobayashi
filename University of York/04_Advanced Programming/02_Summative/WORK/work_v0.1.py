#!/usr/bin/env python
# coding: utf-8

# # Overview
# 
# #### ------------------------------------------------------------------------------------------------------------------------
# ## Backend
# ### Step 1: Load and Clean Data
# ### Step 2: Pre-process Data  
# ### Step 3: Design the SQLite Database Table and Store Data into the Database 
# ### Step 4: Load the processed dataset from the SQLite Database and Close the connection
# ### Step 5: Make outputs for statistics analysis
# 
# #### ------------------------------------------------------------------------------------------------------------------------
# ## Frontend
# ### Step 1: Design GUI
# ### Step 2: Implement the backend’s functions into GUI
# 
# #### ------------------------------------------------------------------------------------------------------------------------
# ## Note
# 1) For the non-functional requirements, the prototype requires: 
# - Codes for error handling must be implemented in each function.
# - Codes for providing feedback against the user actions. 
# 
# 2) For the technical requirements, the developer uses:
# - Core Python from version 3.8.2 within Anaconda using the Jupyter notebook.
# - The design where each function is executed step-by-step rather than concurrently.
# 
# #### ------------------------------------------------------------------------------------------------------------------------

# In[1]:


import sys
import platform


# In[2]:


print(sys.version)


# # Backend

# ## Step 1: Load and Clean Data
# ### ・Step 1-1: Load the three CSV files // (LOAD_RAW_DATA)
# ### ・Step 1-2: Add the column which is prime key // (ADD_PK)
# ### ・Step 1-3: Clean the datasets // (REMOVE) and (RENAME)

# In[81]:


import pandas as pd


# In[82]:


# Step 1-1: Define the function which loads the CSV files 

# Function: load_csv(file_path)
# Purpose:
# This function is designed to load a CSV file into a Pandas DataFrame. It accepts the file path 
# as input, reads the file, and returns the DataFrame object. It also includes error handling 
# to ensure that invalid or missing files are handled gracefully.

def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.
    """
    try:
        # Attempt to read the CSV file
        df = pd.read_csv(file_path)
        print(f"File loaded successfully: {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
    except pd.errors.ParserError:
        print(f"Error: Failed to parse the file at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None


# In[83]:


# Test: Define the three files' path
user_path = "Data/USER_LOG.csv"
activity_path = "Data/ACTIVITY_LOG.csv"
component_path = "Data/COMPONENT_CODES.csv"


# In[84]:


# Test: Call the load_csv function
df_user = load_csv(user_path)
df_activity = load_csv(activity_path)
df_component = load_csv(component_path)


# In[85]:


# Step 1-2: Add the column which is prime key

# Function: add_primary_key
# Purpose:
# This function adds a new column 'PK' to the given DataFrame with sequential numbers 
# starting from 1. The column serves as a unique primary key for merging purposes.

def add_primary_key(df):
    try:
        # Add a 'PK' column with sequential integers
        df = df.reset_index(drop=True)  # Ensure proper indexing before adding PK
        df['PK'] = range(1, len(df) + 1)
        print("Primary key column 'PK' added successfully.")
        return df
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return df


# In[86]:


# Test: Call the function (add_primary_key(df))
df_user = add_primary_key(df_user)
print(df_user.head())

print("")
df_activity = add_primary_key(df_activity)
print(df_activity.head())


# In[87]:


# Step 1-3: Cleand the datasets (REMOVE)

# Function: clean_data_remove
# Purpose:
# This function filters out rows where the 'Component' column has values 'System' or 'Folder' 
# in the ACTIVITY_LOG dataset. This ensures that irrelevant rows are removed before analysis.

def clean_data_remove(df):
    try:
        # Filter out rows with unwanted components
        cleaned_df = df[~df['Component'].isin(['System', 'Folder'])]
        print("Unwanted components removed successfully.")
        return cleaned_df
    except KeyError:
        print("Error: 'Component' column not found in the DataFrame.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return df


# In[88]:


# Step 1-3: Cleand the datasets (RENAME)

# Function: rename_columns
# Purpose:
# This function renames the column "User Full Name *Anonymized" to "User_ID" 
# in the given DataFrame.

def rename_columns(df):
    try:
        # Rename the specified column
        renamed_df = df.rename(columns={"User Full Name *Anonymized": "User_ID"})
        print("Columns renamed successfully.")
        return renamed_df
    except KeyError:
        print("Error: 'User Full Name *Anonymized' column not found in the DataFrame.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return df


# In[89]:


# Test: Call the function "clean_data_remove(df)"
df_activity_cleaned = clean_data_remove(df_activity)
df_activity_cleaned


# In[90]:


# Test: Call the function "rename_columns(df)"
df_activity_cleaned = rename_columns(df_activity_cleaned)
print(df_activity_cleaned)

print("")
df_user_cleaned = rename_columns(df_user)
print(df_user_cleaned)


# ## Step 2: Pre-process Data 
# ### ・Step 2-1: Merge datasets // (MERGE)
# ### ・Step 2-2: Reshape data // (RESHAPE) 
# ### ・Step 2-3: Add calculated fields // (COUNT)

# In[91]:


# Step 2-1: Merge datasets

# Function: merge_datasets
# Purpose:
# This function performs two merge operations:
# Step 2-1-1. Merges the cleaned ACTIVITY_LOG DataFrame with the COMPONENT_CODES DataFrame 
#    using 'Component' as the key.
# Step 2-1-2. Merges the resulting DataFrame with the USER_LOG DataFrame using 'PK'(primary key) as the key.

def merge_datasets(df_activity_cleaned, df_component, df_user_cleaned):
    try:
        # Step 2-1-1: Merge ACTIVITY_LOG with COMPONENT_CODES using 'Component' as the key
        merged_df_activity_component = pd.merge(
            df_activity_cleaned,
            df_component,
            on='Component',
            how='left'
        )
        print("Step 2-1-1: Merged ACTIVITY_LOG with COMPONENT_CODES successfully.")

        # Step 2-1-2: Merge the result with USER_LOG using 'PK' as the key
        # Use suffixes to control duplicate column names
        merged_df = pd.merge(
            merged_df_activity_component,
            df_user_cleaned,
            on='PK',
            how='left',
            suffixes=('', '_drop')  # No suffix for the first, '_drop' for the second
        )
        print("Step 2-1-2: Merged with USER_LOG successfully.")

        # Drop the unnecessary 'User_ID_drop' column created during the merge
        merged_df = merged_df.drop(columns=['User_ID_drop'])
        print("Dropped unnecessary duplicate column 'User_ID_drop'.")

        return merged_df

    except KeyError as e:
        print(f"KeyError: {str(e)} - Check if the keys exist in the DataFrames.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None


# In[92]:


# Test: Call the function (merge_datasets)
merged_df = merge_datasets(df_activity_cleaned, df_component, df_user_cleaned)
merged_df


# In[93]:


merged_df.info()


# In[94]:


# Step 2-2: Reshape data
# Step 2-2-1: Use datetime for "Date"

# Function: convert_to_datetime
# Purpose: Convert the 'Date' column from object to datetime format.

def convert_to_datetime(df):
    try:
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
        print("Date column successfully converted to datetime format.")
        return df
    except Exception as e:
        print(f"An error occurred while converting Date column: {str(e)}")
        return df


# In[95]:


# Step 2-2-2: Extract Month from "Date"



def extract_month(df):
    try:
        # Extract month name from 'Date' and store it in a new column
        df['Month'] = df['Date'].dt.strftime('%B')  # E.g., "October"
        print("Month column successfully created.")
        return df
    except Exception as e:
        print(f"An error occurred while extracting the Month column: {str(e)}")
        return df


# In[96]:


# Test: convert_to_datetime (Step 2-2-1)
merged_df = convert_to_datetime(merged_df)


# In[97]:


# Test: extract_month (Step 2-2-2)
merged_df = extract_month(merged_df)


# In[98]:


# Test: how dataframe looks like
merged_df


# In[99]:


# Check the earliest and latest dates in the 'Date' column
start_date = merged_df['Date'].min()  # Get the earliest date
end_date = merged_df['Date'].max()    # Get the latest date

print(f"The dataset starts on: {start_date}")
print(f"The dataset ends on: {end_date}")
print(end_date - start_date) # 13-week is 91 days


# In[103]:


# Step 2-2-3: Reshape data

# Function: reshape_data
# Purpose: Reshape the dataset using pivot_table to handle duplicates (purely restructuring the data).

def reshape_data(df, group_by):
    try:
        reshaped_df = df.pivot_table(
            index=group_by,        # Group by specified keys
            columns='Component',  # Create columns for Components
            values='PK',          # Use PK as a proxy for counting interactions
            aggfunc='count',      # Use count to handle duplicates
            fill_value=0          # Fill missing values with 0
        ).reset_index()
        print("Reshaped data successfully.")
        return reshaped_df
    except Exception as e:
        print(f"Error while reshaping data: {str(e)}")
        return None


# In[104]:


# Step 2-3: Add calculated fields
# Function: count_interactions
# Purpose: Perform Count aggregation on the reshaped dataset.

def count_interactions(reshaped_df, group_by):
    try:
        counted_df = reshaped_df.groupby(group_by).sum().reset_index()
        print("Counted interactions successfully.")
        return counted_df
    except Exception as e:
        print(f"Error while counting interactions: {str(e)}")
        return None


# In[105]:


# First chunk to use statistics for each month
# Test: Make the first chunk dataset for statistics (each month)

# Reshape the dataset for User_ID and Month without counting
reshaped_df1 = reshape_data(merged_df, ['User_ID', 'Month'])

# Perform Count on the reshaped data
df1_counted = count_interactions(reshaped_df1, ['User_ID', 'Month'])


# In[106]:


# Test: See how the df_1 looks like
df1_counted


# In[107]:


# Second chunk to use statistics for 13-week academic semester
# Test: Make the second chunk dataset for statistics (13-week academic semester)

# Reshape the dataset for User_ID without counting
reshaped_df2 = reshape_data(merged_df, ['User_ID'])

# Perform Count on the reshaped data
df2_counted = count_interactions(reshaped_df2, ['User_ID'])


# In[109]:


# Test: See how the df_2 looks like
df2_counted


# In[110]:


# Third chunk to count the number of interactions of each components
# Directly group and aggregate without reshaping
df3_total = merged_df.groupby('Component').size().reset_index(name='Total')
df3_total


# In[112]:


# Fourth chunk to conduct correlational analysis
# Reuse df2_counted for correlation analysis
df4 = df2_counted.copy()
df4


# ## Step 3: Design the SQLite Database Table and Store Data into the Database
# ### ・Step 3-1: Create SQLite Database
# ### ・Step 3-2: Save Data in the SQLite Database // (STORE)

# In[113]:


import sqlite3


# In[114]:


# Step 3-1: Create SQLite Database tables

# Function: create_tables
# Purpose: Create the SQLite tables for df1, df2, and df3.
def create_tables(conn):
    try:
        cursor = conn.cursor()
        # Create df1_statistics_monthly table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS df1_statistics_monthly (
                User_ID INTEGER,
                Month TEXT,
                Quiz INTEGER,
                Lecture INTEGER,
                Assignment INTEGER,
                Attendance INTEGER,
                Survey INTEGER
            )
        ''')
        
        # Create df2_statistics_semester table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS df2_statistics_semester (
                User_ID INTEGER,
                Quiz INTEGER,
                Lecture INTEGER,
                Assignment INTEGER,
                Attendance INTEGER,
                Survey INTEGER
            )
        ''')
        
        # Create df3_component_totals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS df3_component_totals (
                Component TEXT,
                Total INTEGER
            )
        ''')
        
        conn.commit()
        print("Step 3-1: Tables created successfully.")
    except Exception as e:
        print(f"Error while creating tables: {str(e)}")


# In[115]:


# Step 3-2: Save Data in the SQLite Database // (STORE)

# Function: store_data
# Purpose: Store the processed DataFrames into the corresponding SQLite tables.
def store_data(df, table_name, conn):
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Step 3-2: Data stored in table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error while storing data to table '{table_name}': {str(e)}")


# In[117]:


# Test: Establish connection to SQLite database
connection = sqlite3.connect("processed_data.db")


# In[118]:


# Test: Create tables (Step 3-1)
create_tables(connection)


# In[119]:


# Test: Store Processed Data (Step 3-2)
store_data(df1_counted, "df1_statistics_monthly", connection)
store_data(df2_counted, "df2_statistics_semester", connection)
store_data(df3_total, "df3_component_totals", connection)


# ## Step 4: Load the processed dataset from the SQLite Database and Close the connection
# ### ・Step 4-1: Load the processed data from the SQLite database // (LOAD_PROCESSED_DATA)
# ### ・Step 4-2: Close the connection from the Database

# In[116]:


# Step 4-1: Load the processed data from the SQLite database // (LOAD_PROCESSED_DATA)

# Function: load_data
# Purpose: Load data from the SQLite tables back into DataFrames.
def load_data(table_name, conn):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        print(f"Step 4: Data loaded from table '{table_name}' successfully.")
        return df
    except Exception as e:
        print(f"Error while loading data from table '{table_name}': {str(e)}")
        return None


# In[121]:


# Step 4-2: Close the connection

# Function: close_connection
# Purpose: Close the SQLite connection.
def close_connection(conn):
    try:
        conn.close()
        print("Database connection closed successfully.")
    except Exception as e:
        print(f"Error while closing connection: {str(e)}")


# In[120]:


# Test: Load data from the tables (Step 4-1)
loaded_df1 = load_data("df1_statistics_monthly", connection)
loaded_df2 = load_data("df2_statistics_semester", connection)
loaded_df3 = load_data("df3_component_totals", connection)


# In[122]:


close_connection(connection)


# ## Step 5: Make outputs for statistics analysis
# ### ・Step 5-1: Conduct statistical analysis // (OUTPUT_STATISTICS) 
# ### ・Step 5-2: Make Graphs // (STATISTICS_VISUALISATION)
# ### ・Step 5-3: Conduct correlation analysis // (OUTPUT_CORRELATION)
# ### ・Step 5-4: Make Graphs // (CORRELATION_VISUALISATION)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Frontend

# ## Step 1: Design GUI
# ### ・Step 1-1: Design Processing section
# ### ・Step 1-2: Design Analysis section
# ### ・Step 1-3: Design Output Display section

# In[ ]:





# ## Step 2: Implement the backend’s functions into the GUI
# ### ・Step 2-1: Definethe  Button name
# ### ・Step 2-2: Implement the backend’s functions into each button

# In[ ]:





# # EOF
