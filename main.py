import streamlit as st
import langchain_helper as l

st.title("Restaurant Name Generator")
cuisine = st.sidebar.selectbox("Pick a cuisine", ("Indian", "Mexican", "Chinese", "Italian", "Japanese", "French", "Korean"))

if cuisine:
    response = l.get_rest_name_and_items(cuisine)
    st.header(response['rest_name'])
    menu_items = response["menu_items"]
    st.write("**Menu Items**")
    for i in menu_items:
        st.write("-", i)
