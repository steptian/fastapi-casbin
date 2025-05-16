from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
import json

DB_URL = 'sqlite:///casbin.db'
engine = create_engine(DB_URL)
metadata = MetaData()
casbin_rule = Table('casbin_rule', metadata, autoload_with=engine)

router = APIRouter(prefix="/policy", tags=["policy"])

class PolicyIn(BaseModel):
    ptype: str
    sub: str
    obj: str
    act: str
    tenant: str
    org: Optional[str] = '*'
    data_id: Optional[str] = '*'
    data_filter: Optional[Any] = '*'
    expire_at: Optional[str] = '*'

    @validator('data_filter', pre=True, always=True)
    def validate_data_filter(cls, v):
        if v == '*' or v is None:
            return v
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                raise ValueError('data_filter 必须为合法 JSON')
        # 结构化校验，可扩展字段白名单
        if not isinstance(v, dict):
            raise ValueError('data_filter 必须为对象')
        return json.dumps(v, ensure_ascii=False)

class PolicyOut(PolicyIn):
    id: int

@router.get('/', response_model=List[PolicyOut])
def list_policies(skip: int = 0, limit: int = 20):
    with engine.connect() as conn:
        stmt = select(casbin_rule).offset(skip).limit(limit)
        result = conn.execute(stmt)
        return [dict(row) for row in result]

@router.post('/', response_model=PolicyOut)
def create_policy(policy: PolicyIn):
    with engine.connect() as conn:
        stmt = insert(casbin_rule).values(**policy.dict())
        res = conn.execute(stmt)
        policy_id = res.lastrowid
        stmt2 = select(casbin_rule).where(casbin_rule.c.id == policy_id)
        return dict(conn.execute(stmt2).first())

@router.put('/{policy_id}', response_model=PolicyOut)
def update_policy(policy_id: int, policy: PolicyIn):
    with engine.connect() as conn:
        stmt = update(casbin_rule).where(casbin_rule.c.id == policy_id).values(**policy.dict())
        res = conn.execute(stmt)
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail='Policy not found')
        stmt2 = select(casbin_rule).where(casbin_rule.c.id == policy_id)
        return dict(conn.execute(stmt2).first())

@router.delete('/{policy_id}')
def delete_policy(policy_id: int):
    with engine.connect() as conn:
        stmt = delete(casbin_rule).where(casbin_rule.c.id == policy_id)
        res = conn.execute(stmt)
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail='Policy not found')
        return {"ok": True} 