import pandas as pd

# Path file Excel (.xlsx)
input_file = 'rumah_cleaned.xlsx'
output_file = 'rumah_cleaned.csv'

# Membaca file Excel
df = pd.read_excel(input_file)

# Menyimpan sebagai file CSV
df.to_csv(output_file, index=False)

print(f"File telah dikonversi menjadi CSV: {output_file}")
