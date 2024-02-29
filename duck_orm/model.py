from .db import Database


class Model:
    _db: Database
    _table_name: str
    _fields: dict

    def __init__(self, **kwargs):
        self._data = {}
        self.id = None  # Initialize id attribute
        for field, field_type in self._fields.items():
            value = kwargs.get(field, None)
            setattr(self, field, value)  # Set the attribute
            self._validate_and_set(field, field_type, value)

    def _validate_and_set(self, field, field_type, value):
        if field_type == "text" and not isinstance(value, str):
            raise ValueError(f"Field '{field}' must be a string.")
        elif field_type == "number" and not isinstance(value, (int, float)):
            raise ValueError(f"Field '{field}' must be a number.")
        # Add more field types as needed

        self._data[field] = value

    def _save(self):
        if not self._table_name or not self._fields:
            raise ValueError("Table name and fields must be defined in the Model subclass.")

        if not self.id:
            fields = ', '.join(self._data.keys())
            values = ', '.join([f'"{value}"' for value in self._data.values()])
            insert_query = f"INSERT INTO {self._table_name} ({fields}) VALUES ({values})"
            self._db.execute_query(insert_query)
            self.id = self._db.cursor.lastrowid
        else:
            update_fields = ', '.join([f'{key}="{value}"' for key, value in self._data.items()])
            update_query = f"UPDATE {self._table_name} SET {update_fields} WHERE id={self.id}"
            self._db.execute_query(update_query)

    @classmethod
    def create_table(cls):
        if not cls._table_name or not cls._fields:
            raise ValueError("Table name and fields must be defined in the Model subclass.")

        fields_str = ', '.join([f'{field} {field_type.upper()}' for field, field_type in cls._fields.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {cls._table_name} (id INTEGER PRIMARY KEY, {fields_str})"
        cls._db.execute_query(create_table_query)

    @classmethod
    def select(cls, **kwargs):
        if not cls._table_name or not cls._fields:
            raise ValueError("Table name and fields must be defined in the Model subclass.")

        conditions = ' AND '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        select_query = f"SELECT * FROM {cls._table_name} WHERE {conditions}"
        result = cls._db.fetch_query(select_query)

        if not result:
            return None

        instance = cls()
        instance.id = result[0][0]
        for i, (field, field_type) in enumerate(cls._fields.items()):
            setattr(instance, field, result[0][i + 1])
            instance._validate_and_set(field, field_type, result[0][i + 1])

        return instance

    @classmethod
    def select_all(cls, **kwargs):
        if not cls._table_name or not cls._fields:
            raise ValueError("Table name and fields must be defined in the Model subclass.")

        conditions = ' AND '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        where_clause = f" WHERE {conditions}" if conditions else ""
        select_all_query = f"SELECT * FROM {cls._table_name}{where_clause}"
        results = cls._db.fetch_query(select_all_query)

        instances = []
        for result in results:
            instance = cls()
            instance.id = result[0]
            for i, (field, field_type) in enumerate(cls._fields.items()):
                setattr(instance, field, result[i + 1])
                instance._validate_and_set(field, field_type, result[i + 1])
            instances.append(instance)

        return instances
