import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_excel("Vendas_Base_de_Dados.xlsx")
data["Revenue"] = data["Quantidade"] * data["Valor Unitário"]

st.title("Dashboard de Vendas")
st.sidebar.header("Filtros")

storeList = sorted(data["Loja"].unique())
storeList.insert(0, "Todas")

selectedStore = st.sidebar.selectbox(
    "Loja",
    storeList
)

if selectedStore == "Todas":
    storeData = data
else:
    storeData = data[data["Loja"] == selectedStore]

productList = sorted(storeData["Produto"].unique())
productList.insert(0, "Todos")

selectedProduct = st.sidebar.selectbox(
    "Produto",
    productList
)

if selectedProduct == "Todos":
    filteredData = storeData
else:
    filteredData = storeData[
        storeData["Produto"] == selectedProduct
    ]

totalRevenue = filteredData["Revenue"].sum()

st.metric(
    "Faturamento",
    f"R$ {totalRevenue:,.2f}"
)

if selectedStore != "Todas":
    if selectedProduct != "Todos":
        st.info(
            f"Na loja {selectedStore}, o produto "
            f"{selectedProduct} faturou "
            f"R$ {totalRevenue:,.2f}."
        )

st.subheader("Dados")
st.dataframe(filteredData)

chartData = (
    filteredData.groupby("Loja")["Revenue"]
    .sum()
    .reset_index()
)

barChart = px.bar(
    chartData,
    x="Loja",
    y="Revenue",
    title="Faturamento por Loja",
    color="Loja"
)

st.plotly_chart(barChart)

if selectedStore != "Todas":
    pieData = data[data["Loja"] == selectedStore]

    pieData = (
        pieData.groupby("Produto")["Revenue"]
        .sum()
        .reset_index()
    )

    pieChart = px.pie(
        pieData,
        names="Produto",
        values="Revenue",
        title=f"Produtos da loja {selectedStore}"
    )

    st.plotly_chart(pieChart)