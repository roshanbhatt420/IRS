import streamlit as st

# defining pages
main_pages = st.Page("main.py", title="Home ", icon="🏠")
Upload_page = st.Page("chat.py", title="Try It ! ", icon="📤"   )

# setign navigation
st.sidebar.title("Navigation")
page = st.navigation([main_pages, Upload_page])
page.run()
