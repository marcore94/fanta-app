import pandas as pd
from unidecode import unidecode

# Funzione per normalizzare i nomi
def normalize_name(name):
    name = unidecode(name).lower().replace("'", "").strip()
    return name

# Funzione per estrarre la chiave di matching
def get_matching_key(name):
    tokens = name.split()
    parole_da_verificare = ['di', 'de', "del"]

    # Verifica se il primo token è in questa lista
    if len(tokens) > 1 and tokens[0].lower() in parole_da_verificare:
        return ' '.join(tokens[:2])  # Mantiene "Di Lorenzo"
    return tokens[0]  # Usa solo la prima parola

# Carica i dati da tutti i file CSV
fantapedia_df = pd.read_csv('./data/output/meanSkill.csv', encoding='latin-1')
#fantapedia_df = fantapedia_df[fantapedia_df["Nome"].str.contains("SERGI")]

# Carica i dati dal file Excel
fantacalcio_df = pd.read_excel('./data/input/Quotazioni_Fantacalcio_Stagione_2024_25.xlsx', skiprows=1)
#fantacalcio_df = fantacalcio_df[fantacalcio_df["Nome"].str.contains("Sergi")]

# Crea una colonna per la chiave di matching
fantapedia_df['MatchingKey'] = fantapedia_df['Nome'].apply(normalize_name)
fantacalcio_df['MatchingKey'] = fantacalcio_df['Nome'].apply(normalize_name)

# Unisci i DataFrame df e df2 usando la chiave di matching
merged_df = fantacalcio_df.merge(fantapedia_df, on='MatchingKey', how='left', suffixes=('_excel', '_csv'))

# Verifica le righe nel DataFrame finale
print("Righe nel DataFrame finale:", len(merged_df))
print("Prime righe del DataFrame finale:")
print(merged_df.head())

merged_df.loc[merged_df['R'].notna() & (merged_df['R'] != ''), 'Ruolo'] = merged_df['R']

merged_df.to_csv('./data/output/dati_uniti.csv', index=False)
