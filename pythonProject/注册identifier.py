#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector

conn = mysql.connector.connect(host='cjjarch.db.ali-bj-sit01.shuheo.net', port=3306, user='featurehub',
                               password='lohSh6Ya', charset='utf8')
cursor = conn.cursor()

cursor.execute("""INSERT INTO featurehub.ecube_identifier_update
(identifier, insert_ck_time, created_at, updated_at, cluster)
VALUES
('off_usr_iso_sex', now(), now(), now(), 'clickhouse-ha'),
('off_usr_iso_age', now(), now(), now(), 'clickhouse-ha'),
('clc_usr_reg_mob_new', now(), now(), now(), 'clickhouse-ha'),
('off_usr_reg_mob_new', now(), now(), now(), 'clickhouse-ha'),
('off_usr_grp_sta_dte', now(), now(), now(), 'clickhouse-ha'),
('off_usr_user_level_channel', now(), now(), now(), 'featurestore-ha'),
('off_usr_user_level_marketing', now(), now(), now(), 'featurestore-ha'),
('off_usr_user_level_product_cd', now(), now(), now(), 'featurestore-ha'),
('rt_usr_account_id13', now(), now(), now(), 'featurestore-ha'),
('off_usr_born_date1', now(), now(), now(), 'featurestore-ha'),
('rt_demo_phn', now(), now(), now(), 'featurestore-ha')""")
conn.commit()
cursor.close()
conn.close()