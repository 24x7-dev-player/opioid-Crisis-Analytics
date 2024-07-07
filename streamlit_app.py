import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load your CSV data
df = pd.read_csv('merged_file.csv')
df['TimeofAppointment'] = pd.to_datetime(df['TimeofAppointment'])
df['TimeSeenbyPhysician'] = pd.to_datetime(df['TimeSeenbyPhysician'])
df['PrescriptionDate'] = pd.to_datetime(df['PrescriptionDate'])

# Set the title at the top of the Streamlit app
st.title('Opioid Crisis Analysis')

# Sidebar options on the left side
st.sidebar.title('Select Options')
column_type = st.sidebar.selectbox('Select Column Type', ('Numerical', 'Categorical', 'Datetime'))

if column_type == 'Numerical':
    selected_column = st.sidebar.selectbox('Select Numerical Column:', df.select_dtypes(include=['number']).columns)

elif column_type == 'Categorical':
    selected_column = st.sidebar.selectbox('Select Categorical Column:', df.select_dtypes(include=['object', 'category']).columns)

elif column_type == 'Datetime':
    selected_datetime_column = st.sidebar.selectbox('Select Datetime Column:', df.select_dtypes(include=['datetime64']).columns)

# Button to show the graph
if st.sidebar.button('Show Graph'):
    if column_type == 'Numerical':
        # Plot histograms for numerical columns
        if df[selected_column].dtype in ['int64', 'float64']:
            fig, ax = plt.subplots()
            sns.histplot(df[selected_column], bins=20, kde=True, color='blue', edgecolor='black', alpha=0.7)
            ax.set_title(f'Histogram of {selected_column}', fontsize=16, fontweight='bold')
            ax.set_xlabel(selected_column, fontsize=14)
            ax.set_ylabel('Frequency', fontsize=14)
            ax.tick_params(axis='both', which='major', labelsize=12)
            st.pyplot(fig)

    elif column_type == 'Categorical':
        # Plot countplot for categorical columns
        if df[selected_column].dtype == 'object':
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=selected_column, palette="Set2", order=df[selected_column].value_counts().index, edgecolor='black')
            plt.title(f'Bar chart of {selected_column}', fontsize=16, fontweight='bold')  # Title for countplot
            plt.xlabel(selected_column, fontsize=14)
            plt.ylabel('Count', fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            st.pyplot()

        # Plot barplot for categorical vs numerical columns
        numerical_columns = df.select_dtypes(include=['number']).columns
        for num_col in numerical_columns:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=selected_column, y=num_col, data=df, palette="Set2", edgecolor='black')
            plt.title(f'Bar Plot of {selected_column} vs {num_col}', fontsize=16, fontweight='bold')  # Title for barplot
            plt.xlabel(selected_column, fontsize=14)
            plt.ylabel(num_col, fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            st.pyplot()

    elif column_type == 'Datetime':
        # Do nothing when datetime column is selected
        st.write("Please select a different column type or action.")