import datetime
import json
from database_query import Database_query as DQ


class Database():
    mnth_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day = ["Mon", "Tue", "Wed", "Thu",
           "Fri", "Sat", "Sun"]

    # data_inputs
    year_id = ""
    week_no = ""
    data_id = ""
    date = ""
    main_date = ""
    data_file_name = ""

    def user_register(self, name, code):
        with open("database/user.json", "w") as file:
            data = {"name": name, "code": code}
            data_dump = json.dumps(data, indent=6)
            file.write(data_dump)
            file.close()

    def login(self):
        with open("database/user.json") as file:
            code = json.load(file)
            code = code["code"]

            return code

    def data_input(self, name, amount, category, icon):
        self.index_fill()
        if category == "expenses":
            self.data_file_name = "database/expense.json"
        elif category == "income":
            self.data_file_name = "database/income.json"
        data = {
            self.year_id: {
                self.week_no: {
                    self.main_date: {
                        self.data_id: {
                            "name": name,
                            "amount": amount,
                            "category": category,
                            "icon": icon,
                            "date": self.date
                        }
                    }
                }
            }
        }
        qr_data = data[self.year_id][self.week_no]
        self.update_all(self.year_id, self.week_no, self.main_date, self.data_id, data)
        self.account_info(amount, category)
        DQ.query(DQ(), qr_data, self.main_date, self.data_id, category)

    def write(self, data):
        with open(self.data_file_name, "w") as file:
            initial_data = json.dumps(data, indent=4)
            file.write(initial_data)

    def load(self):
        with open(self.data_file_name, "r") as file:
            initial_data = json.load(file)
        return initial_data

    def load_today(self):
        self.index_fill()
        exp_data = self.read_data("database/expense.json")
        exp_main = exp_data["data"][self.year_id][self.week_no][self.main_date]
        inc_data = self.read_data("database/income.json")
        inc_main = inc_data["data"][self.year_id][self.week_no][self.main_date]
        all_data = {**exp_main, **inc_main}
        all_data = dict(sorted(all_data.items()))
        return all_data

    def today_total(self):
        self.index_fill()
        exp_data = self.read_data("database/expense.json")
        exp_main = exp_data["data"][self.year_id][self.week_no][self.main_date]
        inc_data = self.read_data("database/income.json")
        inc_main = inc_data["data"][self.year_id][self.week_no][self.main_date]
        all_data = {**exp_main, **inc_main}
        all_data = dict(sorted(all_data.items()))
        exp = 0
        inc = 0
        for i, y in all_data.items():
            if y["category"] == "expenses":
                exp = exp + int(y["amount"].replace(",", ""))
            else:
                inc = inc + int(y["amount"].replace(",", ""))
        return [exp, inc]

    def update_month(self, month):
        initial_data = self.load()
        final_data = month
        initial_data["data"].update(final_data)
        self.write(initial_data)

    def update_week(self, month, week):
        initial_data = self.load()
        final_data = week
        initial_data["data"][month].update(final_data)
        self.write(initial_data)

    def update_day(self, month, week, day):
        initial_data = self.load()
        final_data = day
        initial_data["data"][month][week].update(final_data)
        self.write(initial_data)

    def update_data(self, month, week, day, data):
        initial_data = self.load()
        final_data = data
        initial_data["data"][month][week][day].update(final_data)
        self.write(initial_data)

    def update_all(self, month, week, data_date, data_id, data_data):
        m = month
        w = week
        date = data_date
        id = data_id
        data = data_data
        h = self.load()
        if m in h["data"]:
            pass
            if w in h["data"][m]:
                pass

                if date in h["data"][m][w]:
                    pass

                    if id in h["data"][m][w][date]:
                        pass

                    else:
                        data = data[m][w][date]
                        self.update_data(m, w, date, data)

                else:
                    day = data[m][w]
                    self.update_day(m, w, day)

            else:
                week = data[m]
                self.update_week(m, week)
        else:
            self.update_month(data)

    def account_info(self, amount, cate):
        if cate == "expenses":
            data = self.read_data("database/account.json")
            exp = data["expenses"]["info"]
            inc = data["income"]["info"]
            acc = data["account"]["info"]
            exp = exp.replace(",", "")
            acc = acc.replace(",", "")
            amount = amount.replace(",", "")
            acc = '{:,}'.format(int(int(acc) - int(amount)))
            exp = '{:,}'.format(int(int(exp) + int(amount)))
            new_data = {
                "account": {"info": acc},
                "income": {"info": inc},
                "expenses": {"info": exp}
            }
            self.write_data("database/account.json", new_data)
        elif cate == "income":
            data = self.read_data("database/account.json")
            exp = data["expenses"]["info"]
            inc = data["income"]["info"]
            acc = data["account"]["info"]
            inc = inc.replace(",", "")
            acc = acc.replace(",", "")
            amount = amount.replace(",", "")
            acc = '{:,}'.format(int(int(acc) + int(amount)))
            inc = '{:,}'.format(int(int(inc) + int(amount)))
            new_data = {
                "account": {"info": acc},
                "income": {"info": inc},
                "expenses": {"info": exp}
            }
            self.write_data("database/account.json", new_data)

    # main = data["data"]["20208"]["w12"][i]

    def index_fill(self):
        date = self.get_date()
        year, month, day = date.strip().split("-")
        self.date = date
        self.year_id = year + month
        self.main_date = year + month + day
        self.week_no = self.week_number(int(day))
        self.data_id = self.id_generator()

    def exp_list(self):
        with open("database/exp.json") as expenses:
            exp = json.load(expenses)

            return exp

    def inc_list(self):
        with open("database/inc.json") as income:
            inc = json.load(income)

            return inc

    def write_data(self, file_name, data):
        with open(file_name, "w") as file:
            data_dump = json.dumps(data, indent=6)
            file.write(data_dump)
            file.close()

    def read_data(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)

            return data

    def week_number(self, date):
        if 1 <= date <= 7:
            return "w1"
        elif 8 <= date <= 14:
            return "w2"
        elif 15 <= date <= 21:
            return "w3"
        elif date >= 22:
            return "w4"

    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]

    def date_format(self):
        date = self.get_date()
        year, month, day = date.strip().split("-")
        month_update = int(month.replace("0", "")) - 1
        month_name = self.mnth_name[month_update]
        self.week_no = self.week_number(int(day))
        date_frmt = f"{month_name} {str(day)}"
        return date_frmt

    def id_generator(self):
        now = str(datetime.datetime.now()).replace(":", "").replace("-", "").replace(".", "")
        new, old = now.split(" ")
        main = new + old
        return main


# Database.date_format(Database())
# Database.data_input(Database(), "kitungu", "200", "income", "dog")
# Database.today_total(Database())
