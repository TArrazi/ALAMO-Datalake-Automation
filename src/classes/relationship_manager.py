from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Field:
    name: str
    d_type: str


class Table:

    @staticmethod
    def _get_fields(metadata: Dict) -> List[Field]:
        return [
            Field(name=d.get('name'), d_type=d.get('d_type')) for d in metadata.get('fields')
        ]

    @staticmethod
    def _get_table_name(metadata: Dict) -> str:
        return metadata.get('table')

    @staticmethod
    def _get_schema_name(metadata: Dict) -> str:
        return metadata.get('schema')

    def __init__(self, metadata: Dict, db: str) -> None:
        self.fields = self._get_fields(metadata)
        self.name = self._get_table_name(metadata)
        self.schema = self._get_schema_name(metadata)
        self.db = db

    def __rshift__(self, o):
        if isinstance(o, type(self)):
            return Relationship(self, o)
        else:
            raise TypeError(f'Mismatched types: "{type(self)}" >> "{type(o)}"')

    def __str__(self):
        return f'{self.schema}.{self.name}'


class Relationship:
    @dataclass
    class Pair:
        from_: Field
        to_: Field

    def __init__(self, tb_l, tb_r) -> None:
        self.tb_l = tb_l
        self.tb_r = tb_r
        self.transforms = self.infer_transforms(self.tb_r)

    def __str__(self):
        return f'({str(self.tb_l)} >> {str(self.tb_r)})'

    def __rshift__(self, o):
        if isinstance(o, Table):
            return Relationship(self, o)

    def _infer_fields_relationship(self):
        pairs = list()

        for f_l in self.tb_l.fields:
            for f_r in self.tb_r.fields:
                if f_l.name.lower() == f_r.name.lower():
                    pairs.append(self.Pair(f_l, f_r))

        return pairs

    def infer_transforms(self, o, cast_method='try_cast'):
        if isinstance(self.tb_l, Relationship):
            return self.tb_l.infer_transforms(o)
        else:
            pairs = self._infer_fields_relationship()
            return self._make(pairs, cast_method)

    @staticmethod
    def _make(pairs, cast_method):
        return [
            f'{cast_method}({p.from_.name} as {p.to_.d_type}) as {p.to_.name}'
            if p.from_.d_type != p.to_.d_type
            else f'{p.from_.name}'
            for p in pairs
        ]
