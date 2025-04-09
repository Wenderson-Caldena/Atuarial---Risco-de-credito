##### -------------------------- PARTE 1 ----------------- ####
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
from io import StringIO

# Desativa avisos de SSL inseguros
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Caminho do arquivo Excel de entrada
arquivo = r"C:\Users\RD136MM\Documents\PYTHON_RISCO CREDITO\resseguradoras.xlsx"
df_codigos = pd.read_excel(arquivo, sheet_name="resseguradoras")

# Lista para armazenar os dados coletados
dados_classificacao = []

# Loop pelos códigos de resseguradoras
for _, linha in df_codigos.iterrows():
    codigo = str(linha['CODIGO'])
    modalidade = linha['MODALIDADE']
    resseguradora = linha['RESSEGURADORA']

    url = f"https://www2.susep.gov.br/menuatendimento/info_resseguradoras_2011.asp?entcodigo={codigo}&codativo=True"

    try:
        response = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabelas_html = soup.find_all('table')

        if not tabelas_html:
            raise Exception("Nenhuma tabela encontrada")

        tabela_final = pd.read_html(StringIO(str(tabelas_html[-1])))[0]

        # ✅ Verifica se há pelo menos 2 linhas para acessar [1, 0] e [1, 1]
        if tabela_final.shape[0] > 1:
            classificadora = tabela_final.iloc[1, 0]
            nota = tabela_final.iloc[1, 1]
        else:
            classificadora = None
            nota = None

        dados_classificacao.append({
            "MODALIDADE": modalidade,
            "RESSEGURADORA": resseguradora,
            "CODIGO": codigo,
            "CLASSIFICADORA": classificadora,
            "NOTA": nota
        })

    except Exception as e:
        print(f"Erro no código {codigo}: {e}")
        dados_classificacao.append({
            "MODALIDADE": modalidade,
            "RESSEGURADORA": resseguradora,
            "CODIGO": codigo,
            "CLASSIFICADORA": None,
            "NOTA": None
        })

# Cria DataFrame final com os dados coletados
df_resultado = pd.DataFrame(dados_classificacao)

##### ------------------PARTE 2 ---------------------- ####

import pandas as pd

# === 1. Mapeamento de CLASSIFICADORA + NOTA -> GRUPO (mantém o mesmo)
regras_grupo = pd.DataFrame({
    "CLASSIFICADORA": [
        "A. M. Best Company", "A. M. Best Company", "A. M. Best Company", "A. M. Best Company", "A. M. Best Company", "A. M. Best Company",
        "FR", "FR", "FR", "FR", "FR", "FR", "FR", "FR", "FR", "FR",
        "Moody's Investors Services", "Moody's Investors Services", "Moody's Investors Services", "Moody's Investors Services",
        "Moody's Investors Services", "Moody's Investors Services", "Moody's Investors Services", "Moody's Investors Services", "Moody's Investors Services",
        "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH",
        "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH", "Standard & Poor's / FITCH"
    ],
    "NOTA": [
        "A++", "A+", "A", "A-", "B++", "B+",
        "AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-",
        "Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2",
        "AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-"
    ],
    "GRUPO": [
        1, 1, 2, 2, 3, 3,
        1, 1, 1, 1, 2, 2, 2, 3, 3, 3,
        1, 1, 1, 1, 2, 2, 2, 3, 3,
        1, 1, 1, 1, 2, 2, 2, 3, 3, 3
    ]
})

# === 2. Mapeamento de MODALIDADE -> TIPO
regras_tipo = pd.DataFrame({
    "MODALIDADE": ["LOCAL", "ADMITIDA", "EVENTUAL"],
    "TIPO": [1, 2, 3]
})

# === 3. Carrega arquivo com resultado anterior
df = df_resultado

# === 4. Faz merge com GRUPO
df = df.merge(regras_grupo, on=["CLASSIFICADORA", "NOTA"], how="left")

# === 5. Faz merge com TIPO
df = df.merge(regras_tipo, on="MODALIDADE", how="left")

#### ----------------------- PARTE 3 ----------------- ####

import pandas as pd


# 2. Matriz de risco
risco_matrix = pd.DataFrame({
    1: [0.0193, 0.0000, 0.0000],  # Tipo 1
    2: [0.0253, 0.0456, 0.1136],  # Tipo 2
    3: [0.0304, 0.0548, 0.1363],  # Tipo 3
}, index=[1, 2, 3])  # GRUPOs

# 3. Função para buscar risco
def buscar_risco(row):
    grupo = row["GRUPO"]
    tipo = row["TIPO"]
    try:
        return risco_matrix.loc[grupo, tipo]
    except:
        return None

# 4. Aplica grau de risco via matriz
df["GRAU_RISCO"] = df.apply(buscar_risco, axis=1)

# ✅ 5. Força risco fixo para modalidade LOCAL
df.loc[df["MODALIDADE"] == "LOCAL", "GRAU_RISCO"] = 0.0193

# 6. Exporta resultado
saida = r"C:\Users\RD136MM\Documents\PYTHON_RISCO CREDITO\classificacao_com_risco.xlsx"
df.to_excel(saida, index=False)

print("✅ GRAU_RISCO ajustado com sucesso (incluindo regra para 'LOCAL')")