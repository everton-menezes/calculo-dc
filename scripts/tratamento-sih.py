import pandas as pd
import re
from pathlib import Path
from io import StringIO

# Passo 1: abrir o arquivo bruto como TEXTO e imprimir as 30 primeiras linhas numeradas

caminho = "data/input/raw/sih_cnv_spgsp105259191_181_57_192.csv"

# 'encoding="latin-1"' porque o arquivo tem acentos no padrão Brasil/Windows
with open(caminho, "r", encoding="latin-1", errors="replace") as f:
    linhas = f.readlines()  # lê todas as linhas do arquivo em uma lista de strings

# Função que procura a linha que começa a planilha dentro do arquivo
inicio = None
for i, linha in enumerate(linhas):
    if '"Ano/m' in linha and '"Quantidade_aprovada"' in linha and '"Valor_aprovado"' in linha:
        inicio = i
        break
    inicio = 0

print("Índice do cabeçalho encontrado:", inicio)

# encontrar o índice da linha que começa com "Total";
fim = None
for i, linha in enumerate(linhas):
    if linha.startswith('"Total";'):
        fim = i
        break
    fim = len(linhas)

linhas_tabela = linhas[inicio:fim]

# Transformar esse pedaço em um "arquivo em memória"
texto_limpo = "".join(linhas_tabela)             # junta lista -> string
arquivo_virtual = StringIO(texto_limpo)          # vira "arquivo" em memória

# Função que lê o arquivo após o header e converte o Encoding para latin-1
df = pd.read_csv(
    arquivo_virtual,     # arquivo virtual, que substituiu o caminho
    encoding="latin-1",  # acentos BR
    sep=";",             # separador é ponto e vírgula
    quotechar='"',       # campos entre aspas
    decimal=","          # converte 150568707,15 -> 150568707.15
)

col0 = df.columns[0]  # nome da 1ª coluna (ex.: "Ano/mês processamento")

# máscara True para linhas que são exatamente 4 dígitos
mask_ano = df[col0].astype(str).str.fullmatch(r"\d{4}")

# mantemos apenas as linhas que NÃO são ano
df = df[~mask_ano].copy()

# Criando um dicionário para transformar meses em texto para números
MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

def para_data_ptbr(texto):
    if pd.isna(texto):            # 1. Se for vazio, retorna sem data
        return pd.NaT

    s = str(texto).lower().strip().strip('"')  # 2. limpa texto
    s = s.replace("..", "")                    # 3. tira “..”
    
    # 4. tenta separar mês e ano com regex
    m = re.match(r'([a-zçáéíóúâêôãõ]+)\s*/\s*(\d{4})', s)
    if not m:
        return pd.NaT

    nome_mes = m.group(1)
    ano = int(m.group(2))

    # 5. busca número do mês
    mes = MESES.get(nome_mes)
    if not mes:
        return pd.NaT

    # 6. cria e retorna a data
    return pd.Timestamp(year=ano, month=mes, day=1)

col0 = df.columns[0]
print("Coluna usada:", col0)

df["data"] = df[col0].map(para_data_ptbr)

# Quantas linhas ficaram sem data?
erros = df["data"].isna().sum()
print("Linhas sem data:", erros)

# remover a coluna textual "Ano/mês processamento"
df = df.drop(columns=[col0])
df = df.iloc[:, [2, 0, 1]]

print("Colunas após remover a coluna textual:", list(df.columns))

df["data"] = pd.to_datetime(df["data"], errors="coerce")
data_min = df["data"].min()
data_max = df["data"].max()
aaaamm_min = data_min.strftime("%Y%m") if pd.notna(data_min) else "000000"
aaaamm_max = data_max.strftime("%Y%m") if pd.notna(data_max) else "000000"
print("Faixa para nome:", aaaamm_min, aaaamm_max)

linha_estab = next((L for L in linhas if "Estabelecimento:" in L), None)
if linha_estab is None:
    raise RuntimeError("Não encontrei a linha 'Estabelecimento:' no cabeçalho.")
m = re.search(r"Estabelecimento:\s*(\d+)", linha_estab)
if not m:
    raise RuntimeError("Não consegui extrair o CNES da linha de Estabelecimento.")
cnes = m.group(1)
print("CNES extraído:", cnes)

caminho_saida = Path(f"data/output/sih_{cnes}_{aaaamm_min}-{aaaamm_max}.csv")

# Recomendação: separador ';' e UTF-8 com BOM (melhor para Excel)
df.to_csv(
    caminho_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
print("Arquivo salvo em:", caminho_saida)

# Impressões de teste
'''
    print("\nDimensão do DF:", df.shape)
    print("\nPrimeiras 5 linhas:")
    print(df.head(10))

    print("\nÚltimas 5 linhas (checar que 'Total' sumiu):")
    print(df.tail(5))
'''