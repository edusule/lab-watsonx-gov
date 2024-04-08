import streamlit as st
from ibm_watsonx_ai.foundation_models import Model
import os
from dotenv import load_dotenv
from helpers.auth import auth
from helpers.summarization import summarization
from helpers.sentiment import sentiment
from helpers.tipo import tipo_class
from helpers.churn import churn_predict
from helpers.contestacion import res_contestacion

# Set page config to use wide mode by default
st.set_page_config(layout="wide")

load_dotenv()

apikey = os.getenv("APIKEY")
space_id_summarization = os.getenv("SPACE_ID_SUMMARIZATION")
space_id_sentiment = os.getenv("SPACE_ID_SENTIMENT")
space_id_tipo = os.getenv("SPACE_ID_TIPO")
space_id_churn = os.getenv("SPACE_ID_CHURN")
space_id_contestacion = os.getenv("SPACE_ID_CONTESTACION")
token = auth(apikey)["access_token"]

def main():

    xcol1, xcol2 = st.columns([2, 1])

    with xcol1:
        
        # Create a row of columns: one for the image and one for the title
        col1, col2 = st.columns([1, 5], gap="small")  # Adjust the ratio as needed
        
        with col1:
            # Display an image (replace 'image_path_or_url' with the actual path or URL to your image)
            st.image('images\watson.png', width=180)  # Adjust the width as needed
        
        with col2:
            # Display the title next to the image
            st.markdown("# GenIO: El sistema inteligente para la gestión de clientes")

        if 'selected_client' not in st.session_state:
            st.session_state['selected_client'] = None

        # Predefined texts for each client
        client_feedback = {
    "Client 1": {
        "queja": "Hola, el día 5 de abril realicé un depósito de $2,000 en el cajero automático de su sucursal en Paseo de la Castellana. Es mi sucursal habitual. Sin embargo, mi sorpresa fue mayúscula al comprobar que el depósito nunca se reflejó en mi cuenta. He guardado el recibo como prueba y solicito urgentemente que se investigue y se corrija este error a la brevedad. También he revisado mis transacciones por la aplicación del telefono y nada, no aparece.",
        "PuntuacionDeCredito": 812,
        "Geografia": "Spain",
        "Genero": "Female",
        "Edad": 44,
        "Antigüedad": 8,
        "Saldo": 0.0,
        "NumeroDeProductos": 3,
        "TieneTarjetaCredito": 1,
        "EsMiembroActivo": 0,
        "SalarioEstimado": 66926.83
    },
    "Client 2": {
        "queja": "¡Esto es indignante! Por vuestra culpa mi cuentas de ahorros se ha quedado vacía por no haber hecho la tramitación que os indique la semana pasada en la oficina de la calle avenida Machupichu. Esto es intolerante. Ahora la falta de fondos ha congelado muchos pagos que tenía pendientes y ahora me reclaman el pago desde muchos sitios, Como no se arregle esta situación ya me cambio de entidad bancaria.",
        "PuntuacionDeCredito": 794,
        "Geografia": "Germany",
        "Genero": "Female",
        "Edad": 55,
        "Antigüedad": 6,
        "Saldo": 115796.7,
        "NumeroDeProductos": 1,
        "TieneTarjetaCredito": 1,
        "EsMiembroActivo": 0,
        "SalarioEstimado": 160526.36
    },
    "Client 3": {
        "queja": "Estimado banco, intenté abrir una cuenta de ahorros en línea hace dos semanas y el proceso aún no se ha completado. He proporcionado todos los documentos requeridos, pero no he recibido ninguna actualización desde entonces.",
        "PuntuacionDeCredito": 744,
        "Geografia": "France",
        "Genero": "Female",
        "Edad": 39,
        "Antigüedad": 6,
        "Saldo": 0.0,
        "NumeroDeProductos": 1,
        "TieneTarjetaCredito": 0,
        "EsMiembroActivo": 0,
        "SalarioEstimado": 10662.58
    },
    "Client 4": {
        "queja": "Hola buenas, intenté realizar un pago en línea para mi factura de electricidad a través de su plataforma, pero el pago fue rechazado sin motivo aparente, causando que me cobren un recargo por pago tardío.",
        "PuntuacionDeCredito": 593,
        "Geografia": "Spain",
        "Genero": "Male",
        "Edad": 26,
        "Antigüedad": 9,
        "Saldo": 76226.9,
        "NumeroDeProductos": 1,
        "TieneTarjetaCredito": 1,
        "EsMiembroActivo": 0,
        "SalarioEstimado": 167564.82
    },
    "Client 5": {
        "queja": "Mi tarjeta acaba de ser declinada sin explicación alguna. Esto es inaceptable; he revisado mi cuenta y hay fondos suficientes. Necesito saber inmediatamente qué está pasando. ¿Hay alguna restricción o problema de seguridad en mi tarjeta que no conozco? Espero una solución rápida y una explicación de por qué no fui informado previamente de este problema. Este tipo de inconvenientes no solo es molesto, sino que me hace cuestionar la fiabilidad de sus servicios. Espero su pronta respuesta.",
        "PuntuacionDeCredito": 600,
        "Geografia": "France",
        "Genero": "Male",
        "Edad": 40,
        "Antigüedad": 1,
        "Saldo": 141136.79,
        "NumeroDeProductos": 1,
        "TieneTarjetaCredito": 1,
        "EsMiembroActivo": 1,
        "SalarioEstimado": 67803.83
    }
}

        # Icons for each client
        client_icons = {
            "Client 1": "👤",
            "Client 2": "🙎",
            "Client 3": "🧑‍💼",
            "Client 4": "👩‍💼",
            "Client 5": "🧑‍🔧"
        }

        # Create a row of columns for client buttons
        cols = st.columns(len(client_icons))
        for idx, (client, icon) in enumerate(client_icons.items()):
            with cols[idx]:
                # Ensure each button takes the full width of its column
                if st.button(f"{client} {icon}", key=f"client_{idx}", use_container_width=True):
                    st.session_state['selected_client'] = client
                    st.session_state['client_details'] = client_feedback[client]
                    churn, conf = None, None

        # Determine the text to display based on the last pressed button
        if st.session_state['selected_client']:
            selected_text = client_feedback[st.session_state['selected_client']]["queja"]
            input_text = st.text_area("Feedback del cliente:", value=selected_text)

        else:
            input_text = st.text_area("Feedback del cliente:")

        if st.button("watsonx 🧠"):
            if input_text:
                senti = sentiment(token,space_id_sentiment,input_text)
                summari = summarization(token,space_id_summarization,input_text)
                tipo = tipo_class(token,space_id_tipo,input_text)
                contestacion = res_contestacion(token,space_id_contestacion,input_text)

                col_analysis1, col_analysis2 = st.columns(2)

                # Improved results display with icons and markdown
                with col_analysis1:
                    st.markdown(f"### Análisis de sentimiento 🌡️")
                    st.markdown(f"* **Sentimiento:** {senti}")
                    
                    st.markdown(f"### Resumen de la incidencia 📝")
                    st.markdown(f"* **Resumen:** {summari}")

                    st.markdown(f"### Clasificación de incidencia por tipología 📊")
                    st.markdown(f"* **Tipo:** {tipo}")

                with col_analysis2:
                    st.markdown(f"### Contestación automática a la incidencia 🤖")
                    st.markdown(f"* **Contestación automática:** {contestacion}")

                if 'client_details' in st.session_state and st.session_state['client_details'] is not None:
                    # Retrieve and display the client details stored in session state
                    with xcol2:
                        churn,conf = churn_predict(token,space_id_churn,st.session_state['client_details'])
                else:
                    st.warning("No client details available.", icon="🚫")
                
            else:
                st.warning("Please enter some text.")

    detail_labels = [
            ("PuntuacionDeCredito", "Puntuación de Crédito"),
            ("Geografia", "Geografía"),
            ("Genero", "Género"),
            ("Edad", "Edad"),
            ("Antigüedad", "Antigüedad"),
            ("Saldo", "Saldo"),
            ("NumeroDeProductos", "Número de Productos"),
            ("TieneTarjetaCredito", "Tiene Tarjeta de Crédito"),
            ("EsMiembroActivo", "Es Miembro Activo"),
            ("SalarioEstimado", "Salario Estimado")
        ]
    
    if 'client_details' in st.session_state and st.session_state['client_details'] is not None:
        client_details = st.session_state['client_details']
    else:
        client_details = {key: "" for key, _ in detail_labels}
    
    with xcol2:
        # New section for additional client details
        st.markdown("### Detalles del Cliente")

        # Define labels and keys for the new input fields

        # Organize the input fields in a 2x5 grid
        for i in range(0, len(detail_labels), 2):
            col1, col2 = st.columns(2)
            with col1:
                key, label = detail_labels[i]
                # Use the details from the session state to set the value of each input field
                st.text_input(label, value=str(client_details.get(key, "")), key=key, max_chars=20)
            if i + 1 < len(detail_labels):
                with col2:
                    key, label = detail_labels[i + 1]
                    st.text_input(label, value=str(client_details.get(key, "")), key=key, max_chars=20)
        
        if 'client_details' in st.session_state and st.session_state['client_details'] is not None and conf is not None:
            with st.container():  # Use a container to ensure it appears below xcol2
                st.markdown("### Predicción de abandono")
                if churn:
                    st.markdown(f"**Riesgo alto de abandono** ⚠️")
                    st.markdown(f"**Confianza de la decisión:** {1-conf}")
                else:
                    st.markdown(f"**No riesgo de abandono 😌**")
                    st.markdown(f"**Confianza de la decisión:** {conf}")
        else:
            with st.container():
                st.write()

    # Continue with the rest of your main() function...
    # Ensure you handle these input values appropriately in your application logic

if __name__ == "__main__":
    main()
