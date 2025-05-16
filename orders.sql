-- 业务数据表 orders，支持多租户隔离
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id VARCHAR(64) NOT NULL,
    region VARCHAR(32),
    amount INTEGER,
    status VARCHAR(16),
    score INTEGER,
    -- 其他业务字段
    INDEX idx_orders_tenant (tenant_id)
); 