import requests
import json

def tipo_class(token,space_id,text):

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