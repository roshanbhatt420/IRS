import streamlit as st
import os
from PIL import Image
import backend  # Your backend logic
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Second Brain",
    page_icon="🧠",
    layout="wide"
)

# Ensure the 'data' folder exists
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
# TAB 1: INGESTION (Modified for Bulk)
# ==========================================
with tab1:
    st.header("Ingest Knowledge")
    
    # User chooses method
    ingest_type = st.radio("Choose Method:", ["📂 Upload Multiple Files", "💻 Scan Local Folder Path"])

    # --- METHOD A: UPLOAD FILES (Drag & Drop) ---
    if ingest_type == "📂 Upload Multiple Files":
        uploaded_files = st.file_uploader(
            "Choose images...", 
            type=['png', 'jpg', 'jpeg'], 
            accept_multiple_files=True  # <--- THIS ALLOWS SELECTING MANY FILES
        )
        
        if uploaded_files:
            st.write(f"Selected {len(uploaded_files)} images.")
            
            if st.button("🧠 Process All Images"):
                # Progress Bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, uploaded_file in enumerate(uploaded_files):
                    # 1. Save file locally
                    file_path = os.path.join("data", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # 2. Update Status
                    status_text.text(f"Processing {i+1}/{len(uploaded_files)}: {uploaded_file.name}...")
                    
                    # 3. Call Backend
                    try:
                        backend.ingest_screenshot(file_path)
                    except Exception as e:
                        st.error(f"Failed on {uploaded_file.name}: {e}")
                    
                    # 4. Update Progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.success("✅ Batch processing complete!")

    # --- METHOD B: LOCAL FOLDER PATH (For huge datasets) ---
    elif ingest_type == "💻 Scan Local Folder Path":
        st.info("Paste the absolute path to a folder on your computer containing images.")
        folder_path = st.text_input("Folder Path", placeholder="C:/Users/Name/Pictures/Screenshots")
        
        if folder_path and os.path.isdir(folder_path):
            # Find all images in that folder
            valid_extensions = ('.png', '.jpg', '.jpeg', '.JPG', '.PNG')
            image_files = [f for f in os.listdir(folder_path) if f.endswith(valid_extensions)]
            
            st.write(f"Found **{len(image_files)}** images in this folder.")
            
            if len(image_files) > 0 and st.button("🧠 Ingest Folder"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, filename in enumerate(image_files):
                    full_path = os.path.join(folder_path, filename)
                    
                    # Update Status
                    status_text.text(f"Processing {i+1}/{len(image_files)}: {filename}...")
                    
                    try:
                        backend.ingest_screenshot(full_path)
                    except Exception as e:
                        st.error(f"Failed on {filename}: {e}")
                        
                    progress_bar.progress((i + 1) / len(image_files))
                
                status_text.success("✅ Folder ingestion complete!")
        elif folder_path:
            st.error("That path does not exist on this computer.")

# ==========================================
# TAB 2: SEARCH (Unchanged)
# ==========================================
with tab2:
    st.header("Search your Knowledge Base")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("What are you looking for?", placeholder="e.g., 'Receipt for sushi'")
    with col2:
        # Simple date filter toggle
        filter_date = st.date_input("Date", value=None)
        use_date_filter = st.checkbox("Filter by Date")
    
    if st.button("🔍 Search", type="primary"):
        if query:
            with st.spinner("Thinking..."):
                date_str = filter_date.strftime('%Y-%m-%d') if (use_date_filter and filter_date) else None
                
                results = backend.search_brain(query, date_str)
                
                if not results['ids'][0]:
                    st.warning("No matches found.")
                else:
                    # Display Loop
                    num_results = len(results['ids'][0])
                    for i in range(num_results):
                        file_path = results['ids'][0][i]
                        score = results['distances'][0][i]
                        metadata = results['metadatas'][0][i]
                        context = results['documents'][0][i]
                        
                        with st.container():
                            c1, c2 = st.columns([1, 3])
                            with c1:
                                if os.path.exists(file_path):
                                    st.image(file_path, width=150)
                                else:
                                    st.warning("Image missing")
                            with c2:
                                st.markdown(f"**Match {i+1}** (Score: {score:.4f})")
                                st.caption(f"📅 {metadata.get('date', 'Unknown')} | 📂 {file_path}")
                                with st.expander("See AI Description"):
                                    st.write(context)
                            st.divider()