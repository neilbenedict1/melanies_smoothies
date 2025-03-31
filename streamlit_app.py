# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Convert dataframe to list for multiselect
my_dataframe = session.table('smoothies.public.fruit_options').select(col("FRUIT_NAME"))
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.to_pandas()["FRUIT_NAME"].tolist(),  # minimal necessary change
    max_selections=5
)

if ingredients_list:

    ingredients_string = ' '.join(ingredients_list)
    st.text(ingredients_string)

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('{ingredients_string}','{name_on_order}')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

