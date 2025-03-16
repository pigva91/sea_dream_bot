import requests


# Добавить ссылку на битрикс
def req(name, number, city, type, budget, type_of_funds, detail, district):
    url = 'https://ССЫЛКА НА БИТРИКС/crm.lead.add.json'

    data = {
        "fields": {
            "TITLE": "Заявка TG",
            "UF_CRM_1739362341": name,
            "PHONE": [
                {
                    "VALUE": number,
                }],
            "ASSIGNED_BY_ID": '49',
            "UF_CRM_1739363249": city,
            "UF_CRM_1739363296": type,
            "UF_CRM_1735573745": budget,
            "UF_CRM_1728402741": type_of_funds,
            "UF_CRM_1728402821": district,
            "SOURCE_ID": "OTHER"
        }
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Лид успешно добавлен')
    else:
        print('Ошибка:', response.status_code, response.text)


def main():
    None


if __name__ == "__main__":
    main()
