import pandas as pd
import random

# List of real phyla (from various kingdoms of life)
phyla = [
    "Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Ascomycota", 
    "Basidiomycota", "Ciliophora", "Chytridiomycota", "Cyanobacteria", "Euglenozoa", 
    "Glomeromycota", "Mollusca", "Nematoda", "Porifera", "Arthropoda", "Chordata", 
    "Annelida", "Bryophyta", "Pteridophyta", "Ginkgophyta", "Coniferophyta"
]

# Function to generate synthetic species names
def generate_species_name(species_id):
    return f"Species{species_id}"

# Create a list to store the rows of data
data = []

# Generate 1000 rows of data
for i in range(1, 1001):
    species_name = generate_species_name(i)
    phylum = random.choice(phyla)
    count = random.randint(1, 500)  # Random count between 1 and 500
    data.append([species_name, phylum, count])

# Create a DataFrame
df = pd.DataFrame(data, columns=["species", "phylum", "count"])

# Save to CSV
df.to_csv("synthetic_taxonomic_data.csv", index=False)

print("Synthetic dataset with 1000 rows generated and saved as 'synthetic_taxonomic_data.csv'.")
