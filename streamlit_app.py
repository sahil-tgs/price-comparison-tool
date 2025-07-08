import streamlit as st
import requests
import json

st.title("🛒 Price Comparison Tool")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox(
        "Country",
        ["US", "IN", "UK", "CA", "AU", "DE", "FR", "JP", "CN"]
    )

with col2:
    query = st.text_input("Product Query", placeholder="e.g. iPhone 16 Pro, 128GB")

if st.button("Search Prices", type="primary"):
    if query:
        with st.spinner("Searching for best prices..."):
            try:
                response = requests.post(
                    "http://localhost:8000/search",
                    json={"country": country, "query": query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success(f"Found {len(data['results'])} results")
                    
                    for idx, product in enumerate(data['results']):
                        with st.expander(f"{product['productName'][:60]}... - {product['currency']} {product['price']}"):
                            st.write(f"**Price:** {product['currency']} {product['price']}")
                            st.write(f"**Source:** {product.get('source', 'Unknown')}")
                            st.write(f"**Link:** {product['link']}")
                else:
                    st.error("No results found")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a product query")

# Add example queries
with st.sidebar:
    st.header("Example Queries")
    st.code('{"country": "US", "query": "iPhone 16 Pro, 128GB"}')
    st.code('{"country": "IN", "query": "boAt Airdopes 311 Pro"}')