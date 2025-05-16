-- Casbin 策略表结构设计，支持多租户、临时授权、数据范围
CREATE TABLE casbin_rule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ptype VARCHAR(10) NOT NULL,
    sub VARCHAR(64),
    obj VARCHAR(64),
    act VARCHAR(32),
    tenant VARCHAR(64),
    org VARCHAR(64),
    data_id VARCHAR(64),
    data_filter TEXT,
    expire_at DATETIME,
    -- 可根据实际需要添加更多字段
    INDEX idx_casbin_rule_main (ptype, sub, obj, act, tenant, org, data_id)
); 