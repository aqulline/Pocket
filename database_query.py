import json


class Database_query:

    def load_query_data(self):
        with open("database/data.json") as file:
            initail_data = json.load(file)
        return initail_data

    def write_query_data(self, data):
        with open("database/data.json", "w") as file:
            initial_data = json.dumps(data, indent=4)
            file.write(initial_data)

    def query(self, data, date, id, cate):
        name = data[date][id]["name"]
        data_data = data[date][id]
        print(name)
        data_model = {
            cate: {
                name: {
                    "count": "1",
                    "name": data[date][id]["name"],
                    "total_amount": data[date][id]["amount"],
                    "category": cate,
                    "icon": data[date][id]["icon"],
                    "date": data[date][id]["date"],
                }
            }
        }
        self.update_all(cate, name, data_model)

    def update_category(self, cate):
        initial_data = self.load_query_data()
        final_data = cate
        initial_data["data"].update(final_data)
        self.write_query_data(initial_data)

    def update_name(self, cate, name):
        initial_data = self.load_query_data()
        final_data = name
        initial_data["data"][cate].update(final_data)
        self.write_query_data(initial_data)

    def count_amount_update(self, name, cate, amount, data):
        qdata = self.load_query_data()
        amount = amount.replace(",", "")
        get_amount = qdata["data"][cate][name]["total_amount"]
        get_amount = get_amount.replace(",", "")
        get_count = qdata["data"][cate][name]["count"]
        new_amount = str(int(get_amount) + int(amount))
        new_amount = '{:,}'.format(int(new_amount))
        new_count = str(int(get_count) + 1)
        data[name]["total_amount"] = new_amount
        data[name]["count"] = new_count
        self.update_name(cate, data)

    def update_all(self, cate, name, data):
        qdata = self.load_query_data()
        data_data = data
        amount = data[cate][name]["total_amount"]
        if cate in qdata["data"]:
            if name in qdata["data"][cate]:
                main_data = data_data[cate]
                self.count_amount_update(name, cate, amount, main_data)
            else:
                main_data = data_data[cate]
                self.update_name(cate, main_data)
        else:
            self.update_category(data)

    def account_info(self):
        with open("database/account.json") as file:
            data = json.load(file)
            acc = data["account"]["info"]
            inc = data["income"]["info"]
            exp = data["expenses"]["info"]

        return [str(acc), str(inc), str(exp)]
