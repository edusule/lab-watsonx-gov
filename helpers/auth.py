def auth(apikey):
    import requests

    url = "https://iam.cloud.ibm.com/identity/token"

    payload = f'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={apikey}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '\\',
    'Cookie': 'ak_bmsc=3E48C90874AE6442260BFD02849A66B8~000000000000000000000000000000~YAAQj2ATAssoO5uOAQAAd4ysqRc4DpYFBMBBjRNgEX7A1OyxW3YruGvi/SDI8sRfGnQ9Cz/bfkiveItmZwI2uRUH3YGIAuf/MYyQ2XyCTU5WbLF7/lPV6lzPzCVplQO5VsU1PGUb81QEOtVj2DOeiauwNEQZEhZIZHSoA3Ulu5HFxiFt5ouzEcS2m8dLxwnXXLIlft3WjeeyLvzuNssa/Ut04BkssUB6DSpVHybqi9ugD0CHwdMdv7hpB55SVlbeF5l6a1JXDOL+mor6pX854h1buGiq8HtHSdA+sKTbf9iOiR+VTiVvt0cTZpf1Dl+Bz/80jYD0NP0YT9HTVQz9Uqc9ULzpeylqTH/WEfCYHk7KTRmM6PVO89usBxYQ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()