import requests
import json

def churn_predict(values_json: dict) -> str:

    """Esta función permite calcular el riesgo de abandono de un cliente basándose en los datos del cliente recolectados en la incidencia. 
    :param values_json: json con los datos del cliente Te doy un ejemplo del input correcto de como tienes que introducir los datos. Se te penalizara si modificas el formato. Se preciso. 
    Ejemplo: {'PuntuacionDeCredito': 812, 'Geografia': 'Spain', 'Genero': 'Female', 'Edad': 44, 'Antigüedad': 8, 'Saldo': 0.0, 'NumeroDeProductos': 3, 'TieneTarjetaCredito': 1, 'EsMiembroActivo': 0, 'SalarioEstimado': 66926.83}
    :return: Son dos valores de la predicción, el primero es el riesgo de abandono y el segundo es el nivel de confianza de la predicción. Presentalos en formato tabla para el usuario. Solo contesta con la tabla.
    """

    space_id = "6a880c3e-abbe-4444-81e0-2d35ec08e7a2"
    url = "https://iam.cloud.ibm.com/identity/token"
    apikey="aDF-UZT2GTNO-z-VeVZil-VrHndSSxB7luomkS3weZah"

    payload = f'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={apikey}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '\\',
    'Cookie': 'ak_bmsc=3E48C90874AE6442260BFD02849A66B8~000000000000000000000000000000~YAAQj2ATAssoO5uOAQAAd4ysqRc4DpYFBMBBjRNgEX7A1OyxW3YruGvi/SDI8sRfGnQ9Cz/bfkiveItmZwI2uRUH3YGIAuf/MYyQ2XyCTU5WbLF7/lPV6lzPzCVplQO5VsU1PGUb81QEOtVj2DOeiauwNEQZEhZIZHSoA3Ulu5HFxiFt5ouzEcS2m8dLxwnXXLIlft3WjeeyLvzuNssa/Ut04BkssUB6DSpVHybqi9ugD0CHwdMdv7hpB55SVlbeF5l6a1JXDOL+mor6pX854h1buGiq8HtHSdA+sKTbf9iOiR+VTiVvt0cTZpf1Dl+Bz/80jYD0NP0YT9HTVQz9Uqc9ULzpeylqTH/WEfCYHk7KTRmM6PVO89usBxYQ'
    }

    token = requests.request("POST", url, headers=headers, data=payload).json()["access_token"]

    url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{space_id}/predictions?version=2021-05-01"

    #values_json = values_json["values_json"]

    #values_json["Antigüedad"] = values_json.pop("Antiguedad")

    fields = list(values_json.keys())
    values = list(values_json.values())

    payload = json.dumps({
        "input_data": [
        {
            "fields": fields,
            "values": [values]
        }
    ]})

    print(payload)
    
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}',
    'Cookie': 'ak_bmsc=3E48C90874AE6442260BFD02849A66B8~000000000000000000000000000000~YAAQj2ATAssoO5uOAQAAd4ysqRc4DpYFBMBBjRNgEX7A1OyxW3YruGvi/SDI8sRfGnQ9Cz/bfkiveItmZwI2uRUH3YGIAuf/MYyQ2XyCTU5WbLF7/lPV6lzPzCVplQO5VsU1PGUb81QEOtVj2DOeiauwNEQZEhZIZHSoA3Ulu5HFxiFt5ouzEcS2m8dLxwnXXLIlft3WjeeyLvzuNssa/Ut04BkssUB6DSpVHybqi9ugD0CHwdMdv7hpB55SVlbeF5l6a1JXDOL+mor6pX854h1buGiq8HtHSdA+sKTbf9iOiR+VTiVvt0cTZpf1Dl+Bz/80jYD0NP0YT9HTVQz9Uqc9ULzpeylqTH/WEfCYHk7KTRmM6PVO89usBxYQ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print("################################################################################")
    print(response.text)

    churn = False

    if response.json()["predictions"][0]["values"][0][0] > 0:
        return "Riesgo alto de abandono", str(1-response.json()["predictions"][0]["values"][0][1][0])
    else:
        return "No hay riesgo de abandono", str(response.json()["predictions"][0]["values"][0][1][0])

print(churn_predict({
    "PuntuacionDeCredito": 812,
    "Geografia": "Spain",
    "Genero": "Female",
    "Edad": 44,
    "Antigüedad": 8,
    "Saldo": 0,
    "NumeroDeProductos": 3,
    "TieneTarjetaCredito": 1,
    "EsMiembroActivo": 0,
    "SalarioEstimado": 66926.83
}))