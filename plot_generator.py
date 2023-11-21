import pandas as pd
import matplotlib.pyplot as plt
import os


# ENTER YOUR VARIABLE HERE
# ========================
variable = 'National Rainfall Index (NRI)'

# Download the data from https://yaon.org/data.csv




print("Loading Dataset")

'''import csv'''
csv_path = 'data.csv'
import_df = pd.read_csv(csv_path)
import_df.drop(columns=['Unnamed: 0'], inplace=True)
'''Format dataframe'''
df = import_df.pivot_table(index=['Country', 'Year'], columns='Variable', values='Value', aggfunc='first')
df.reset_index(inplace=True)


'''relevant variables for us'''
relevant_vars = [variable,                 
                ]
'''filter countries (no filter if empty)'''
filter_countries = []


'''Extract relevant variables and drop all NaN'''
data = df[['Country', 'Year', *relevant_vars]]
if filter_countries:
    data = data[data['Country'].isin(filter_countries)]
data = data.dropna()



# Create the 'x' folder if it doesn't exist
output_folder = 'plots'
os.makedirs(output_folder, exist_ok=True)

# Iterate over unique countries in the dataset
for country in df['Country'].unique():
    # Filter data for the current country
    country_data = df[df['Country'] == country]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(country_data['Year'], country_data[variable],
             marker='o', linestyle='-', color='b')

    # Set labels and title
    plt.xlabel('Year')
    plt.ylabel(variable)
    plt.title(f'{variable} in {country} over the Years')

    # Show the plot
    plt.grid(True)

    # Save the plot as an image in the 'x' folder
    output_filename = os.path.join(output_folder, f'{country}_plot.png')
    plt.savefig(output_filename)

    # Close the plot to avoid displaying it in the loop
    plt.close()

    print(f"Generating plot for {country}")

print("Plots saved!")