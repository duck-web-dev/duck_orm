# Duck ORM

Duck ORM is a simple Object-Relational Mapping (ORM) library for SQLite, designed to ease the interaction between Python objects and an SQLite database. This lightweight library provides a basic structure for defining models and performing common database operations.

## File Structure

```plaintext
/duck_orm
|-- duck_orm
|   |-- __init__.py
|   |-- model.py
|   |-- database.py
|-- example_usage.py
|-- README.md
```

## Usage

### 1. Model Definition

Create your model by subclassing the `Model` class in `model.py` and defining the fields.

```python
# Example Model Definition
class User(Model):
    _fields = {'id': 'INTEGER PRIMARY KEY', 'username': 'TEXT', 'email': 'TEXT'}
```

### 2. Create Table

Use the `create_table` method to create the table in the database.

```python
# Example Table Creation
User.create_table()
```

### 3. Save Data

Instantiate your model, set the attributes, and use the `save` method to insert data into the database.

```python
# Example Data Insertion
new_user = User(username='john_doe', email='john@example.com')
new_user.save()
```

### 4. Retrieve Data

Use the `find` method to retrieve data based on specified conditions.

```python
# Example Data Retrieval
users = User.find(username='john_doe')
for user in users:
    print(user._data)
```

## Database Connection

The `Database` class in `database.py` handles database connections. It is used as a context manager to ensure proper handling of connections.

## Example Usage

Check `example_usage.py` for a quick overview of how to define models, create tables, save data, and retrieve data from the SQLite database using Duck ORM.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
