import requests
import json

def tipo_class(text: str) -> dict:

    """
    Función para clasificar la incidencia de un cliente en la tipologia definida por el banco :param text: Texto con la incidencia original y completa del cliente. Se te penalizara si haces alguna modifcacion de la incidencia original :return: Tipologia de la incidencia, solo contesta con el texto generado nada más.
    """

    space_id = "d64445ae-c251-4375-b249-9839f9f829ee"
    url = "https://iam.cloud.ibm.com/identity/token"
    apikey="aDF-UZT2GTNO-z-VeVZil-VrHndSSxB7luomkS3weZah"

    payload = f'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={apikey}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '\\',
    'Cookie': 'ak_bmsc=3E48C90874AE6442260BFD02849A66B8~000000000000000000000000000000~YAAQj2ATAssoO5uOAQAAd4ysqRc4DpYFBMBBjRNgEX7A1OyxW3YruGvi/SDI8sRfGnQ9Cz/bfkiveItmZwI2uRUH3YGIAuf/MYyQ2XyCTU5WbLF7/lPV6lzPzCVplQO5VsU1PGUb81QEOtVj2DOeiauwNEQZEhZIZHSoA3Ulu5HFxiFt5ouzEcS2m8dLxwnXXLIlft3WjeeyLvzuNssa/Ut04BkssUB6DSpVHybqi9ugD0CHwdMdv7hpB55SVlbeF5l6a1JXDOL+mor6pX854h1buGiq8HtHSdA+sKTbf9iOiR+VTiVvt0cTZpf1Dl+Bz/80jYD0NP0YT9HTVQz9Uqc9ULzpeylqTH/WEfCYHk7KTRmM6PVO89usBxYQ'
    }

    token = requests.request("POST", url, headers=headers, data=payload).json()["access_token"]

    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{space_id}/text/generation?version=2021-05-01"

    payload = json.dumps({
    "parameters": {
        "prompt_variables": {
        "input": f"{text}"
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}',
    'Cookie': 'ak_bmsc=3E48C90874AE6442260BFD02849A66B8~000000000000000000000000000000~YAAQj2ATAssoO5uOAQAAd4ysqRc4DpYFBMBBjRNgEX7A1OyxW3YruGvi/SDI8sRfGnQ9Cz/bfkiveItmZwI2uRUH3YGIAuf/MYyQ2XyCTU5WbLF7/lPV6lzPzCVplQO5VsU1PGUb81QEOtVj2DOeiauwNEQZEhZIZHSoA3Ulu5HFxiFt5ouzEcS2m8dLxwnXXLIlft3WjeeyLvzuNssa/Ut04BkssUB6DSpVHybqi9ugD0CHwdMdv7hpB55SVlbeF5l6a1JXDOL+mor6pX854h1buGiq8HtHSdA+sKTbf9iOiR+VTiVvt0cTZpf1Dl+Bz/80jYD0NP0YT9HTVQz9Uqc9ULzpeylqTH/WEfCYHk7KTRmM6PVO89usBxYQ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    dict_json= {
        "DRD_": "Depósitos y retiradas de dinero",
        "ACG_": "Apertura, cierre o gestión de cuentas",
        "PCF_": "Problemas causados por falta de fondos",
        "RPE_": "Realizar/recibir pagos, enviar dinero",
        "ATM_": "Usando una tarjeta de débito o cajero automático"
    }

    return dict_json[response.json()["results"][0]["generated_text"].replace("\n", "").replace(" ", "")]

print(tipo_class("Hola, el día 5 de abril realicé un depósito de $2,000 en el cajero automático de su sucursal en Paseo de la Castellana. Es mi sucursal habitual. Sin embargo, mi sorpresa fue mayúscula al comprobar que el depósito nunca se reflejó en mi cuenta. He guardado el recibo como prueba y solicito urgentemente que se investigue y se corrija este error a la brevedad. También he revisado mis transacciones por la aplicación del telefono y nada, no aparece."))