# get the user input from index site and turn it into a variable
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html")
print()   
print("<TITLE>CGI script output</TITLE>")
selected_neighborhood = str(form["neighborhood"].value)

### definition of function for creating a list of strings in html
def print_ul(elements):
    print("<ul>")
    for element in elements:
        ul= "<li>"+str(element)+"</li>"
        print(ul)
    print("</ul>")


# import the python library for SQLite 
import sqlite3

# connect to the database file, and create a connection object
db_connection = sqlite3.connect('restaurants.db')

# create a database cursor object, which allows us to perform SQL on the database. 
db_cursor = db_connection.cursor()

# run a query combining restaurants with neighborhood
db_cursor.execute("SELECT restaurants.NAME, neighborhoods.NAME from restaurants INNER JOIN neighborhoods on restaurants.NEIGHBORHOOD_ID=neighborhoods.ID")

# store the result in a local variable. 
list_restaurants = db_cursor.fetchall()

# convert list of tuple into dictionary
dict_restaurant=dict(list_restaurants)


list_of_neighborhood =[]

print("""
    <!DOCTYPE html>
    <h1>""")  
print(f"These are restaurants in {selected_neighborhood.title()}:")
print("""
    </h1>
    <h2>""")
final_list = []
for key, value in dict_restaurant.items():
    if value == selected_neighborhood:
        final_list.append(key)
# calling the function
print_ul(final_list)
print("""
    </h2>   
    </html>
    """)  
