# import json
# from db import CashDB
#
#
# cash_db = CashDB('cashflow.db')
#
# debts = cash_db.get_all_debts()
#
# def get_debts():
#     # Чтение данных из JSON файла
#     with open("debts.json", "r") as json_file:
#         debts = json.load(json_file)
#     return debts
#
# def save_debts(debts):
#     # Запись данных в JSON файл
#     with open("debts.json", "w") as json_file:
#         json.dump(debts, json_file)
#
# debts_list = get_debts()
#
# for debt_item in debts:
#     debts_list.append({
#         "debt_id": str(debt_item[0]),
#         "user_id": str(debt_item[1]),
#         "debt_amount": str(debt_item[2]),
#         "creditor_name": debt_item[3],
#         "date": debt_item[4].strftime("%Y-%m-%d")
#     })
#
# save_debts(debts_list)


import json

import bcrypt

from db import CashDB


cash_db = CashDB('cashflow.db')

admins = cash_db.get_all_admin()


for admin in admins:
    print(admin[3])
    print(admin[0])
    i = admin[3]
    hashed_password = bcrypt.hashpw(i.encode('utf-8'), bcrypt.gensalt())
    password = hashed_password.decode('utf-8')
    print(password)
    cash_db.update_password(password, admin[0])


# 4352
# $2b$12$EzPrv1I5GNL/uF6uiBlD.eKYT7WRZnnFheMeMHtCZ5AP4dHAsgL2O


