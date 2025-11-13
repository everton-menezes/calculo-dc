# Cálculo de Direito Creditório (V0.1 – MVP manual)

Pipeline focado em leitura, limpeza e consolidação de dados para cálculo de valor de direito creditório.

## Estrutura

├── data/ │ ├── input/ │ │ ├── processos.csv │ │ ├── hospitais.csv │ │ └── raw/ │ │ └── sih_cnv_spgsp105259191_181_57_192.csv │ └── output/ ├── scripts/ │ └── aula01_tratamento_sih.py ├── requirements.txt └── README.md
## Pré-requisitos
- Python 3.11+
- VS Code + extensão Python

## Setup rápido
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Como rodar
	1	Garanta os arquivos de entrada em data/input/ e data/input/raw/.
	2	Execute a Aula 1 (parser SIH):

python scripts/tratamento-sih.py
	3	Saídas são gravadas em data/output/.
Dados de entrada (cabecalhos)
	•	processos.csv id_processo,cnpj_hospital,data_distribuicao,data_citacao,data_transito,data_sentenca,data_precatorio,data_pgto,data_calculo,descricao,observacoes
	•	hospitais.csv cnpj_hospital,razao_social,nome_fantasia,cnes,uf,municipio
