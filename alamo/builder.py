import logging
import traceback

from .relationship_manager import Relationship


class Builder:

    _TEMPLATE = """
insert into {}.{}.{}
select
{}
from {}.{}.{}
"""

    def __enter__(self):
        return self

    def __call__(self, *args, **kwargs):
        self.update(kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            return 0
        logging.fatal(f'Exception raised: {exc_type}')
        logging.fatal(f'Exception value: {exc_val}')
        traceback.print_tb(exc_tb)
        return -1

    def __init__(self, relationship):
        self._nested_relationships = relationship
        self.relationships = self._flatten_relationships()

    def _flatten_relationships(self):

        flattened_relationships = list()

        def _flatten(relationship):

            if isinstance(relationship.tb_l, Relationship):
                flattened_relationships.append(Relationship(relationship.tb_l.tb_r, relationship.tb_r))
                _flatten(relationship.tb_l)
            else:
                flattened_relationships.append(relationship)

            return reversed(flattened_relationships)

        return _flatten(self._nested_relationships)

    def build_queries(self):

        queries = [
            self._TEMPLATE.format(
                rel.tb_r.db,
                rel.tb_r.schema,
                rel.tb_r.name,
                ',\n'.join(rel.transforms),
                rel.tb_l.db,
                rel.tb_l.schema,
                rel.tb_l.name
            )
            for rel in self.relationships
        ]

        return queries
