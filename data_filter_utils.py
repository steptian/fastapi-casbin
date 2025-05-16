import json
from sqlalchemy import and_, or_

def parse_filter(data_filter: str, table=None):
    """
    data_filter: JSON字符串，结构如 {"region": "华东", "amount": {">": 10000}, "and": [{...}, {...}]}
    table: SQLAlchemy Table对象，用于字段引用
    """
    if not data_filter or data_filter.strip() == "*" or data_filter.strip() == "":
        return None
    try:
        filter_dict = json.loads(data_filter)
    except Exception:
        raise ValueError("data_filter 不是合法的 JSON 格式")
    return _build_sqlalchemy_filter(filter_dict, table)

def _build_sqlalchemy_filter(filter_dict, table):
    # 递归构建 SQLAlchemy 表达式
    exprs = []
    for key, value in filter_dict.items():
        if key.lower() == "and":
            exprs.append(and_(*[_build_sqlalchemy_filter(v, table) for v in value]))
        elif key.lower() == "or":
            exprs.append(or_(*[_build_sqlalchemy_filter(v, table) for v in value]))
        elif isinstance(value, dict):
            for op, v in value.items():
                col = getattr(table.c, key)
                if op == "=":
                    exprs.append(col == v)
                elif op == ">":
                    exprs.append(col > v)
                elif op == "<":
                    exprs.append(col < v)
                elif op == ">=":
                    exprs.append(col >= v)
                elif op == "<=":
                    exprs.append(col <= v)
                elif op == "!=":
                    exprs.append(col != v)
                elif op.lower() == "in" and isinstance(v, list):
                    exprs.append(col.in_(v))
                else:
                    raise ValueError(f"不支持的操作符: {op}")
        else:
            col = getattr(table.c, key)
            exprs.append(col == value)
    return and_(*exprs) 