import pandas as pd
import json
import unidecode
import numpy as np

# Cargar el JSON en un DataFrame
with open('raw_data/json1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)
df["tipo_completo"] = df["tipo"].copy()

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

resolucion_depositos = """
Para realizar depósitos o retiradas de dinero, los clientes pueden seguir estos pasos detallados:
- Depósitos: 
  a. En sucursales: Acudir a cualquier sucursal bancaria, completar el formulario de depósito y 
     entregar el dinero en efectivo o cheque al cajero.
  b. En cajeros automáticos: Utilizar los cajeros que permiten depósitos introduciendo la tarjeta, 
     seleccionando la opción de depósito y siguiendo las instrucciones para insertar el efectivo o 
     los cheques.
  c. Banca en línea: Iniciar sesión en la cuenta, seleccionar la opción "Depósito" y seguir los 
     pasos para realizar un depósito por medio de transferencia electrónica o imagen de cheque.

- Retiradas: 
  a. En cajeros automáticos: Introducir la tarjeta de débito, seleccionar la cantidad deseada y 
     retirar el dinero.
  b. En sucursales: Presentar una identificación válida y el número de cuenta al cajero, y solicitar 
     la cantidad específica de dinero.
  c. Banca en línea: Programar una retirada para recoger en sucursal o para ser enviada por medio de 
     un cheque.
"""
resolucion_apertura = """
- Apertura de cuenta:
  a. En línea: Completar el formulario de solicitud en la página web del banco, adjuntar los 
     documentos necesarios (identificación y prueba de domicilio) y seguir las instrucciones para 
     verificar la identidad.
  b. En sucursal: Visitar la sucursal más cercana con los documentos necesarios, hablar con un 
     representante de atención al cliente para revisar las opciones de cuenta y firmar el acuerdo de 
     servicio.

- Cierre de cuenta:
  a. Solicitar el cierre a través de la banca en línea, seleccionando la opción correspondiente y 
     siguiendo los pasos para confirmar la acción.
  b. En sucursal: Solicitar una cita con un asesor para discutir el cierre de la cuenta, asegurarse 
     de que todos los débitos o créditos pendientes estén resueltos y completar el formulario de cierre.

- Gestión de cuentas:
  a. Banca en línea: Ofrece herramientas para verificar saldos, revisar transacciones, transferir 
     fondos, pagar facturas, actualizar información personal y configurar alertas.
  b. Aplicación móvil: Similar a la banca en línea, pero optimizada para dispositivos móviles; permite 
     manejar la cuenta desde cualquier lugar.
"""
resolucion_problema = """
Si un cliente enfrenta problemas por falta de fondos:
- Revisar transacciones: Verificar todas las transacciones recientes para entender el origen del 
  déficit.
- Alertas de saldo: Configurar alertas para ser notificado por mensaje de texto o email cuando el 
  saldo baje de un umbral específico.
- Planes de financiamiento: Discutir con el banco las opciones de crédito o líneas de crédito 
  temporales para cubrir déficits.
"""
resolucion_pagos = """
- Métodos para realizar pagos:
  a. Transferencias electrónicas: Usar la banca en línea para enviar dinero a cuentas nacionales o 
     internacionales.
  b. Pagos móviles: Utilizar aplicaciones como Google Pay o Apple Pay para realizar pagos rápidos.
  c. Servicios en línea: Utilizar plataformas como PayPal para enviar y recibir pagos de manera 
     segura.

- Métodos para enviar dinero:
  a. Transferencia bancaria: Realizar una transferencia desde la banca en línea seleccionando al 
     beneficiario y especificando el monto.
  b. Aplicaciones de pago: Usar servicios como Venmo para enviar dinero a amigos o familiares de 
     manera instantánea.
"""
resolucion_tarjeta = """
- Activación y uso de tarjeta de débito:
  a. Activar la tarjeta siguiendo las instrucciones recibidas con la tarjeta o a través de la banca 
     en línea.
  b. Establecer un PIN seguro y no compartirlo con nadie.
  c. Usar la tarjeta para pagos en comercios o retiros en cajeros automáticos.
  
- Problemas con cajeros automáticos:
  a. Si un cajero no dispensa dinero pero muestra un débito en la cuenta, contactar inmediatamente al 
     banco.
  b. Reportar cajeros descompuestos o sospechosos al banco y preferentemente usar cajeros en 
     ubicaciones seguras.
"""

df_evaluaciones["context1"] = resolucion_depositos + " " + resolucion_apertura
df_evaluaciones["context2"] = resolucion_problema + " " + resolucion_pagos
df_evaluaciones["context3"] = resolucion_tarjeta

list_cats = list(df_evaluaciones["tipo"])
res_list = []

for tipo in list_cats:
    if tipo == "DRD_":
        res_list.append(resolucion_depositos)
    if tipo == "ACG_":
        res_list.append(resolucion_apertura)
    if tipo == "PCF_":
        res_list.append(resolucion_problema)
    if tipo == "RPE_":
        res_list.append(resolucion_pagos)
    if tipo == "ATM_":
        res_list.append(resolucion_tarjeta)

df_evaluaciones["resolucion"] = np.array(res_list)

df_evaluaciones.to_csv('data/evaluaciones.csv', index=False, encoding="utf-8")

df_evaluaciones[["tipo_completo","context1","context2","context3","resolucion"]].to_csv('data/evaluaciones_rag.csv', index=False, encoding="utf-8")

df_churn = pd.read_csv("data/Churn Modeling.csv")
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