import pandas as pd
import matplotlib.pyplot as plt
import argparse
from itertools import cycle

# Function to load and validate data
def load_and_validate_data(input_file):
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

    # Check the columns of the input data
    required_columns = ['species', 'phylum', 'count']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"The CSV file must contain the following columns: {required_columns}")
    
    # Check if the input file contains invalid or missing data
    df = df.dropna(subset=['species', 'phylum', 'count'])  # Drop rows with missing values
    df['count'] = pd.to_numeric(df['count'], errors='coerce')  # Convert 'count' to numeric
    df = df.dropna(subset=['count'])  # Drop rows where 'count' is invalid
    df = df[df['count'] >= 0]  # Remove rows with negative counts

    return df

# Function to calculate summary statistics
def calculate_summary_statistics(df):
    total_species_count = df.groupby('phylum')['count'].sum().reset_index()
    total_species_count.columns = ['Phylum', 'Total Species Count']
    
    avg_species_count = df.groupby('phylum')['count'].mean().reset_index()
    avg_species_count.columns = ['Phylum', 'Average Species Count']
    avg_species_count['Average Species Count'] = avg_species_count['Average Species Count'].round(2)
    
    # Merge total and average count dataframes
    summary_df = pd.merge(total_species_count, avg_species_count, on='Phylum')

    # Sort by average species count in descending order
    summary_df = summary_df.sort_values(by='Average Species Count', ascending=False)

    return summary_df

# Function to plot a bar chart
def plot_bar_chart(summary_df, sort_by='abundance', output_png='phylum_species_count', resolution=(300, 300), color_scheme='d3'):
    # Sorting based on the user's choice
    if sort_by == 'abundance':
        summary_df_sorted = summary_df.sort_values(by='Total Species Count', ascending=False)
    elif sort_by == 'alphabetical':
        summary_df_sorted = summary_df.sort_values(by='Phylum', ascending=True)
    else:
        raise ValueError("Invalid sorting option. Use 'abundance' or 'alphabetical'.")

    # Define color palette using D3's category20 colors
    if color_scheme == 'd3':
        # D3 category20 color palette
        d3_category20_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", 
            "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#9edae5", "#f7b6d2", 
            "#c5b0d5", "#c49c94", "#f0e3a1", "#e7ba52", "#9c7561", "#d9d9d9", 
            "#8c6d31", "#7b4173"
        ]
        colors = cycle(d3_category20_colors)  # Loop over the 20 colors if needed for more than 20 categories
    else:
        colors = 'tomato'  # Default color scheme

    # Plot the bar chart with the specified resolution
    plt.figure(figsize=(12, 8), dpi=resolution[0])
    plt.bar(summary_df_sorted['Phylum'], summary_df_sorted['Total Species Count'], color=[next(colors) for _ in range(len(summary_df_sorted))])
    plt.xlabel('Phylum', fontsize=14)
    plt.ylabel('Total Species Count', fontsize=16)
    plt.title('Total Species Count by Phylum', fontsize=20)
    plt.xticks(rotation=45, ha='right', fontsize=14)
    plt.tight_layout()

    # Save the chart
    plt.savefig(str(output_png) + '.png', dpi=resolution[0])

# Function to save summary statistics to a CSV file
def save_summary_to_csv(summary_df, output_file):
    summary_df.to_csv(output_file, index=False)
    print(f"Summary statistics saved to {output_file}")

# Main function to analyze the taxonomic data
def analyze_taxonomic_data(input_file, output_file, output_png, sort_by='total', resolution=(300, 300), color_scheme='d3'):
    df = load_and_validate_data(input_file)
    summary_df = calculate_summary_statistics(df)
    save_summary_to_csv(summary_df, output_file)
    plot_bar_chart(summary_df, sort_by, output_png, resolution, color_scheme)

# Entry point for the script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze taxonomic data and generate summary statistics and visualizations.")
    parser.add_argument('-i', '--input', required=True, help="Input CSV file containing taxonomic data.")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file to save the summary statistics.")
    parser.add_argument('-p', '--png', default='phylum_species_count', help="Output PNG file to save the barchart.")
    parser.add_argument('--sort', choices=['abundance', 'alphabetical'], default='abundance', help="Sort the chart by 'abundance' or 'alphabetical'. Default is 'total'.")
    parser.add_argument('--dpi', type=int, default=300, help="Resolution (DPI) of the output chart. Default is 300.")
    parser.add_argument('--color', choices=['d3', 'default'], default='d3', help="Color scheme for the chart. 'd3' or 'default'. Default is 'd3'.")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output
    output_png = args.png
    sort_method = args.sort
    resolution = args.dpi
    color_scheme = args.color
    
    analyze_taxonomic_data(input_file, output_file, output_png, sort_method, (resolution, resolution), color_scheme)
