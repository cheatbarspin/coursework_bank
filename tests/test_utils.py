import pytest

from utils import get_data, get_last_data, get_formatted_data, get_filtered_data


def test_get_data():
    """Тест проверки: существует ли адрес, проблему соединения и ошибку 400"""
    url = "https://file.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1677770580708&signature=HYWka6OBTvvw6eeeQxhHC43XzgynMVYtcQaKZK-5IAI&downloadName=operations.json"
    assert get_data(url) is not None
    url = "https://file.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1677770580708&signature=HYWka6OBTvvw6eeeQxhHC43XzgynMVYtcQaKZK-5IAI&downloadNam=operations.json"
    data, info = get_data(url)
    assert data is None
    assert info == "WARNING: Статус ответа: 400"
    url = "https://fil.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1677770580708&signature=HYWka6OBTvvw6eeeQxhHC43XzgynMVYtcQaKZK-5IAI&downloadNam=operations.json"
    data, info = get_data(url)
    assert data is None
    assert info == "ERROR: requests.exceptions.ConnectionError"


def test_get_filtered_data(test_data):
    """Тест на проверку нашей фикстуры, что среди выборки
    выполненных операций 3, а если учитывать
     неизвестного отправителя, то всего 2"""
    assert len(get_filtered_data(test_data)) == 3
    assert len(get_filtered_data(test_data, filtered_empty_from=True)) == 2


def test_get_last_data(test_data):
    """Тест на проверку, что после всей фильтрации
    мы на выходе получаем последнюю дату и 5 операций"""
    data = get_last_data(test_data, count_last_values=5)
    assert data[0]['date'] == '2021-03-23T10:45:06.972075'
    assert len(data) == 5


def test_get_formatted_data(test_data):
    """Тест на проверку, что все данные получаются по шаблону и скрытием,
    а данные не имеющие отправителя автоматически появляются с надписью
    [СКРЫТО]"""
    data = get_formatted_data(test_data[:1])
    assert data == ['26.08.2019 Перевод организации\nMaestro 1596 83** **** 5199 -> Счет **9589\n31957.58 руб\n']
    data = get_formatted_data(test_data[3:4])
    assert data == ['23.03.2021 Открытие вклада\n[СКРЫТО]  -> Счет **2431\n48223.05 руб.\n']
