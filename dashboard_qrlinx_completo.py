
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Carregamento de dados (exemplo)
df = pd.read_excel("Adiantamentos Recebidos _BANCO - Copia.xlsx", sheet_name='base')
df['DTA_EMISSAO'] = pd.to_datetime(df['DTA_EMISSAO'], errors='coerce')
df['ANO_MES'] = df['DTA_EMISSAO'].dt.to_period('M')

# Totais e percentuais por origem e revenda
total_por_revenda = df.groupby('REVENDA')['VALOR'].sum().reset_index(name='TOTAL_REVENDA')
total_por_origem = df.groupby(['REVENDA', 'ORIGEM'])['VALOR'].sum().reset_index()
total_merged = pd.merge(total_por_origem, total_por_revenda, on='REVENDA')
total_merged['PERCENTUAL'] = (total_merged['VALOR'] / total_merged['TOTAL_REVENDA']) * 100

# Evolução QR LINX
df_qrlinx = df[df['ORIGEM'] == '03020-ADTO-QR LINX']
evolucao_qrlinx = df_qrlinx.groupby(['ANO_MES', 'REVENDA'])['VALOR'].sum().reset_index()

# Ranking QR LINX
ranking_qrlinx = df_qrlinx.groupby('REVENDA')['VALOR'].sum().reset_index().sort_values(by='VALOR', ascending=False)

st.title("📊 Dashboard - Uso do QR LINX nas Revendas do Grupo Linhares")

# Seção 1: Totais e Percentuais
st.subheader("Totais e Percentuais de Recebimentos por Origem e Revenda")
st.dataframe(total_merged.style.format({"VALOR": "R$ {:,.2f}", "TOTAL_REVENDA": "R$ {:,.2f}", "PERCENTUAL": "{:.2f}%"}))

# Seção 2: 📈 Evolução Mensal do Uso do QR LINX
st.subheader("📈 Evolução Mensal do Uso do QR LINX")
fig1, ax1 = plt.subplots(figsize=(14, 6))
evolucao_qrlinx_plot = evolucao_qrlinx.copy()
evolucao_qrlinx_plot['ANO_MES'] = evolucao_qrlinx_plot['ANO_MES'].astype(str)
sns.lineplot(data=evolucao_qrlinx_plot, x='ANO_MES', y='VALOR', hue='REVENDA', marker="o", ax=ax1)
plt.xticks(rotation=45)
plt.xlabel('Ano-Mês')
plt.ylabel('Valor Recebido (R$)')
plt.grid(True)
plt.tight_layout()
st.pyplot(fig1)

# Seção 3: 📌 Comparativo entre Origens por Revenda
st.subheader("📌 Comparativo entre Origens por Revenda")
fig2, ax2 = plt.subplots(figsize=(14, 8))
dest = total_merged.copy()
dest['ORIGEM'] = dest['ORIGEM'].str.replace('03020-ADTO-QR LINX', '🔵 03020-ADTO-QR LINX')
sns.barplot(data=dest.sort_values(by=['REVENDA', 'VALOR'], ascending=[True, False]), x='VALOR', y='REVENDA', hue='ORIGEM', ax=ax2)
plt.xlabel('Valor Total Recebido (R$)')
plt.ylabel('Revenda')
plt.title('Recebimentos por Origem nas Revendas')
st.pyplot(fig2)

# Seção 4: 🥇 Ranking de Revendas pelo Uso do QR LINX
st.subheader("🥇 Ranking de Revendas pelo Uso do QR LINX")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=ranking_qrlinx, x='VALOR', y='REVENDA', palette='Blues_d', ax=ax3)
plt.xlabel('Valor Total Recebido via QR LINX (R$)')
plt.ylabel('Revenda')
plt.title('Top Revendas - QR LINX')
st.pyplot(fig3)
