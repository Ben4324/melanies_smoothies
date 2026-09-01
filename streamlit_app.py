import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

session = get_active_session()

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# No col import required
fruit_options_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select("FRUIT_NAME")
    .to_pandas()
)

fruit_options = fruit_options_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options,
    max_selections=5
)

if ingredients_list and name_on_order.strip():
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        # Parameter binding avoids SQL injection and handles apostrophes safely
        insert_sql = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
        """

        session.sql(
            insert_sql,
            params=[ingredients_string, name_on_order.strip()]
        ).collect()

        st.success("Your Smoothie is ordered! ✅")

elif ingredients_list and not name_on_order.strip():
    st.warning("Please enter a name for the smoothie.")
