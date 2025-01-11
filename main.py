import streamlit as st
import langchain_helper as l

# Set up the app title
st.title("Restaurant Name Generator")

# Sidebar for cuisine selection
cuisine = st.sidebar.selectbox(
    "Pick a cuisine",
    ("Select a cuisine", "Indian", "Mexican", "Chinese", "Italian", "Japanese", "French", "Korean")
)

# Initialize session state for response
if "response" not in st.session_state:
    st.session_state.response = {"rest_name": "Please select a cuisine", "menu_items": []}

# Fetch restaurant name and menu items when a valid cuisine is selected
if cuisine and cuisine != "Select a cuisine":
    if st.session_state.get("last_cuisine") != cuisine:
        # Update only if a new cuisine is selected
        st.session_state.response = l.get_rest_name_and_items(cuisine)
        st.session_state.last_cuisine = cuisine

# Display the restaurant name and menu items
response = st.session_state.response
st.header(response['rest_name'])
st.write("**Menu Items**")
for item in response["menu_items"]:
    st.write("-", item)
