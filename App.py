import streamlit as st
from PIL import Image, ImageOps
from io import BytesIO

# Configuración de la página
st.title("Agrega Empresa B a tu LinkedIn")
st.write("Sube una imagen, ajusta el tamaño del logo de Empresa B, descarga el resultado ¡y comparte el orgullo de ser parte del movimiento que busca un nuevo modelo económico con Triple Impacto!")

# Ocultar solo el footer con CSS
hide_footer_style = """
    <style>
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

# Subir la imagen principal
uploaded_file = st.file_uploader("Carga la imagen principal (PNG recomendado)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Cargar la imagen principal
    try:
        main_image = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error("Error al cargar la imagen principal: asegúrate de que el archivo sea válido.")
        st.stop()

    # Mostrar la imagen principal procesada
    st.image(main_image, caption="Imagen Principal", use_container_width=True)

    # Selección de la marca de agua
    watermark_option = st.radio("Selecciona el estilo de marca de agua:", ("Opción 1", "Opción 2"))

    # Cargar la marca de agua basada en la selección
    watermark_file = "Amarillo final.png" if watermark_option == "Opción 1" else "gris final.png"
    try:
        watermark = Image.open(watermark_file).convert("RGBA")  # Marca de agua
    except FileNotFoundError:
        st.error(f"No se encontró el archivo '{watermark_file}'. Asegúrate de colocarlo en la misma carpeta que este script.")
        st.stop()
    except Exception as e:
        st.error("Error al cargar la marca de agua: asegúrate de que el archivo sea válido.")
        st.stop()

    # Continuar si la marca de agua existe
    if watermark:
        # Ajustar tamaño de la marca de agua
        scale_factor = st.slider("Tamaño del logo (porcentaje del ancho):", 10, 100, 30)
        watermark_width = int(main_image.width * (scale_factor / 100))
        watermark_height = int(watermark.size[1] * (watermark_width / watermark.size[0]))
        watermark_resized = watermark.resize((watermark_width, watermark_height))

        # Calcular posición centralizada
        position_x = (main_image.width - watermark_width) // 2
        position_y = (main_image.height - watermark_height) // 2

        # Botón para aplicar la marca de agua
        if st.button("Aplicar"):
            try:
                # Crear capa para la marca de agua
                overlay = Image.new("RGBA", main_image.size, (0, 0, 0, 0))  # Capa transparente
                overlay.paste(watermark_resized, (position_x, position_y), watermark_resized)

                # Combinar capa de la marca de agua con la imagen principal
                final_image = Image.alpha_composite(main_image, overlay)

                # Mostrar la imagen con la marca de agua
                st.image(final_image, caption="Imagen con Marca de Agua", use_container_width=True)

                # Descargar la imagen con la marca de agua
                buffer = BytesIO()
                final_image.save(buffer, format="PNG")
                buffer.seek(0)

                # Diseñar la distribución: botón, mensaje y logo
                col1, col2, col3 = st.columns([2, 4, 2])

                with col1:
                    st.download_button(
                        label="Descargar Imagen final",
                        data=buffer,
                        file_name="imagen_final.png",
                        mime="image/png",
                    )

                with col2:
                    st.write(
                        "*Este es un producto desarrollado por Extend*"
                    )

                with col3:
                    try:
                        logo = Image.open("AvatarET.png").convert("RGBA")  # Cargar logo de Extend

                        # Ajustar tamaño del logo para que coincida con el tamaño del texto
                        logo_width = 50
                        logo_height = int(logo.size[1] * (logo_width / logo.size[0]))
                        logo_resized = logo.resize((logo_width, logo_height))

                        st.image(logo_resized, use_container_width=False)
                    except FileNotFoundError:
                        st.error("No se encontró el archivo 'AvatarET.png'. Asegúrate de colocarlo en la misma carpeta que este script.")
            except Exception as e:
                st.error("Error al aplicar la marca de agua. Inténtalo nuevamente.")






