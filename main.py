from utils import get_data, get_filtered_data, get_last_data, get_formatted_data


def main():
    # адрес с данными банковских переводов
    OPERATIONS_URL = "https://file.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1677770580708&signature=HYWka6OBTvvw6eeeQxhHC43XzgynMVYtcQaKZK-5IAI&downloadName=operations.json"
    # кол-во выполненных операций, которые мы хотим вывести
    COUNT_LAST_VALUES = 5
    # есть ли в словаре отправитель
    FILTERED_EMPTY_FROM = True

    data, info = get_data(OPERATIONS_URL)
    if not data:
        exit(info)
    print(info, end="\n\n")

    data = get_filtered_data(data, FILTERED_EMPTY_FROM)
    data = get_last_data(data, COUNT_LAST_VALUES)
    data = get_formatted_data(data)
    for row in data:
        print(row)


if __name__ == "__main__":
    main()
