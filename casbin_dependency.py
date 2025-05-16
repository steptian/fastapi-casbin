from fastapi import Depends, HTTPException
from enforcer import get_enforcer
from audit_log import log_permission_check

def casbin_dependency(sub, obj, act, tenant, org="*", data_id="*", data_ctx=None):
    def checker():
        enforcer = get_enforcer()
        # 获取所有匹配的策略
        policies = enforcer.get_filtered_policy(0, sub, obj, act, tenant)
        for p in policies:
            # 判断有效期
            expire_at = p[8] if len(p) > 8 else "*"
            if expire_at != "*":
                from datetime import datetime
                if datetime.now() > datetime.fromisoformat(expire_at):
                    continue
            # 判断数据范围
            data_filter = p[7] if len(p) > 7 else "*"
            if data_filter != "*" and data_ctx is not None:
                if not eval_data_filter(data_filter, data_ctx):
                    continue
            # 通过
            log_permission_check(sub, obj, act, True, f"tenant={tenant}, org={org}, data_id={data_id}")
            return
        # 失败时记录详细日志
        log_permission_check(sub, obj, act, False, f"tenant={tenant}, org={org}, data_id={data_id}, ctx={data_ctx}")
        raise HTTPException(status_code=403, detail="无权限")
    return checker

def eval_data_filter(data_filter, data_ctx):
    # 简单实现：data_filter 是 Python 表达式，data_ctx 是 dict
    # 生产环境建议用更安全的表达式解析库
    try:
        return eval(data_filter, {}, data_ctx)
    except Exception:
        return False 