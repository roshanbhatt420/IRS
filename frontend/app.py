import streamlit as st
import os
from PIL import Image
# import backend  

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Second Brain",
    page_icon="🧠",
    layout="wide"
)

# Ensure the 'data' folder 
if not os.path.exists("data"):
    os.makedirs("data")

# --- HEADER ---
st.title("🧠 AI Second Brain")
st.markdown("""
*Upload your chaos. Search by meaning.*  
This system uses **OCR**, **Neural Image Captioning**, and **Vector Embeddings** to make your screenshots searchable.
""")


tab1, tab2 = st.tabs(["📤 Add to Brain", "🔍 Search Memory"])

# ==========================================
with tab1:
    st.header("Upload Screenshots")
    
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # 1. Show the user a preview of the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview", width=300)
        
        # 2. Button to Trigger AI Processing
        if st.button("🧠 Process & Index"):
            with st.spinner("Reading text, analyzing visuals, and embedding vectors..."):
                
                # Save file locally first (so the backend can read it)
                file_path = os.path.join("data", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Call the Backend!
                try:
                    context = backend.ingest_screenshot(file_path)
                    st.success("✅ Successfully added to Second Brain!")
                    st.info(f"**AI Interpretation:** {context}")
                except Exception as e:
                    st.error(f"Error processing image: {e}")


# TAB 2: SEARCH
with tab2:
    st.header("Search your Knowledge Base")
    
    # Search Bar
    query = st.text_input("What are you looking for?", placeholder="e.g., 'Receipt for sushi', 'Python error message', 'WiFi password'")
    
    # Optional Date Filter (As per your architecture)
    filter_date = st.date_input("Filter by Date (Optional)", value=None)
    use_date_filter = st.checkbox("Apply Date Filter")
    
    if st.button("🔍 Search"):
        if query:
            with st.spinner("Thinking..."):
                # Handle Date Logic
                date_str = None
                if use_date_filter and filter_date:
                    date_str = filter_date.strftime('%Y-%m-%d')
                
                # Call Backend
                results = backend.search_brain(query, date_str)
                
                # Display Results
                if not results['ids'][0]:
                    st.warning("No matches found.")
                else:
                    st.markdown("### Top Matches")
                    
                    # Loop through results
                    # ChromaDB returns lists of lists, so we need to be careful with indices
                    num_results = len(results['ids'][0])
                    
                    for i in range(num_results):
                        col1, col2 = st.columns([1, 2])
                        
                        file_path = results['ids'][0][i]
                        score = results['distances'][0][i] # Lower distance = better match
                        metadata = results['metadatas'][0][i]
                        context_text = results['documents'][0][i]
                        
                        with col1:
                            if os.path.exists(file_path):
                                st.image(file_path, width=200)
                            else:
                                st.error(f"Image not found at {file_path}")
                        
                        with col2:
                            st.subheader(f"Result #{i+1}")
                            st.caption(f"📅 Date: {metadata['date']}")
                            st.write(f"**AI Context:** {context_text}")
                            st.progress(max(0.0, 1.0 - score), text="Relevance Score") # Visual score bar
                        
                        st.divider()