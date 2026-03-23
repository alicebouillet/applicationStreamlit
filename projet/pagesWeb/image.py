import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import cv2
from io import BytesIO

def app():


    # Titre principal
    st.markdown(
        """
        <h1 style="text-align:center;">🖼️ Analyse et Traitement d'Image</h1>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Instructions pour l'utilisateur
    st.markdown(
        """
        ### 📂 Importez votre image

        Utilisez le sélecteur de fichiers ci-dessous pour importer une image.  
        L'application analysera automatiquement l'image et vous permettra d'appliquer diverses transformations.  
        Si aucune image n'est importée, une image par défaut sera utilisée.
        """
    )
    
    uploaded_file = st.file_uploader("Choisissez une image", type=["png", "jpg", "jpeg"])

    # Charger l'image
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
    else:
        img = Image.open("projet/docs/img_fruits_leg.png")


    # Afficher les données dans des onglets
    tab1, tab2, tab3 = st.tabs(["📊 Affichage et métadonnées", "🔧 Transformations basiques", "✨ Transformations avancées"])
    
    # TAB 1 : AFFICHAGE ET MÉTADONNÉES
    with tab1:
        st.subheader("📷 Image originale")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(img, caption='Image importée', use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Métadonnées")
            st.markdown(f"**Format :** {img.format if img.format else 'N/A'}")
            st.markdown(f"**Dimensions :** {img.size[0]} × {img.size[1]} pixels")
            st.markdown(f"**Mode :** {img.mode}")
            st.markdown(f"**Taille du fichier :** {img.size[0] * img.size[1] * len(img.getbands())} bytes")
            
            # Afficher l'histogramme des couleurs
            st.markdown("### 📊 Histogramme des couleurs")
            fig, ax = plt.subplots(figsize=(6, 4))
            
            if img.mode == 'RGB':
                colors = ('r', 'g', 'b')
                for i, color in enumerate(colors):
                    histogram = img.split()[i].histogram()
                    ax.plot(histogram, color=color, alpha=0.7, label=color.upper())
                ax.legend()
            else:
                histogram = img.histogram()
                ax.plot(histogram, color='gray')
            
            ax.set_xlabel('Intensité')
            ax.set_ylabel('Fréquence')
            ax.set_title('Distribution des pixels')
            st.pyplot(fig)

    # TAB 2 : TRANSFORMATIONS BASIQUES
    with tab2:
        st.subheader("🔧 Transformations basiques")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Bouton reset
            if st.button("Réinitialiser tous les paramètres"):
                st.session_state.color_mode = "Couleur"
                st.session_state.angle = 0
                st.session_state.do_crop = False
                st.session_state.flip_horizontal = False
                st.session_state.flip_vertical = False
                st.session_state.brightness = 1.0
                st.session_state.contrast = 1.0
                st.session_state.sharpness = 1.0
                st.session_state.saturation = 1.0
                st.rerun()
                
            # Mode couleur
            st.markdown("#### 🎨 Mode d'affichage")
            color_mode = st.radio(
                "Choisissez le mode",
                ("Couleur", "Niveaux de gris"),
                key="color_mode"
            )
            
            # Rotation
            st.markdown("#### 🔄 Rotation")
            angle = st.slider("Angle de rotation (degrés)", -180, 180, 0, 15, key="angle")
            
            # Recadrage
            st.markdown("#### ✂️ Recadrage")
            do_crop = st.checkbox("Activer le recadrage", key="do_crop")
            if do_crop:
                crop_width = st.number_input("Largeur (pixels)", min_value=10, max_value=img.size[0], value=min(300, img.size[0]), key="crop_width")
                crop_height = st.number_input("Hauteur (pixels)", min_value=10, max_value=img.size[1], value=min(300, img.size[1]), key="crop_height")
            
            # Miroir
            st.markdown("#### 🪞 Miroir")
            flip_horizontal = st.checkbox("Miroir horizontal", key="flip_horizontal")
            flip_vertical = st.checkbox("Miroir vertical", key="flip_vertical")


            # Ajustements
            st.markdown("#### 🎛️ Ajustements")
            # Luminosité
            brightness = st.slider("Luminosité", 0.0, 2.0, 1.0, 0.1, key="brightness")
            
            # Contraste
            contrast = st.slider("Contraste", 0.0, 2.0, 1.0, 0.1, key="contrast")
            
            # Netteté
            sharpness = st.slider("Netteté", 0.0, 2.0, 1.0, 0.1, key="sharpness")
            
            # Saturation
            saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1, key="saturation")
        
        with col_right:
            # Appliquer les transformations
            img_transformed = img.copy()
            
            # Mode couleur
            if color_mode == "Niveaux de gris":
                img_transformed = img_transformed.convert("L")
            
            # Ajustements
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img_transformed)
                img_transformed = enhancer.enhance(brightness)
            
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img_transformed)
                img_transformed = enhancer.enhance(contrast)
            
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img_transformed)
                img_transformed = enhancer.enhance(sharpness)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img_transformed)
                img_transformed = enhancer.enhance(saturation)

            # Rotation
            if angle != 0:
                img_transformed = img_transformed.rotate(angle, expand=True, fillcolor='white')
            
            # Recadrage
            if do_crop:
                # Calculer les coordonnées pour centrer le crop
                left = (img_transformed.size[0] - crop_width) // 2
                top = (img_transformed.size[1] - crop_height) // 2
                right = left + crop_width
                bottom = top + crop_height
                # Recadrer l'image
                img_transformed = img_transformed.crop((left, top, right, bottom))
            
            # Miroir
            if flip_horizontal:
                img_transformed = img_transformed.transpose(Image.FLIP_LEFT_RIGHT)
            if flip_vertical:
                img_transformed = img_transformed.transpose(Image.FLIP_TOP_BOTTOM)
            
            st.markdown("#### ✅ Résultat")
            st.image(img_transformed, caption='Image transformée', use_container_width=True)
            
            # Bouton de téléchargement
            buf = BytesIO()
            img_transformed.save(buf, format="PNG")
            st.download_button(
                label="📥 Télécharger l'image",
                data=buf.getvalue(),
                file_name="image_transformee.png",
                mime="image/png",
                key="download_tab2"
            )


    # TAB 3 : TRANSFORMATIONS AVANCÉES
    with tab3:
        st.subheader("Transformations avancées")
        
        col_controls, col_result = st.columns([1, 2])
        
        with col_controls:

            
            st.markdown("#### ✍️ Ajouter du texte")
            add_text = st.checkbox("Ajouter du texte")
            
            if add_text:
                text_content = st.text_input("Texte :", "Exemple")
                text_color = st.color_picker("Couleur du texte", "#FF0000")
                text_size = st.slider("Taille du texte", 10, 100, 40)
            
            st.markdown("#### 🔲 Zone d'intérêt")
            add_box = st.checkbox("Afficher une zone d'intérêt")
            
            if add_box:
                box_label = st.text_input("Label de la zone :", "Zone d'interet")
                box_color = st.color_picker("Couleur du rectangle", "#FAE600")
                
                # Position et taille de la zone
                st.markdown("**Position et taille**")
                box_x = st.slider("Position X (%)", 0, 100, 33, 1, help="Position horizontale du coin supérieur gauche")
                box_y = st.slider("Position Y (%)", 0, 100, 33, 1, help="Position verticale du coin supérieur gauche")
                box_width = st.slider("Largeur (%)", 5, 100, 33, 1, help="Largeur de la zone en % de l'image")
                box_height = st.slider("Hauteur (%)", 5, 100, 33, 1, help="Hauteur de la zone en % de l'image")
        
        with col_result:
            # Appliquer les transformations
            img_advanced = img.copy()
            
            # Ajouter du texte
            if add_text:
                draw = ImageDraw.Draw(img_advanced)
                try:
                    font = ImageFont.truetype("arial.ttf", text_size)
                except:
                    font = ImageFont.load_default()
                
                # Position du texte (centré en bas)
                text_bbox = draw.textbbox((0, 0), text_content, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                position = ((img_advanced.size[0] - text_width) // 2, 
                           img_advanced.size[1] - text_height - 20)
                
                # Convertir la couleur hex en RGB
                text_rgb = tuple(int(text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                
                draw.text(position, text_content, fill=text_rgb, font=font)
            
            # Ajouter une zone d'intérêt
            if add_box:
                # Convertir PIL en array numpy pour cv2
                img_cv = cv2.cvtColor(np.array(img_advanced), cv2.COLOR_RGB2BGR)
                
                # Calculer les dimensions de la box selon les paramètres
                h, w = img_cv.shape[:2]
                
                # Convertir les pourcentages en pixels
                x1 = int((box_x / 100) * w)
                y1 = int((box_y / 100) * h)
                box_w = int((box_width / 100) * w)
                box_h = int((box_height / 100) * h)
                
                # S'assurer que la box reste dans l'image
                x1 = max(0, min(x1, w - box_w))
                y1 = max(0, min(y1, h - box_h))
                x2 = min(x1 + box_w, w)
                y2 = min(y1 + box_h, h)
                
                # Convertir la couleur hex en BGR pour cv2
                box_rgb = tuple(int(box_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                box_bgr = (box_rgb[2], box_rgb[1], box_rgb[0])
                
                # Dessiner le rectangle
                cv2.rectangle(img_cv, (x1, y1), (x2, y2), box_bgr, 3)
                
                # Ajouter le label
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                thickness = 2
                
                (text_w, text_h), baseline = cv2.getTextSize(box_label, font, font_scale, thickness)
                text_x = x1
                text_y = max(text_h + 10, y1 - 10)
                
                # Fond pour le texte
                cv2.rectangle(img_cv, (text_x, text_y - text_h - 5), (text_x + text_w, text_y + 5), box_bgr, -1)
                cv2.putText(img_cv, box_label, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                
                # Reconvertir en PIL
                img_advanced = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
            
            st.markdown("#### ✅ Résultat final")
            st.image(img_advanced, caption='Image avec transformations avancées', use_container_width=True)
            
            # Bouton de téléchargement
            buf = BytesIO()
            img_advanced.save(buf, format="PNG")
            st.download_button(
                label="📥 Télécharger l'image",
                data=buf.getvalue(),
                file_name="image_transformee.png",
                mime="image/png",
                key="download_tab3"
            )
