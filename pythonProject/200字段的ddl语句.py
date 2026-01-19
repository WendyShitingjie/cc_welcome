import sys

original_ddl = """CREATE TABLE `lyf_instance_test_copy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `created_by` varchar(45) DEFAULT NULL COMMENT '创建人',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` varchar(45) DEFAULT NULL COMMENT '更新人',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `bucket_name` varchar(100) NOT NULL COMMENT 'ss这是一个注释',
  PRIMARY KEY (`id`),
  KEY `idx_updated_at` (`updated_at`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实例映射测试';"""

# 生成240个测试字段（原表已有6个字段）
new_columns = []
for i in range(1, 241):
    col = f"  `test_col_{i:03}` varchar(20) DEFAULT NULL COMMENT '压力测试字段{i}'"
    new_columns.append(col)

full_ddl = original_ddl.replace(");", ",\n" + ",\n".join(new_columns) + "\n);")

print(full_ddl)