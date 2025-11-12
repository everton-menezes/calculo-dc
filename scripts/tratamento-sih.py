import pandas as pd

# Caminho do arquivo original
arquivo_raw = "data/input/raw/sih_cnv_spgsp105259191_181_57_192.csv"

# 1) Tentativa de leitura direta
try:
    df = pd.read_csv(arquivo_raw)
    print("Leitura padrão funcionou")
except Exception as e:
    print("Leitura padrão falhou")    