# Contents of ~/my_app/streamlit_app.py
import streamlit as st
import pandas as pd

df = pd.read_excel("data/forumvision.xlsx")

def main_page():
    st.markdown("# Forumvision - full table")
    st.sidebar.markdown("# Forumvision - full table")

    st.dataframe(df.head(200))


# def page2():
#     st.markdown("# Page 2 ❄️")
#     st.sidebar.markdown("# Page 2 ❄️")


# def page3():
#     st.markdown("# Page 3 🎉")
#     st.sidebar.markdown("# Page 3 🎉")

# page_names_to_funcs = {
#     "Main Page": main_page,
#     "Page 2": page2,
#     "Page 3": page3,
# }

# selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
# page_names_to_funcs[selected_page]()

if __name__ == "__main__":
    main_page()

    
