#This script demonstrates basic CRUD operations with SQL commands on a PostgreSQL database for a blog API.
#It could be used instead of a traditional ORM (like SQLAlchemy) for lightweight applications.
#That being said I prefer SQLALchemy so we are sticking to it in the actual API.

import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(
        dbname="BlogAPI",
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Connected to the PostgreSQL database successfully.")
except Exception as e:
    print("Error connecting to the PostgreSQL database:")
    print(e)

###########################   
#Fetching all the entries from the blogs table
cursor.execute("SELECT * FROM public.blogs")
blogs = cursor.fetchall()
print(blogs)
############################

###################################
#Creating a new blog and adding it to the blogs table
new_blog = {
    "title": "My New Blog 4",
    "body": "This is the content of my new blog 4.",
}
cursor.execute("INSERT INTO public.blogs (title, body) VALUES (%s, %s) RETURNING *",
               (new_blog["title"], new_blog["body"]))
new_blog_id = cursor.fetchone()["id"]
conn.commit()

print(f"New blog created with ID: {new_blog_id}")
######################################

#################################
#Fetching one blog by its id
id = 1
cursor.execute("SELECT * FROM public.blogs WHERE id = %s", (id,))
blog = cursor.fetchone()
print(blog)

################################

###############################
#Deleting a blog by its id

id = new_blog_id  # Use the ID of the blog you want to delete
cursor.execute("DELETE FROM public.blogs WHERE id = %s RETURNING *", (id,))
deleted_blog = cursor.fetchone()
conn.commit()
print(f"Deleted blog: {deleted_blog}")

##############################


############################
#Updating a blog by its id

id = 2  # Use the ID of the blog you want to update
updated_blog = {
    "title": "My Updated Blog 2",
    "body": "This is the updated content of my blog 2.",
}
cursor.execute("UPDATE public.blogs SET title = %s, body = %s WHERE id = %s RETURNING *",
               (updated_blog["title"], updated_blog["body"], id))
updated_blog_data = cursor.fetchone()
conn.commit()
print(f"Updated blog: {updated_blog_data}")

###########################


# Ensure to close the connection when done
if cursor:
    cursor.close()
if conn:
    conn.close()