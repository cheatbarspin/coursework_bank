import requests
from datetime import datetime


def get_data(url):
    """Функция для получения json данных с адреса при помощи requests,
    а так же с проверкой status кода + добавлено исключение ConnectionError """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), "INFO: Данные получены успешно!"
        return None, f"WARNING: Статус ответа: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "ERROR: requests.exceptions.ConnectionError"


def get_filtered_data(data, filtered_empty_from=False):
    """Функция фильтрации данных, проверяющая наличие state/from в дате,
    а так же выдающая лишь выполненные операции"""
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
    if filtered_empty_from:
        data = [x for x in data if "from" in x]
    return data


def get_last_data(data, count_last_values):
    """Функция сортировки по ключу Дата(временная) в обратном порядке,
    с указанным количеством операций"""
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    return data[0:count_last_values]


def get_formatted_data(data):
    """Функция форматирования данных в нужный нам формат по условию"""
    formatted_data = []
    for row in data:
        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = row['description']
        if 'from' in row:
            sender = row['from'].split()
            sender_bill = sender.pop(-1)
            sender_bill = f"{sender_bill[:4]} {sender_bill[4:6]}** **** {sender_bill[-4:]}"
            sender_info = ' '.join(sender)
        else:
            sender_bill, sender_info = "", "[СКРЫТО]"

        recipient = f"**{row['to'][-4:]}"
        amount = f"{row['operationAmount']['amount']} {row['operationAmount']['currency']['name']}"

        formatted_data.append(f"""\
{date} {description}
{sender_info} {sender_bill} -> Счет {recipient}
{amount}
""")

    return formatted_data
