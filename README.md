# ALAMO-Datalake-Automation (WIP)
#
- PT-BR: Uma ferramenta simples para ajudar com tarefas repetitivas de tipagem quando construindo queries entre camadas (RAW, TRUSTED, SERVICE)
- EN-US: A simple tool to aid in repetitive field typing tasks when building queries between layers (RAW, TRUSTED, SERVICE).
###
- PT-BR: No momento, esta ferramenta constrói automaticamente as queries de tipagem de campos entre as camadas RAW e TRUSTED em um Data Lake.
- EN-US: At the moment, this tool automatically builds field typing queries between the RAW and TRUSTED layers in a Data Lake.

## Installation
```
git clone https://github.com/TArrazi/ALAMO-Datalake-Automation.git
cd ALAMO-Datalake-Automation
python setup.py install
```

## How to use
```python
from alamo.builder import Builder
from alamo.relationship_manager import Table


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

with Builder(relationship) as builder:

    queries = builder.build_queries()

    for q in queries:
        print(q)
```

### OUTPUT
```
insert into hive.trusted.people
select
try_cast(id as integer) as id,
full_name,
try_cast(age as integer) as age
from hive.raw.people


insert into hive.service.people
select
id,
full_name,
age
from hive.trusted.people
```

#### Note
This tools works strictly with standard SQL queries and currently does not require/support database connections.