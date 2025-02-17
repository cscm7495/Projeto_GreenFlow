import pandas as pd
import os

# File path
file_path = 'data/dados_sensores_5000.parquet'

# Clean duplicates and remove null values
def clean_data(df):
    duplicates = df.duplicated()
    if duplicates.any():
        # Remove duplicates
        cleaned_df = df.drop_duplicates()
        # Optionally, reset the index
        cleaned_df.reset_index(drop=True, inplace=True)
    else:
        cleaned_df = df

    # Check for null values
    null_values = cleaned_df.isnull().sum()
    if null_values.any():
        # Fill null values with 0
        cleaned_df = cleaned_df.fillna(0)

    return cleaned_df

def dataset_summary(df):
    # Summary
    print("Basic Information:")
    print(df.info())

    # Statistical summary
    print("\nStatistical Summary:")
    print(df.describe())

    # Correlation Matrix
    print(df[['energia_kwh', 'agua_m3', 'co2_emissoes']].corr())

# Save data
def save_data(df, output_file):
    try:
        df.to_parquet(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
    except Exception as e:
        print(f"Error occurred while saving data: {e}")

#Call Functions
try:
    df = pd.read_parquet(file_path)
    print(df)

    # Clean the data
    cleaned_df = clean_data(df)

    # Save the cleaned data
    output_file = 'data/dados_sensores_5000_limpos.parquet'
    save_data(cleaned_df, output_file)

except Exception as e:
    print(f"Error occurred: {e}")

dataset_summary(cleaned_df)
