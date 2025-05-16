from loguru import logger
from datetime import datetime

logger.add('audit.log', level='INFO', rotation='10 MB', retention='10 days')

def log_policy_change(action, policy):
    logger.info(f"[{datetime.now()}] POLICY_CHANGE: {action} {policy}")

def log_permission_check(user, obj, act, result, detail=None):
    logger.info(f"[{datetime.now()}] PERMISSION_CHECK: user={user}, obj={obj}, act={act}, result={result}, detail={detail}") 