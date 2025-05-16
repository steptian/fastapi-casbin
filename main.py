from fastapi import FastAPI, Depends, HTTPException
from casbin_dependency import casbin_dependency
from data_filter_utils import parse_filter
from sqlalchemy import create_engine, Table, MetaData, select

app = FastAPI()
DB_URL = 'sqlite:///casbin.db'
engine = create_engine(DB_URL)
metadata = MetaData()

# 假设有一个 orders 表
orders = Table('orders', metadata, autoload_with=engine)

# 用户模拟
class User:
    def __init__(self, username, tenant_id, org, data_ctx):
        self.username = username
        self.tenant_id = tenant_id
        self.org = org
        self.data_ctx = data_ctx

def get_current_user():
    # 实际项目应从 token/session 获取
    return User('alice', 'tenant1', 'orgA', {'region': '华东', 'amount': 12000})

@app.get('/orders')
def list_orders(user=Depends(get_current_user)):
    # 权限校验
    casbin_dependency(user.username, 'order', 'list', user.tenant_id, user.org, '*', data_ctx=user.data_ctx)()
    # 获取 data_filter（此处简化，实际应从策略中获取）
    data_filter = 'region == "华东" and amount > 10000'
    filter_expr = parse_filter(data_filter)
    with engine.connect() as conn:
        stmt = select(orders)
        if filter_expr is not None:
            stmt = stmt.where(filter_expr)
        result = conn.execute(stmt)
        return [dict(row) for row in result] 