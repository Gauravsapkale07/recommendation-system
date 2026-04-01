import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Recommendation System", layout="wide")

# ---------- LOAD DATA ----------
products = pickle.load(open('products.pkl', 'rb'))
df = pd.read_csv('rating_short.csv')

# ---------- FIX IMAGE ISSUE ----------
products['image'] = products.get('image', "https://via.placeholder.com/150")
products['image'] = products['image'].fillna("https://via.placeholder.com/150")

# ---------- UI ----------
st.title("🛍 Smart Product Recommendation")

search = st.text_input("🔍 Search Product")

filtered_products = products[
    products['product_name'].str.contains(search, case=False, na=False)
] if search else products

selected_product = st.selectbox(
    "Select product",
    filtered_products['product_name'].values
)

# ---------- RECOMMEND FUNCTION (FIXED) ----------
def recommend(product_name):
    try:
        product_id = products[
            products['product_name'] == product_name
        ]['productid'].values[0]

        # Users who interacted with selected product
        users = df[df['productid'] == product_id]['userid']

        # If no users → fallback (top products)
        if len(users) == 0:
            top_products = df['productid'].value_counts().index[:6]
        else:
            similar = df[df['userid'].isin(users)]
            top_products = similar['productid'].value_counts().index[:6]

        recommended = []
        for pid in top_products:
            temp = products[products['productid'] == pid]
            if not temp.empty:
                recommended.append(temp.iloc[0])

        return recommended

    except:
        return []

# ---------- BUTTON ----------
if st.button("✨ Recommend"):
    st.write(f"Because you selected **{selected_product}**")

    results = recommend(selected_product)

    if results:
        cols = st.columns(3)

        for i, row in enumerate(results):
            with cols[i % 3]:
                st.image(row['image'], width=150)
                st.write(f"**{row['product_name']}**")
                st.write(f"⭐ {row.get('rating', 4.2)}")
                st.write(f"₹ {row.get('price', 999)}")
    else:
        st.error("No recommendations found")