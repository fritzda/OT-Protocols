print("Rise and Shine")
# This will display "Hello, World!" in the terminal
print("Hello, World!")

# This will display your system version in the terminal
import sys
print(sys.version)


conda config --add channels conda-forge
conda config --add channels defaults
conda config --add channels r
conda config --add channels bioconda
conda install snp-sites

snp-sites -v -b  -o d3_test.vcf  /Users/fritzda/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Collaborators_Data/denv_seqs_wgs/whole_genome/d3_n625_degap.fas