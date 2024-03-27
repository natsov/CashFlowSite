import psycopg2

class CashDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = psycopg2.connect(
            host="localhost",
            database="cashflow",
            user="postgres",
            password="1111"
        )
        self.cursor = self.conn.cursor()

    def update_password(self, email, new_password):
        """Обновление пароля"""
        query = "UPDATE users SET passworduser = %s WHERE email = %s"
        values = (new_password, email)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def user_exists(self, email, password):
        """Проверка на существование юзера в БД"""
        query = "SELECT userid FROM users WHERE Email = %s and passworduser = %s"
        values = (email, password)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def admin_exists(self, email, password):
        """Проверка на существование администратора в БД"""
        query = "SELECT adminid FROM system_admin WHERE adminemail = %s and adminpassword = %s"
        values = (email, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return bool(result)

    def get_password(self, email):
        """Получение пароля пользователя"""
        query = "SELECT passworduser FROM users where email = %s"
        value = (email, )
        self.cursor.execute(query, value)
        result = self.cursor.fetchall()
        return result

    def check_email(self, email):
        """Проверка на существование адреса электронной почты"""
        query = "SELECT * FROM users where email = %s"
        value = (email, )
        self.cursor.execute(query, value)
        result = self.cursor.fetchall()
        return result

    def get_password_admin(self, email):
        """Получение всего списка пользователей"""
        query = "SELECT adminpassword FROM system_admin where adminemail = %s"
        value = (email, )
        self.cursor.execute(query, value)
        result = self.cursor.fetchall()
        return result

    def get_all_users(self):
        """Получение всего списка пользователей"""
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_all_admin(self):
        """Получение всего списка пользователей"""
        query = "SELECT * FROM system_admin"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_all_debts(self):
        """Получение всего списка долгов"""
        query = "SELECT * FROM debts"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_user_name(self, email):
        """Получить имя и фамилию пользователя"""
        query = "SELECT firstname, lastname FROM users WHERE Email = %s"
        values = (email, )
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    def add_user(self, user_first_name, user_second_name, email, password):
        """Добавление пользователя в БД"""
        query = "INSERT INTO users (firstname, lastname, email, passworduser) VALUES (%s, %s, %s, %s)"
        values = (user_first_name, user_second_name, email, password)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def add_user_with_id(self,user_id, user_first_name, user_second_name, email, password):
        """Добавление пользователя в БД"""
        query = "INSERT INTO users (userid, firstname, lastname, email, passworduser) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, user_first_name, user_second_name, email, password)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def get_user_id(self, email_user):
        """Получаем id юзера в базе по его email"""
        query = "SELECT userid FROM users WHERE email = %s"
        values = (email_user,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    def add_debt(self, user_id, amount, name_debt, date):
        """Добавление записи о долге"""
        query = "INSERT INTO debts (userid, debtamount, creditorname, duedate) VALUES (%s, %s, %s, %s)"
        values = (user_id, amount, name_debt, date)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def show_debts(self, user_id):
        """Вывести все долги пользователя"""
        query = "SELECT * FROM debts WHERE userid = %s"
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        debts = self.cursor.fetchall()
        return debts

    def show_transactions(self, user_id):
        """Вывести все транзакции пользователя"""
        query = "SELECT * FROM transaction_money WHERE userid = %s"
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def delete_debt(self, debt_id, user_id):
        """Удаление записи о долге"""
        query = "DELETE FROM debts WHERE debtid = %s AND userid = %s"
        values = (debt_id, user_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def add_wish(self, cost, userid, target_date, name, image):
        """Добавление записи в WishList"""
        query = "INSERT INTO wishlists (cost, userid, itemname, imageurl, targetdate) VALUES (%s, %s, %s, %s, %s)"
        values = (cost, userid, name, image, target_date)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def add_income(self, amount, userid, type):
        """Добавление записи о доходе"""
        query = "INSERT INTO transaction_money (amount, userid, trtype) VALUES (%s, %s, %s)"
        values = (amount, userid, type)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def add_expense(self, amount, userid, type, category_id):
        """Добавление записи о расходе"""
        query = "INSERT INTO transaction_money (amount, userid, trtype, categoryid) VALUES (%s, %s, %s,  %s)"
        values = (amount, userid, type, category_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False


    def get_category_id (self, name):
        """Получаем id категории по имени"""
        query = "SELECT categoryid FROM categoriesexpence WHERE categoryname = %s"
        values = (name,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    def get_category_name(self, categoryid):
        """Получаем name категории по id"""
        query = "SELECT categoryname FROM categoriesexpence WHERE categoryid = %s"
        values = (categoryid,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result


    def get_all_categories(self):
        """Получаем весь список категорий"""
        query = "SELECT categoryname FROM categoriesexpence"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


    def add_categories(self, name):
        """Добавление категории расходов"""
        query = "INSERT INTO categoriesexpence (categoryname) VALUES (%s)"
        values = (name,)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False



    def show_wishes(self, user_id):
        """Вывести желания пользователя"""
        query = "SELECT * FROM wishlists WHERE userid = %s ORDER BY wishid ASC "
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish


    def show_wish_id(self,name, user_id):
        """Получить wishid"""
        query = "SELECT wishid FROM wishlists WHERE itemname = %s and userid = %s "
        values = (name, user_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish


    def show_wishes_amount(self, wish_id):
        """Показать текущее накопление"""
        query = "SELECT accummoney FROM wishlists WHERE wishid = %s"
        values = (wish_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish

    def show_categories(self):
        """Просмотреть категории расходов"""
        query = "SELECT categoryname FROM categoriesexpence"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def add_amount_to_wish(self, amount, wish_id):
        """Добавить накопление на мечту"""
        query = "UPDATE wishlists SET accummoney = %s WHERE wishid = %s"
        values = (amount, wish_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False


    def add_bill(self, name, amount, user_id):
        """Добавление нового счета"""
        query = "INSERT INTO bills (billname, balance, userid) VALUES (%s, %s, %s)"
        values = (name, amount, user_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False


    def show_bills(self, user_id):
        """Вывести счета пользователя"""
        query = "SELECT * FROM bills WHERE userid = %s ORDER BY billid ASC "
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish


    def show_bill_id(self, name, user_id):
        """Получить billid"""
        query = "SELECT billid FROM bills WHERE billname = %s and userid = %s "
        values = (name, user_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish

    def show_bill_balance(self, bill_id):
        """Показать текущий баланс счета"""
        query = "SELECT balance FROM bills WHERE billid = %s"
        values = (bill_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        wish = self.cursor.fetchall()
        return wish

    def add_amount_to_bill(self, balance, bill_id):
        """Пополнить счёт"""
        query = "UPDATE bills SET balance = %s WHERE billid = %s"
        values = (balance, bill_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def transfer_amount_between_bills(self, source_bill_id, destination_bill_id, amount):
        """Перевести сумму между счетами"""
        try:
            self.conn.autocommit = False
            query = "SELECT balance FROM bills WHERE billid = %s"
            values = (source_bill_id,)
            self.cursor.execute(query, values)
            balance1 = self.cursor.fetchall()
            source_balance = float(balance1[0][0])

            query = "SELECT balance FROM bills WHERE billid = %s"
            values = (destination_bill_id,)
            self.cursor.execute(query, values)
            balance2 = self.cursor.fetchall()
            destination_balance = float(balance2[0][0])

            if source_balance >= amount:
                source_balance -= amount
                destination_balance += amount
                query1 = "UPDATE bills SET balance = %s WHERE billid = %s"
                values1 = (source_balance, source_bill_id)
                self.cursor.execute(query1, values1)
                query2 = "UPDATE bills SET balance = %s WHERE billid = %s"
                values2 = (destination_balance, destination_bill_id)
                self.cursor.execute(query2, values2)
                self.conn.commit()

                return True
            else:
                return False
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            self.conn.autocommit = True

    def transfer_amount_to_wish(self, wish_id, bill_id, amount):
        """Перевод денег со счета на желание"""
        try:
            self.cursor.execute("BEGIN")

            query = "SELECT accummoney FROM wishlists WHERE wishid = %s"
            values = (wish_id,)
            self.cursor.execute(query, values)
            balance1 = self.cursor.fetchall()
            source_balance = float(balance1[0][0])

            query = "SELECT balance FROM bills WHERE billid = %s"
            values = (bill_id,)
            self.cursor.execute(query, values)
            balance2 = self.cursor.fetchall()
            destination_balance = float(balance2[0][0])

            if destination_balance >= amount:
                source_balance += amount
                destination_balance -= amount
                print(source_balance, destination_balance)
                query1 = "UPDATE wishlists SET accummoney = %s WHERE wishid = %s"
                values1 = (source_balance, wish_id)
                self.cursor.execute(query1, values1)
                query2 = "UPDATE bills SET balance = %s WHERE billid = %s"
                values2 = (destination_balance, bill_id)
                self.cursor.execute(query2, values2)
                self.conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            self.cursor.execute("COMMIT")

    def remove_bill(self, bill_id, user_id):
        """Удаление счета"""
        query = "DELETE FROM bills WHERE billid = %s AND userid = %s"
        values = (bill_id, user_id)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def order_by(self, name_column, user_id, sort_direction):
        """Сортировка данных"""
        query = "SELECT * FROM debts WHERE userid = %s ORDER BY {} {}".format(name_column, sort_direction)
        values = (user_id, )
        self.cursor.execute(query, values)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result


    def search(self, date1, date2, userid):
        """Поиск по дате"""
        query = "SELECT * FROM transaction_money WHERE trdate BETWEEN %s and %s and userid = %s"
        values = (date1, date2, userid)
        self.cursor.execute(query, values)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result


    def get_data_statistic(self, user_id):
        """Получение истории о доходах/расходах"""
        query = 'SELECT amount, trdate FROM transaction_money WHERE userid = %s ORDER BY trdate'
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def get_data_statistic_interval(self, user_id,type_stat, start_date, end_date):
        """Получение истории о доходах/расходах"""
        query = "SELECT amount, trdate FROM transaction_money WHERE userid= %s AND trtype = %s AND trdate >= %s AND trdate <= %s"
        values = (user_id, type_stat, start_date, end_date)
        self.cursor.execute(query, values)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def users_table(self):
        """Получение данных из users"""
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def bills_table(self):
        """Получение данных из bills"""
        query = "SELECT * FROM bills"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def categoriesexpence_table(self):
        """Получение данных из categoriesexpence"""
        query = "SELECT * FROM categoriesexpence"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result


    def debts_table(self):
        """Получение данных из debts"""
        query = "SELECT * FROM debts"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def system_admin_table(self):
        """Получение данных из system_admin"""
        query = "SELECT * FROM system_admin"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result


    def transaction_money_table(self):
        """Получение данных из transaction_money"""
        query = "SELECT * FROM transaction_money"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def wishlists_table(self):
        """Получение данных из wishlists"""
        query = "SELECT * FROM wishlists"
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result





    def __del__(self):
        self.cursor.close()
        self.conn.close()