from classes.relationship_manager import Table
from classes.builder import Builder


raw_table_meta = {
    'schema': 'raw',
    'table': 'people',
    'fields': [
        {'name': 'id', 'd_type': 'varchar'},
        {'name': 'full_name', 'd_type': 'varchar'},
        {'name': 'age', 'd_type': 'varchar'}
    ]
}

trusted_table_meta = {
    'schema': 'trusted',
    'table': 'people',
    'fields': [
        {'name': 'id', 'd_type': 'integer'},
        {'name': 'full_name', 'd_type': 'varchar'},
        {'name': 'age', 'd_type': 'integer'}
    ]
}

service_table_meta = {
    'schema': 'service',
    'table': 'people',
    'fields': [
        {'name': 'id', 'd_type': 'integer'},
        {'name': 'full_name', 'd_type': 'varchar'},
        {'name': 'age', 'd_type': 'integer'}
    ]
}

db = 'hive'

raw_table = Table(metadata=raw_table_meta, db=db)
trusted_table = Table(metadata=trusted_table_meta, db=db)
service_table = Table(metadata=service_table_meta, db=db)

relationship = raw_table >> trusted_table >> service_table

with Builder(relationship=relationship) as b:

    queries = b.build_queries()
    for q in queries:
        print(q)
