import requests
import json

def churn_predict(token,space_id,values_json):

    url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{space_id}/predictions?version=2021-05-01"

    print("###########")
    print(values_json)

    values_json.pop('queja', None)

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

    churn = False

    if response.json()["predictions"][0]["values"][0][0] > 0:
        churn = True
    else:
        churn = False

    print(response.text)

    return response.json()["predictions"][0]["values"][0][0],response.json()["predictions"][0]["values"][0][1][0]