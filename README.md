# Atuarial---Risco-de-credito

# 📊 Classificação de Risco de Resseguradoras - Automação SUSEP

Este projeto automatiza a extração e classificação de risco de resseguradoras, conforme determina a **Resolução CNSP nº 432/2021**, que regula o cálculo do **Capital de Risco de Crédito**.

---

## 💡 Objetivo

Evitar o processo manual e demorado de verificação das classificações de risco de **118 resseguradoras** (locais, admitidas e eventuais) no site da SUSEP, entregando uma solução automatizada, rápida e confiável.

---

## 🧠 Lógica do Script

### 🔍 Extração de Dados
- Utiliza as bibliotecas `requests`, `BeautifulSoup`, `urllib3` e `pandas`.
- Acessa e extrai automaticamente as informações do site da SUSEP.
- Coleta:
  - Nome da resseguradora
  - Notas de crédito atribuídas por agências como S&P, Moody's, Fitch e AM Best

### 🏷️ Classificação do Grau de Risco

| Grau | Notas de crédito |
|------|------------------|
| **Grau 1** | AAA até AA- |
| **Grau 2** | A+ até A- |
| **Grau 3** | BBB+ até BBB- |

- Se houver mais de uma nota, considera-se a **pior classificação**, conforme a legislação.

### 🧾 Classificação do Tipo de Contraparte

| Tipo | Descrição |
|------|-----------|
| **1** | Resseguradoras locais |
| **2** | Resseguradores admitidos |
| **3** | Resseguradores eventuais |
| **4** | RPEs que investem exclusivamente em títulos públicos pós-fixados atrelados à SELIC |

### 🧮 Cálculo do Fator de Risco
- Determinado a partir da **combinação entre tipo da contraparte e grau de risco**
- Utilizado no cálculo final do **Capital de Risco de Crédito**

---

## 📦 Tecnologias utilizadas
- `Python 3.x`
- `requests`
- `BeautifulSoup4`
- `urllib3`
- `pandas`

---

## 📊 Resultado

O script retorna um `DataFrame` com as seguintes colunas:

- ✅ Nome da resseguradora  
- 🏷️ Grau de risco  
- 🔍 Tipo de contraparte  
- 📉 Fator de risco correspondente  

*(Opcionalmente, pode ser exportado para Excel ou CSV)*

---

## ▶️ Como usar

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
