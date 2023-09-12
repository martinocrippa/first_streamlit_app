#libs
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healty Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# read data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New Section to diplay fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   if not fruit_choice:
       streamlit.error('Please select a fruit to get inormation.')
   else:
       # get data from api
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
       # streamlit.text(fruityvice_response.json())  # just write data to screen
       # write your own comment -what does the next line do? 
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   
       # write your own comment - what does this do?
       streamlit.dataframe(fruityvice_normalized)
     
except URLError as e:
    streamlit.error()

# don0t run anything past here while we troibleshoot
streamlit.stop()

# snowflake connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# New Section add a second text box entry
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# this will not work correctly, but just go with it for now
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit')")
