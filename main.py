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
        "perPage": 100,
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


def processing_list_products(all_products_list):
    products_info_list = []

    for product in all_products_list:
        product_id = product.get("id")
        product_name = product.get("title")
        product_code = product.get("code")
        product_price = product.get("price", {}).get("value")
        product_currency = product.get("price", {}).get("currency")

        old_price_data = product.get("oldPrice", {})
        product_old_price = old_price_data.get("value") if old_price_data else None

        product_brand_name = product.get("brand", {}).get("name")

        product_link = f"https://www.auchan.ru/product/{product_code}/"

        processed_product = {
            "id": product_id,
            "name": product_name,
            "link": product_link,
            "oldPrice": product_old_price,
            "price": {"value": product_price, "currency": product_currency},
            "brand": {
                "name": product_brand_name,
            },
        }
        products_info_list.append(processed_product)

    return products_info_list


if __name__ == "__main__":
    all_products_list = get_products_list()

    if all_products_list:
        products_info_list = processing_list_products(all_products_list)

        json_data = json.dumps(products_info_list, ensure_ascii=False, indent=2)

        with open("products_info_list.json", "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

        print("Information about the products has been successfully written to products_info_list.json.")
    else:
        print("The request for product information failed.")
