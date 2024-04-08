import pandas as pd
import json
import unidecode

# Cargar el JSON en un DataFrame
with open('raw_data/json1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

def add_dot(value):
    value = unidecode.unidecode(value)
    # Replace spaces with hyphens
    value = value.replace(' ', '_')
    return value + '_'

# Apply the function to the 'tipo' column
#df['tipo'] = df['tipo'].apply(add_dot)
distinct_values = df['tipo'].unique()

# Creating a dictionary to map distinct values to unique letters
value_to_letter = {value: chr(idx + ord('A')) for idx, value in enumerate(distinct_values)}

dict_tipo = {
    "Depósitos y retiradas de dinero":"DRD_",
    "Apertura, cierre o gestión de cuentas":"ACG_",
    "Problemas causados por falta de fondos":"PCF_",
    "Realizar/recibir pagos, enviar dinero":"RPE_",
    "Usando una tarjeta de débito o cajero automático":"ATM_"
}

# Creating a new column with unique letters as identifiers
df["tipo"].replace(dict_tipo, inplace=True)
df['sentimiento'] = df['sentimiento'].apply(add_dot)

# Dividir el DataFrame en dos basado en el valor de la columna "tipo"
df_tipo_distinto = df.drop_duplicates(subset=['tipo'])

quejas = list(df_tipo_distinto["queja"])
tipos = list(df_tipo_distinto["contestación"])

tuning_dict = []

for queja,tipo in zip(quejas,tipos):
    print(queja)
    print(tipo)
    print("#############")
    tuning_dict.append({
        "input":queja,
        "output":tipo
    })

with open('data/promp_tuning.json', 'w', encoding='utf-8') as json_file:
    json.dump(tuning_dict, json_file,ensure_ascii=False)

df_evaluaciones = df[~df.index.isin(df_tipo_distinto.index)]

# Guardar los DataFrames en archivos CSV
df_tipo_distinto.to_csv('data/prompt.csv', index=False, encoding="utf-8")
df_evaluaciones.to_csv('data/evaluaciones.csv', index=False, encoding="utf-8")

df_churn = pd.read_csv("data\Churn Modeling.csv")
df = df_churn[["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]]

column_names_mapping = {
    "CreditScore": "PuntuacionDeCredito",
    "Geography": "Geografia",
    "Gender": "Genero",
    "Age": "Edad",
    "Tenure": "Antigüedad",
    "Balance": "Saldo",
    "NumOfProducts": "NumeroDeProductos",
    "HasCrCard": "TieneTarjetaCredito",
    "IsActiveMember": "EsMiembroActivo",
    "EstimatedSalary": "SalarioEstimado",
    "Exited": "Abandono"
}

df.columns = [column_names_mapping[col] for col in df.columns]


# Separate 5 rows with at least 2 having Exited = 1
exited_rows = df[df["Abandono"] == 1].sample(n=2)  # Getting 2 rows with Exited = 1
non_exited_rows = df[df["Abandono"] == 0].sample(n=3)  # Getting 3 rows with Exited = 0
test_df = pd.concat([exited_rows, non_exited_rows])

# The rest of the data will be used for training
train_df = df.drop(test_df.index)

# Saving the datasets
test_df.to_csv('data/test_data_bank_churn.csv', index=False)
train_df.to_csv('data/train_data_bank_churn.csv', index=False)

test_df.head(), train_df.head()