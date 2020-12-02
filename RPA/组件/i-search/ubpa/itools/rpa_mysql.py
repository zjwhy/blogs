#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import uuid
import time
import datetime

def excute_db(host, username, pwd, tablename, sql, flag, param=None, port=3306):
   result = None
   try:
      db = MySQLdb.connect(host, username, pwd, tablename, port, charset="utf8")
      cursor = db.cursor()
      if "select_all" == flag:

         cursor.execute(sql)
         result = cursor.fetchall()
      if "insert_many" == flag:

         for i in range(len(sql)):
            result = cursor.executemany(sql[i], param[i])

      db.commit()
   except Exception as e:
      db.rollback()
   finally:
      db_close(db)
      return result


def db_close(db):

   try:
      db.close()
   except Exception as e:
      raise e


def deal_usertable(host, username, pwd, tablename):

   try:
      sql = "SELECT userEmail, userName, userPassword, ddId FROM symphony_user"

      user_list = excute_db(host, username, pwd, tablename, sql, "select_all")

      return user_list
   except Exception as e:
      raise e


def deal_cust_logintable(host, username, pwd, tablename):

   try:
      sql = "SELECT CUST_MAIL FROM t_cust_login"

      custlogin_list = excute_db(host, username, pwd, tablename, sql, "select_all")

      return custlogin_list

   except Exception as e:
      raise e

def compare_data(user_list, custlogin_list):
   '''
   :param user_list:
   :param custlogin_list:
   :return: 筛选出user_list有  custlogin_list没有的数据
   '''
   u_list = []
   c_list = []
   new_cl_list = []
   new_ci_list = []
   new_so_list = []

   for index_user in user_list:
      if '' != index_user[0]:
         u_list.append(index_user[0])

   for index_custlogin in custlogin_list:
      if '' != index_custlogin[0]:
         c_list.append(index_custlogin[0])

   uc_list = list(set(u_list).difference(set(c_list)))
   now_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

   now_time = datetime.datetime.now().strftime('%H:%M:%S')
   days_after = datetime.date.today() + datetime.timedelta(days=30)
   order_time = str(days_after) + " " + now_time

   for index_uc in uc_list:

      for index_user in user_list:
         if index_uc == index_user[0]:

            uuid_id1 = str(uuid.uuid1())
            uuid_id1 = uuid_id1.split('-')
            uuid_id1 = ''.join(uuid_id1)

            uuid_id2 = str(uuid.uuid1())
            uuid_id2 = uuid_id2.split('-')
            uuid_id2 = ''.join(uuid_id2)

            mail_addr = index_user[0]
            user_name = index_user[1]
            if '' == user_name:
               user_name = mail_addr

            pwd = index_user[2]
            dingding_id = index_user[3]

            user_tup = (uuid_id1, user_name, mail_addr, '', pwd, dingding_id, '', '', '', now_date, 0, '', '', now_date, now_date)
            new_cl_list.append(user_tup)

            cust_tup = (uuid_id1, '', '', '', '', '', '', '', '', now_date, now_date)
            new_ci_list.append(cust_tup)

            order_tup = (uuid_id1, uuid_id2, '', '', '', '', order_time, '', 0, 0, '', '', now_date, now_date, '', '')
            new_so_list.append(order_tup)

            break

   return [new_cl_list, new_ci_list, new_so_list]


def insert_data(host, username, pwd, tablename, data_list):
   sql_cl = "insert into t_cust_login (CUST_NO, CUST_NAME, CUST_MAIL, CUST_PHONE, CUST_PASSWORD, DING_ID, WECHAT_ID, STU_TOKEN, STU_TOKEN_EXPIRATION, " \
            "STU_ORDER_DATE, STATUS, REQ_IP, REQ_TIME, CREATE_TIME, MODIFY_TIME) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

   sql_ci = "insert into t_cust_info (CUST_NO, CUST_ALIAS, CUST_AREA, CUST_ADDR, CUST_COMPANY, CUST_PHONE, CUST_FAX, CUST_INDUSTRY, " \
            "CUST_IMAGE, CREATE_TIME, MODIFY_TIME) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

   sql_so = "insert into t_service_order (cust_no, order_no, product_no, product_name, order_model, order_status, order_time, pay_time, orig_price, " \
            "dct_rpice, date_start, date_end, create_time, modify_time, ding_process_id, ding_process_result) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

   sql_list = [sql_cl, sql_ci, sql_so]

   insert_num = excute_db(host, username, pwd, tablename, sql_list, "insert_many", data_list)

   return insert_num


def dbdata_handle(host, username, pwd, tablename1, tablename2):

   try:
      user_list = deal_usertable(host, username, pwd, tablename1)
      custlogin_list = deal_cust_logintable(host, username, pwd, tablename2)

      data_list = compare_data(user_list, custlogin_list)

      insert_num = insert_data(host, username, pwd, tablename2, data_list)
      return insert_num
   except Exception as e:
      raise e


# if __name__ == '__main__':
#    host="192.168.11.11"
#    username="isa"
#    pwd="isa1qaz2wsx"
#    tablename1="b3log_symphony"
#    tablename2="i_cas"
#
#    result = dbdata_handle(host, username, pwd, tablename1, tablename2)
#    print(result)

