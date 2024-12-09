import streamlit as st
import requests

# Set page configuration at the top of the script
st.set_page_config(page_title="Ice Cream Shop", layout="wide")

# Define API base URL
API_URL = "http://127.0.0.1:5000"

# Function to fetch flavors from the API
def fetch_flavors():
    response = requests.get(f"{API_URL}/flavors")
    if response.status_code == 200:
        return response.json()
    return []

# Function to check if search_query is a subsequence of flavor_name
def is_subsequence(query, flavor_name):
    it = iter(flavor_name.lower())
    return all(char in it for char in query.lower())

# Function to add a new flavor
def add_flavor(flavor_name):
    response = requests.post(f"{API_URL}/add_flavor", json={"name": flavor_name})
    return response.json()

# Function to add an allergen
def add_allergen(allergen_name, flavor_id):
    response = requests.post(f"{API_URL}/add_allergen", json={"name": allergen_name, "flavor_id": flavor_id})
    return response.json()

# Initialize session state for shopping cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Streamlit application UI
st.sidebar.title("🍦 Ice Cream Shop")
sidebar_option = st.sidebar.radio(
    "",
    ["Search Flavors", "Add Flavor", "Add Allergen", "Shopping Cart"]
)

# Catchy title with icons
st.markdown("""
    <div style="text-align: center; color: #FF6347; font-size: 48px; font-weight: bold;">
        Welcome to the Ice Cream Shop! 🍨 🍨 🍨
    </div>
    <div style="text-align: center; font-size: 24px; color: #FF4500;">
        The place for all your sweet cravings! 🍧
    </div>
""", unsafe_allow_html=True)

# Search for Flavors Section
if sidebar_option == "Search Flavors":
    st.header("🔍 Search for Flavors")

    search_query = st.text_input("Enter flavor name:")
    if st.button("Search"):
        if search_query:
            flavors = fetch_flavors()  # Fetch all flavors
            matching_flavors = [flavor for flavor in flavors if is_subsequence(search_query, flavor['name'])]
            
            if matching_flavors:
                st.write(f"### Found {len(matching_flavors)} matching flavor(s):")
                for flavor in matching_flavors:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Flavor ID:** {flavor['id']}<br>**Name:** {flavor['name']}", unsafe_allow_html=True)
                    with col2:
                        if st.button("🛒 Add to Cart", key=f"add_to_cart_{flavor['id']}"):
                            if flavor['id'] not in st.session_state.cart:
                                st.session_state.cart.append(flavor['id'])
                                st.success(f"Flavor ID {flavor['id']} added to cart.")
                            else:
                                st.warning(f"Flavor ID {flavor['id']} is already in your cart.")
            else:
                st.warning("No flavors found matching your search.")
        else:
            st.warning("Please enter a flavor name to search.")

# Add a New Flavor Section
elif sidebar_option == "Add Flavor":
    st.header("➕ Add a New Flavor")

    new_flavor_name = st.text_input("New Flavor Name:")
    if st.button("Add Flavor"):
        if new_flavor_name:
            result = add_flavor(new_flavor_name)
            st.success(result.get("message", "Flavor added successfully!"))
        else:
            st.error("Flavor name cannot be empty.")

# Add Allergen Section
elif sidebar_option == "Add Allergen":
    st.header("⚠️ Add Allergen")

    allergen_name = st.text_input("Allergen Name:")
    selected_flavor_id = st.number_input("Flavor ID:", min_value=1)
    if st.button("Add Allergen"):
        if allergen_name and selected_flavor_id:
            result = add_allergen(allergen_name, selected_flavor_id)
            st.success(result.get("message", "Allergen added successfully!"))
        else:
            st.error("Allergen name and Flavor ID cannot be empty.")

# Shopping Cart Section
elif sidebar_option == "Shopping Cart":
    st.header("🛒 Shopping Cart")

    # Input field for adding a flavor by ID
    new_cart_item_id = st.number_input("Enter Flavor ID to Add to Cart:", min_value=1)
    
    if st.button("Add to Cart"):
        if new_cart_item_id not in st.session_state.cart:
            st.session_state.cart.append(new_cart_item_id)
            st.success(f"Flavor ID {new_cart_item_id} added to cart!")
        else:
            st.warning(f"Flavor ID {new_cart_item_id} is already in your cart.")
    
    # Display current items in the cart
    if len(st.session_state.cart) > 0:
        cart_items = set(st.session_state.cart)
        st.write("### Items in Your Cart:")
        for item in cart_items:
            st.write(f"Flavor ID: **{item}**")
    else:
        st.info("Your cart is empty.")
