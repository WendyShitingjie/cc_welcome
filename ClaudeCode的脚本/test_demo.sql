-- 测试表生成脚本
-- 数据库类型: mysql
-- 表名: test_save_file
-- 数据类型: mixed
-- 数据行数: 5
-- 生成时间: 2026-01-28 20:37:30
-- 符合 MySQL 建表规范

CREATE TABLE IF NOT EXISTS test_save_file (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    user_name VARCHAR(100) NOT NULL DEFAULT '' COMMENT '用户姓名',
    age INT NOT NULL DEFAULT 0 COMMENT '年龄',
    salary DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '薪资',
    birth_date DATE DEFAULT NULL COMMENT '出生日期',
    is_active TINYINT NOT NULL DEFAULT 1 COMMENT '是否激活',
    description TEXT COMMENT '详细描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    KEY idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='test_save_file测试表';

INSERT INTO test_save_file (user_name, age, salary, is_active, description) VALUES ('bdjC9B83ns4ECEv', 83, 68205974.72, 0, 'l3rVjoadeeznpPglHwFwOOrpXMXTAEelcPYU0Ebk3K6cGEdEuDGmnxEcnH98XG4BbqHnMyGftrqmZOKwoQV5jsOARL0RUgqjuCqwhd3QPVmfQ6NnfXggOJFwx7DdgXAEyaVn7RBuyeS');
INSERT INTO test_save_file (user_name, age, salary, birth_date, is_active, description) VALUES ('GPxvsA5', 9, 80948462.07, '2022-01-08', 0, 'bXtwmAjzIkHz6TVXIH1TNJVPAy7tc33c92U2KmFK9vbBG1fgNqg');
INSERT INTO test_save_file (user_name, age, salary, is_active, description) VALUES ('gazi90vR8B7giRVAxee', 58, 54737356.12, 1, 'UNOqQY02SRQaFTcpgpzXxwbi0IW7VgdB9bPoteh3pUAdbb3gDAieoQ95RJYoAyRSQqT');
INSERT INTO test_save_file (user_name, age, salary, birth_date, is_active, description) VALUES ('uja7WWwBNCurloL', 73, 52172160.44, '2023-08-30', 0, 'cwTLtTvzXbMXvykvWTtbThm9wgWG6kbmXcCHTu7NhP1Ouh0c391kw1RVz1CtkfeG');
INSERT INTO test_save_file (user_name, age, salary, birth_date, is_active, description) VALUES ('XGPs8ODYkUsMp', 56, 64551485.21, '2022-08-27', 0, 'nKyk3yWqYu8yloSZ4UTj9hWtyuh1RHz2NQlGPdrOYlMda4o5Q4PIyt1N5EArelS37wsmhIbz3YNDud7KEttzbEhYbWeYk4VMIw4AsPEg5CctkkoG3MBeXjN');