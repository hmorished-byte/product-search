import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Company Product Search", layout="wide")

st.title("🔎 MOH / NUPCO Code Search")
st.markdown("Search by **any** detail (ID, NUPCO Code, Description, Trade Code, etc.)")

@st.cache_data
def load_data():
    try:
        # First try: UTF-8 (Standard)
        df = pd.read_csv('data.csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            # Second try: UTF-8 with BOM (Common for Excel files)
            df = pd.read_csv('data.csv', encoding='utf-8-sig')
        except UnicodeDecodeError:
            # Third try: Latin-1 (Fallback for Western encoding)
            df = pd.read_csv('data.csv', encoding='latin1')
    
    df = df.fillna("")
    df['search_combined'] = df.astype(str).agg(' '.join, axis=1)
    return df

try:
    data = load_data()

    # User Input
    search_query = st.text_input("Type anything to search all columns:", placeholder="e.g. 55121608, Syringe, or Formtec")

    if search_query:
        # Search the query within the 'search_combined' column (fastest for 150k+ rows)
        mask = data['search_combined'].str.contains(search_query, case=False, na=False)
        results = data[mask].drop(columns=['search_combined']) # Drop the hidden column before showing results

        st.success(f"Found {len(results)} matches")
        
        # Display the results
        st.dataframe(
            results, 
            use_container_width=True, 
            hide_index=True
        )
        
        # Option to download the filtered results back to Excel
        if not results.empty:
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download results as CSV",
                data=csv,
                file_name='search_results.csv',
                mime='text/csv',
            )
    else:
        st.info("💡 **Tip:** You can search for a NUPCO Generic Code, a Trade Description, or even a Customer MAT Number. Anything you see in the Excel headers is searchable.")

except Exception as e:
    st.error(f"Error: {e}")