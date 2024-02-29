from duck_orm.db import Database
from duck_orm.model import Model

# Create a Database instance
db_instance = Database("example.db")

# Create a Model subclass
class Person(Model):
    _db = db_instance
    _table_name = "persons"
    _fields = {"name": "text", "age": "number", "city": "text"}

# Create the table
Person.create_table()

# Create and save a Person instance
john = Person(name="John Doe", age=25, city="New York")
john._save()

# Edit and save the instance
john.age = 26
john.city = "Los Angeles"
john._save()

# Access the id attribute
print(f"John's ID: {john.id}")

# Select a Person instance by ID
john_from_db = Person.select(id=1)
print(john_from_db.name, john_from_db.age, john_from_db.city)

# Select all Person instances with a specific condition
all_johns = Person.select_all(name="John Doe")
for person in all_johns:
    print(person.id, person.name, person.age, person.city)

# Close the database connection
db_instance.close_connection()
