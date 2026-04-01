import streamlit as st
import pickle
import pandas as pd

# Load data
products = pickle.load(open('products.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Recommendation System", layout="wide")

# ----------- CUSTOM CSS (Design) -----------
st.markdown("""
<style>
.card {
    padding: 10px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    background-color: #ffffff;
}
.title {
    font-size: 18px;
    font-weight: bold;
}
.price {
    color: green;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.title("🛍 Smart Product Recommendation")
st.write("Get similar products instantly")

# ----------- SEARCH BAR -----------
search = st.text_input("🔍 Search Product")

# Auto suggestions
filtered_products = products[products['product_name'].str.contains(search, case=False, na=False)] if search else products

selected_product = st.selectbox(
    "Select product",
    filtered_products['product_name'].values
)

# ----------- RECOMMEND FUNCTION -----------
def recommend(product):
    index = products[products['product_name'] == product].index[0]
    distances = similarity[index]

    product_list = sorted(list(enumerate(distances)),
                          reverse=True,
                          key=lambda x: x[1])[1:7]

    recommended = []
    for i in product_list:
        recommended.append(products.iloc[i[0]])

    return recommended

# ----------- BUTTON -----------
if st.button("✨ Recommend"):
    results = recommend(selected_product)

    st.subheader("🔥 Similar Products")

    cols = st.columns(3)

    for i, row in enumerate(results):
        with cols[i % 3]:
            image = row.get('image', 'https://via.placeholder.com/150')
            name = row.get('product_name', 'Product')
            rating = row.get('rating', 4.2)
            price = row.get('price', 999)

            st.markdown(f"""
            <div class="card">
                <img src="{image}" width="150">
                <div class="title">{name}</div>
                ⭐ {rating} <br>
                <div class="price">₹ {price}</div>
            </div>
            """, unsafe_allow_html=True)