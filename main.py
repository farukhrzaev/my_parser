import json
import requests


def get_products_list():
    url = "https://www.auchan.ru/v1/catalog/products"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.auchan.ru",
        "Referer": "https://www.auchan.ru/catalog/kolbasnye-izdeliya/myasnye-delikatesy/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Chrome/124.0.0.0",  # установите свой User-Agent
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "filter": {
            "category": "myasnye_delikatesy",
            "promo_only": False,
            "active_only": False,
            "cashback_only": False,
        },
        "page": 1,
        "perPage": 100,  # количество товара которое нужно вывести
        "merchantId": 1,
    }

    all_products_list = []

    while True:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            products = response.json().get("items", [])

            if not products:
                break

            all_products_list.extend(products)

            if len(all_products_list) >= data["perPage"]:
                break

            data["page"] += 1
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(response.text)

            break

    return all_products_list