import casbin
from casbin_sqlalchemy_adapter import Adapter
import os

MODEL_CONF_PATH = os.path.join(os.path.dirname(__file__), 'model.conf')
DB_URL = os.getenv('CASBIN_DB_URL', 'sqlite:///casbin.db')

_enforcer = None

def get_enforcer():
    global _enforcer
    if _enforcer is None:
        adapter = Adapter(DB_URL)
        _enforcer = casbin.Enforcer(MODEL_CONF_PATH, adapter)
        _enforcer.load_policy()  # 确保策略热加载
    return _enforcer 