from loguru import logger
from datetime import datetime

logger.add('audit.log', level='INFO', rotation='10 MB', retention='10 days')
# 日志告警示例：如需邮件告警，取消注释并配置邮箱
# logger.add(
#     'smtp://user:password@smtp.example.com',
#     level='ERROR',
#     format='{time} {level} {message}',
#     subject='[Casbin权限系统] 错误告警',
#     to='ops@example.com'
# )

def log_policy_change(action, policy):
    logger.info(f"[{datetime.now()}] POLICY_CHANGE: {action} {policy}")

def log_permission_check(user, obj, act, result, detail=None):
    logger.info(f"[{datetime.now()}] PERMISSION_CHECK: user={user}, obj={obj}, act={act}, result={result}, detail={detail}") 