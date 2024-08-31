import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Set up connection parameters using Streamlit secrets
connection_parameters = {
    "account": "LKMLPQZ-LF57785",
    "user": "KARTHIKALLU",
    "password": "Ishan@2016",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "client_session_keep_alive": True
}

# Initialize the Snowflake session
try:
    session = Session.builder.configs(connection_parameters).create()
    st.success("Connected to Snowflake successfully!")
except Exception as e:
    st.error(f"Failed to connect to Snowflake: {e}")

# Streamlit app UI
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits to customize your own Smoothie"""
)

# User input for name on order
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Fetch fruit options from the Snowflake table
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
    st.dataframe(data=my_dataframe, use_container_width=True)
except Exception as e:
    st.error(f"Error fetching fruit options: {e}")

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    
    # SQL Insert statement for the order
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""
    
    st.write(my_insert_stmt)
    
    # Button to submit the order
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Failed to submit order: {e}")
if ingredients_list:
    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "
    st.subheader(fruit_chosen + " Nutrition Information")
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

