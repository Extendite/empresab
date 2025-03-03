import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

# Configuración de la página
st.title("Generador de Foto de Perfil con Empresa B")
st.write("Sube tu foto, recórtala en un círculo y agrega el logo de Empresa B. ¡Descarga el resultado y úsala en LinkedIn!")

# Ocultar solo el footer con CSS
hide_footer_style = """
    <style>
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

# Subir la imagen principal
uploaded_file = st.file_uploader("Carga tu foto de perfil (PNG recomendado)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Cargar la imagen principal
    try:
        main_image = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error("Error al cargar la imagen principal: asegúrate de que el archivo sea válido.")
        st.stop()

    # Mostrar la imagen original
    st.image(main_image, caption="Imagen Original", use_column_width=True)

    # Recortar la imagen en un círculo
    size = min(main_image.size)  # Tamaño del círculo (usamos la dimensión más pequeña)
    mask = Image.new("L", (size, size), 0)  # Máscara circular
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)  # Dibujar un círculo en la máscara

    # Aplicar la máscara a la imagen
    main_image_cropped = ImageOps.fit(main_image, (size, size))  # Recortar la imagen al tamaño del círculo
    main_image_cropped.putalpha(mask)  # Aplicar la máscara circular

    # Mostrar la imagen recortada en un círculo
    st.image(main_image_cropped, caption="Imagen Recortada en Círculo", use_column_width=True)

    # Cargar la marca de agua (logo de Empresa B)
    watermark_file = "sello_amarillo_gris.png"  # Logo de Empresa B
    try:
        watermark = Image.open(watermark_file).convert("RGBA")
    except FileNotFoundError:
        st.error(f"No se encontró el archivo '{watermark_file}'. Asegúrate de colocarlo en la misma carpeta que este script.")
        st.stop()
    except Exception as e:
        st.error("Error al cargar la marca de agua: asegúrate de que el archivo sea válido.")
        st.stop()

    # Ajustar tamaño de la marca de agua
    scale_factor = st.slider("Tamaño del logo (porcentaje del ancho):", 10, 100, 30)
    watermark_width = int(size * (scale_factor / 100))  # Tamaño proporcional al círculo
    watermark_height = int(watermark.size[1] * (watermark_width / watermark.size[0]))
    watermark_resized = watermark.resize((watermark_width, watermark_height))

    # Crear un círculo semi-transparente (similar a "Open to Work")
    circle_size = watermark_resized.width  # Tamaño del círculo igual al tamaño del logo
    circle = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))  # Fondo transparente
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, circle_size, circle_size), fill=(0, 0, 0, 128))  # Círculo semi-transparente

    # Combinar el círculo con el logo de Empresa B
    circle.paste(watermark_resized, (0, 0), watermark_resized)

    # Posición del círculo en la esquina inferior izquierda
    position_x = 20  # Margen de 20 píxeles desde el borde izquierdo
    position_y = size - circle_size - 20  # Margen de 20 píxeles desde el borde inferior

    # Aplicar la marca de agua a la imagen recortada
    final_image = main_image_cropped.copy()
    final_image.paste(circle, (position_x, position_y), circle)

    # Mostrar la imagen final
    st.image(final_image, caption="Imagen Final con Marca de Agua", use_column_width=True)

    # Descargar la imagen final
    buffer = BytesIO()
    final_image.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Descargar Imagen Final",
        data=buffer,
        file_name="foto_perfil_empresa_b.png",
        mime="image/png",
    )




