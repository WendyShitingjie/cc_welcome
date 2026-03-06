-- 测试表生成脚本
-- 数据库类型: adb
-- 表名: test_adb_demo
-- 数据类型: mixed
-- 数据行数: 20
-- 生成时间: 2026-01-29 16:57:32
-- 符合 MySQL 建表规范

CREATE TABLE IF NOT EXISTS test_adb_demo (
    id BIGINT NOT NULL COMMENT '主键ID',
    user_name VARCHAR(100) NOT NULL DEFAULT '' COMMENT '用户姓名',
    age INT NOT NULL DEFAULT 0 COMMENT '年龄',
    salary DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '薪资',
    birth_date DATE DEFAULT NULL COMMENT '出生日期',
    is_active TINYINT NOT NULL DEFAULT 1 COMMENT '是否激活',
    description TEXT COMMENT '详细描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    KEY idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ADB测试表';

INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (1, 'euiPUyqobIxzVCAH72Dn', 75, 70951837.45, 1, 'CnGvvWNlfbeACzdYxeSxKLWkZVQJjWbrCj6opVP46CRUFva7PuEyKYVPLrme19sfm7ITd7hAg6FYX88dBDUHS8c6S9VDX7J9yLqSUTNfOMkMo8BQYPre0ftR5MH3sJh6NplQSnwd6cOrVyDdFNVCQqSaSlMDcpybjzfHqiZ3mxoSh');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (2, 'SnrgpDFfapYD', 67, 55556636.03, 1, 'oCnTg5BZYeHaSVxwTitnCqC55M2RwCSP6k9t3x6ZMqYzmHiyBO50');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (3, '8M85eazV4V2', 78, 48999364.96, 1, 'muLxy4b299JTNwaNcMA3syHsXPwwr5Hm7Hnn7GdQ5fzl1OwLN1VzgoT0reRYKgfFeDaVf0WutZZ9Y5vRHm6DsMmwIAbX7J4BtnKQmtARxpjGX4G4nqEbQt4x4bSDdYdvEiqsczG');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (4, 'JIWCJr9xIZ6xeo', 60, 86069933.64, '2021-06-03', 1, 'FJ5zgwfM8laSCek79KfIH2uhaTypYuY4q7dGIYmUDH8JTtlgM7eRHvQblnVd6ZdeAzwksW31mjBclI61U63uoD9iHQTWRYZQFzPUC4Ma6Hy6DNUBofVXC5dS0TddaOK4Np6osSDW6ucJvZaG0A1aBXg2bjFiheD0AuxOYiNNDsJUC6Io71TEJy');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (5, 'MOxEYNbkBrwSh', 83, 89817583.13, '2023-01-22', 1, '0MD0BAmASEWObl0L4zkEFntA4G7gtejhWitFBRIclPpSJlnKvwzUXXM78BQlk');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (6, 'bUygs54', 98, 4082391.24, '2024-05-03', 1, 'BSM61UHPuatI2J3QcIV65s1hej8UnzmIqepkFQjyRyMYkhlEc0JkDd4cnu0c0ewr8');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (7, 'wlWkyCYUO2kd', 20, 64886387.67, 1, '7K3gEvDuydXzvFKIJz6vYfg6TCfl6nPkZWtmibDlaNfK0qZpPLkYJ6fP9OLon5fU7Adb1Ki0UTwQcSMFqniblUS01gd3UsvyeioTrZr59cQu2KN19JAiG2mQKAwjlIQ9OhpUw');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (8, 'b58BEuMMIg4D', 87, 42256520.74, 0, '6OioUF7ERpqJdAQyS5FpydvYOnlztRquhtCKSBXM2njsxQ8yMT991w95mdieRAWrFvmkH9bu73AMJNxiyjuNqxcwGGIx7pNvOq0fkUWV18fUfGBHXzSp0P4Dh5sVX6iU5pIVYT4tiFSorNnd6iTBReYyjGB9T');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (9, 'BrZeV', 29, 42653601.34, '2022-02-15', 1, '9UDEQ2CChpg3sFS0mXfS8QuZH7OEgtDStxxFGjQvV2JHmR0NkfrHOk2F7l1EVE9AWwhN7Ib4v3NHBULhJQeotgtfu7UIcVZF59FbRuIx4dCVzdrxW9GHKROYhummfykKLBEPhdieXeXLdNdDHfdrC8GC2Xgmln2RtgZQ');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (10, '5ifcZpS', 43, 24756299.72, 0, 'eMS5dfOD1tcBPsTrXk7Yhv6HhZyM0uKIWo6rLelNLBhw0XeVog0FldRYLErnRSf9bIyrMbuxQ4I8Ia5NOM9qTKifPrQGJC50ERu');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (11, 'PtFgKwFxiSo', 92, 74900282.91, '2021-02-11', 0, 'ZLGnnjFzBqUKjSe0IPQhNqyfS21KGbg4vIMsaKzM9S9DAAUBPZBQ3kB2uUDr641HSqDkjAVdcvc5k0B7B6SSDALLEANYNJjS7evaAw5USQngA5UuUcQyykpwoy1mCJxO66Oe5OFb');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (12, 'sd5Ij6sXP0EVBhGsHYh', 91, 48077863.79, 1, 'IiO0VXeLK6XTqJ9sHeR8ymx4QPUk6Sty1dQ3j3qYGIf1ajM88KKdHJaaZbvbG8UVm911a9flUKDbx9HEEcbtj4FE7tev1QnnoHyocyVGOPNa3NY3YCfb76TUxTVIh7bTUPHntt');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (13, 'KiKtq8Ne6zyWFtAo', 62, 16985400.44, 1, 'lcMfQAvx7lAopHKSNm1Xn4JhSv5mI07CehLcG4cJNxb59f0NFXN37GJuVXcnlioTYHPSfhZ8Ukb4IxllMnytIjDDJytNCcPKDY81dGqPUrCdtHxuBYFXlqhI5mzEbciNgoZbaTXemmsgW');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (14, 'T0eVgyoR', 85, 25222050.61, 0, 'KBIDxGLC6wVLBtUTerGgjKN8jEw9uUjXjihjtNb7K1BhpOnNRDG8JGKx4K3UcLtSTwGIJApZDO1f2cKm33Uo4');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (15, 'LCs2YZd3q4ekeyJqcIs', 11, 73849014.86, 0, 'BoWLwoDwhPt1SzQXefy03xHKlhBwpZ3eQckoLn5POmrCd8D0un42JtVga9b786qD4kTluc03rmoU6h1kJUlJjOZlfzPrAf8EaQr5i0fDWqsdpkWFSMWL5pSYp4c0ZZuE9naMTd0xCkXtDuWPGFFO2H05sTZkfk7Rc6ZGDNAlfXD14jbGodZaN92S2xlpbsPwvANt3n');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (16, 'Jeec8xRlogoFeBB8nI3M', 53, 1737026.77, 1, 'r9nxuCxK9UQfU7rnPonDodWamlR20JepLYO5d1swKV7HNvgqnkjbSvL1CHDBbAw89iu31D2QksnIdqgdVViCT3GgC2BINKQth0pAQ8c7');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (17, 'Lw6d6s0LIcP2USn', 80, 96057916.26, '2024-06-20', 0, 'MYAdz4crQDKP8P4rj7qKxPBK2ny1vBtZdGm8sucHHFlLKbbHCp603a5sKVnmV9aTB9shFNLuWESWLuozNWmpRgQCFMIpystVvnIL7tcxm7pM4r');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (18, 'oLaDYEYRSk3VFJWA', 27, 54811285.11, 0, 'G0MdYh6b2DoEdcjlxfEotog5YTKEGxOsSERbAh85cTGmcxivJdAmeXGeNcqNJQRFeutSVaP');
INSERT INTO test_adb_demo (id, user_name, age, salary, birth_date, is_active, description) VALUES (19, 'ty1FsgUhxmh64cUBBO18', 40, 63905754.02, '2021-10-05', 1, 'gSMMsabumJACx9rqq14HrPxfSDznavGF6r5Y8q1A1envz7px8VKX535AOkJWDWtIMHurh1T87PJOADwd1N8tEtqGsMfk07KSWvNnsDjMqY10z5Xp5dlmyDQWEdlCcubOWnmI8W35Jx');
INSERT INTO test_adb_demo (id, user_name, age, salary, is_active, description) VALUES (20, 'cXuFlWw74t1DNwrj44Lv', 70, 38215778.17, 0, 'x9UkN8gDFp3OLvHN8aigosD0OYOTWLgPGt0XbFRSX5EaP5ktFPqdxfyOdutXVA33b3bzQdeeM5oAMHLIK8oMOas0rQXI97T0RPeXaaisawEAU747diF8s1IfmcCDGFPAvBSsrJMt9qzuXAg');