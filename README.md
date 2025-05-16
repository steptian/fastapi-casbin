# FastAPI + Casbin 多租户/临时授权/数据范围权限方案说明

## 1. 权限模型与表结构
- 采用 Casbin，支持多租户（tenant）、临时授权（expire_at）、数据范围（data_filter）等字段。
- 策略表 casbin_rule 字段：ptype, sub, obj, act, tenant, org, data_id, data_filter, expire_at。
- model.conf 支持多维度匹配与通配符。

## 2. Enforcer 初始化与依赖注入
- 通过 enforcer.py 的 get_enforcer() 工厂方法，自动加载 model.conf 和数据库策略。
- FastAPI 权限依赖 casbin_dependency，支持多租户、临时授权、数据范围上下文参数。

## 3. 路由集成与数据范围过滤
- 路由中通过 Depends 注入权限校验。
- data_filter 支持表达式，结合 parse_filter 工具转为 SQLAlchemy 查询条件，实现数据范围过滤。

## 4. 临时授权与定时任务
- 策略支持 expire_at 字段，权限依赖和 Celery 定时任务均可自动失效和清理过期策略。

## 5. 日志与审计
- 所有策略变更、权限校验结果通过 audit_log.py 记录到 audit.log，便于合规追溯。

## 6. 扩展建议
- 可开发策略管理后台，支持策略的增删改查、批量导入导出、临时授权、审批等。
- data_filter 建议用更安全的表达式解析库。
- 可扩展更多维度（如环境、时间、IP等），只需扩展 model.conf 和 policy 字段。 