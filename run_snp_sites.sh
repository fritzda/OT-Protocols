#!/bin/bash

# Directory containing .fas files (update this path as needed)
INPUT_DIR="/Users/fritzda/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Collaborators_Data/denv_seqs_wgs/gene"

# Output directory for .vcf files (optional, defaults to input directory)
OUTPUT_DIR="$INPUT_DIR"

# Loop through each .fas file in the input directory
for file in "$INPUT_DIR"/*underscore.fas; do
  # Get the base name of the file (without the directory and extension)
  base_name=$(basename "$file" .fas)
  
  # Define the output VCF file path
  output_file="$OUTPUT_DIR/${base_name}_bioconda.vcf"
  
  # Run snp-sites
  snp-sites -v -b -o "$output_file" "$file"
  
  # Print a message indicating completion for each file
  echo "Processed $file -> $output_file"
done

echo "All .fas files processed!"