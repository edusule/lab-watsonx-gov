import requests
import json

def summarization(text: str) -> dict:

    """
    Función para resumir incidencia de un cliente
    :param text: Texto con la incidencia de un cliente
    :return: Incidencia resumida
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

    return response.json()["results"][0]["generated_text"]