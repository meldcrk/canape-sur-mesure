"""
Application Streamlit pour générer des devis de canapés sur mesure
Design style 'Lovable/Shadcn' avec Onglets - Utilise canapematplot.py
"""

import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Import des modules personnalisés
from pricing import calculer_prix_total
from pdf_generator import generer_pdf_devis

# Import des fonctions de génération de schémas depuis canapematplot
from canapematplot import (
    render_LNF, render_LF_variant, render_U2f_variant,
    render_U, render_U1F_v1, render_U1F_v2, render_U1F_v3, render_U1F_v4,
    render_Simple1
)

# -----------------------------------------------------------------------------
# 1. CONFIGURATION DE LA PAGE & STYLE CSS
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Configurateur Canapé Marocain",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injection de CSS pour imiter le style Lovable (Shadcn UI) + Style des Tabs
st.markdown("""
<style>
    /* Import de la police Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Reset & Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #0f172a;
    }
    
    /* Fond général */
    .stApp {
        background-color: #f8fafc;
    }

    /* Titres */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.025em;
        color: #0f172a;
    }
    h1 { margin-bottom: 1.5rem !important; }

    /* Input Fields Styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        color: #0f172a;
        height: 42px;
    }
    
    /* Focus states */
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #000000;
        box-shadow: none;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px;
        padding: 0 16px;
        font-weight: 500;
        border: none;
        background-color: white;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important;
        color: white !important;
    }

    /* Boutons Primaires */
    div.stButton > button[kind="primary"] {
        background-color: #0f172a;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
        height: 45px;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Boutons Secondaires */
    div.stButton > button[kind="secondary"] {
        background-color: white;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        font-weight: 500;
        height: 45px;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #f1f5f9;
        border-color: #cbd5e1;
    }

    /* Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #64748b;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. FONCTION GENERATION SCHEMA (Inchangée)
# -----------------------------------------------------------------------------

def generer_schema_canape(type_canape, tx, ty, tz, profondeur, 
                          acc_left, acc_right, acc_bas,
                          dossier_left, dossier_bas, dossier_right,
                          meridienne_side, meridienne_len, coussins="auto"):
    fig = plt.figure(figsize=(12, 8))
    
    try:
        if "Simple" in type_canape:
            render_Simple1(tx=tx, profondeur=profondeur, dossier=dossier_bas,
                acc_left=acc_left, acc_right=acc_right,
                meridienne_side=meridienne_side, meridienne_len=meridienne_len,
                coussins=coussins, window_title="Canapé Simple")
        elif "L - Sans Angle" in type_canape:
            render_LNF(tx=tx, ty=ty, profondeur=profondeur,
                dossier_left=dossier_left, dossier_bas=dossier_bas,
                acc_left=acc_left, acc_bas=acc_bas,
                meridienne_side=meridienne_side, meridienne_len=meridienne_len,
                coussins=coussins, variant="auto", window_title="L - Sans Angle")
        elif "L - Avec Angle" in type_canape:
            render_LF_variant(tx=tx, ty=ty, profondeur=profondeur,
                dossier_left=dossier_left, dossier_bas=dossier_bas,
                acc_left=acc_left, acc_bas=acc_bas,
                meridienne_side=meridienne_side, meridienne_len=meridienne_len,
                coussins=coussins, window_title="L - Avec Angle")
        elif "U - Sans Angle" in type_canape:
            render_U(tx=tx, ty_left=ty, tz_right=tz, profondeur=profondeur,
                dossier_left=dossier_left, dossier_bas=dossier_bas, dossier_right=dossier_right,
                acc_left=acc_left, acc_bas=acc_bas, acc_right=acc_right,
                coussins=coussins, variant="auto", window_title="U - Sans Angle")
        elif "U - 1 Angle" in type_canape:
            render_U1F_v1(tx=tx, ty=ty, tz=tz, profondeur=profondeur,
                dossier_left=dossier_left, dossier_bas=dossier_bas, dossier_right=dossier_right,
                acc_left=acc_left, acc_right=acc_right,
                meridienne_side=meridienne_side, meridienne_len=meridienne_len,
                coussins=coussins, window_title="U - 1 Angle")
        elif "U - 2 Angles" in type_canape:
            render_U2f_variant(tx=tx, ty_left=ty, tz_right=tz, profondeur=profondeur,
                dossier_left=dossier_left, dossier_bas=dossier_bas, dossier_right=dossier_right,
                acc_left=acc_left, acc_bas=acc_bas, acc_right=acc_right,
                meridienne_side=meridienne_side, meridienne_len=meridienne_len,
                coussins=coussins, window_title="U - 2 Angles")
        
        fig = plt.gcf()
        return fig
        
    except Exception as e:
        plt.close()
        raise Exception(f"Erreur schéma: {str(e)}")

# -----------------------------------------------------------------------------
# 3. INTERFACE UTILISATEUR
# -----------------------------------------------------------------------------

st.markdown("# Configurateur de Canapé")
st.markdown("Créez votre canapé sur mesure et obtenez un devis immédiat.")
st.markdown("<br>", unsafe_allow_html=True)

# Layout principal
col_config, col_preview = st.columns([1.1, 0.9], gap="large")

# --- COLONNE GAUCHE : CONFIGURATION AVEC ONGLETS ---
with col_config:
    
    # Création des 3 onglets
    tab_structure, tab_finitions, tab_client = st.tabs(["📏 Structure", "🛋️ Finitions", "👤 Client"])
    
    # --- ONGLET 1 : STRUCTURE ---
    with tab_structure:
        with st.container(border=True):
            st.markdown("### Dimensions & Forme")
            
            type_canape = st.selectbox(
                "Modèle",
                ["Simple (S)", "L - Sans Angle", "L - Avec Angle (LF)", 
                 "U - Sans Angle", "U - 1 Angle (U1F)", "U - 2 Angles (U2F)"]
            )
            
            c1, c2, c3 = st.columns(3)
            with c1:
                label_tx = "Largeur (Tx)"
                if "L" in type_canape or "U" in type_canape: label_tx = "Largeur Bas (Tx)"
                tx = st.number_input(label_tx, 100, 600, 280 if "Simple" in type_canape else 350, 10)
            
            with c2:
                ty = tz = None
                if "L" in type_canape:
                    ty = st.number_input("Retour Gauche (Ty)", 100, 600, 250, 10)
                elif "U" in type_canape:
                    ty = st.number_input("Retour Gauche (Ty)", 100, 600, 300, 10)
                else:
                    st.markdown("<div style='height: 42px; display: flex; align-items: center; color: #cbd5e1;'>-</div>", unsafe_allow_html=True)

            with c3:
                if "U" in type_canape:
                    tz = st.number_input("Retour Droit (Tz)", 100, 600, 280, 10)
                else:
                    st.markdown("<div style='height: 42px; display: flex; align-items: center; color: #cbd5e1;'>-</div>", unsafe_allow_html=True)
                    
            profondeur = st.slider("Profondeur d'assise (cm)", 50, 120, 70, 5)

        with st.container(border=True):
            st.markdown("### Méridienne (Optionnel)")
            has_meridienne = st.checkbox("Ajouter une méridienne (ouverture sans dossier)")
            
            meridienne_side = None
            meridienne_len = 0
            
            if has_meridienne:
                m1, m2 = st.columns(2)
                with m1:
                    opts = ["Gauche (g)", "Droite (d)"]
                    if "L" in type_canape or "U" in type_canape:
                        opts.append("Bas (b)")
                    mer_sel = st.selectbox("Emplacement", opts)
                    meridienne_side = mer_sel[0].lower()
                with m2:
                    meridienne_len = st.number_input("Longueur ouverture (cm)", 30, 200, 100, 10)

    # --- ONGLET 2 : FINITIONS ---
    with tab_finitions:
        with st.container(border=True):
            st.markdown("### Accoudoirs & Dossiers")
            
            ac1, ac2 = st.columns(2)
            with ac1:
                st.markdown("**Accoudoirs**")
                acc_left = st.checkbox("Gauche", value=True, key="acc_gauche")
                acc_right = st.checkbox("Droit", value=True, key="acc_droit")
                
                show_acc_bas = True if "L" in type_canape else ("Simple" not in type_canape)
                if show_acc_bas:
                    acc_bas = st.checkbox("Bas (Retour)", value=True, key="acc_bas")
                else:
                    acc_bas = False

            with ac2:
                st.markdown("**Dossiers**")
                dossier_bas = st.checkbox("Bas (Central)", value=True, key="dos_bas")
                
                dossier_left = False
                if "Simple" not in type_canape:
                    dossier_left = st.checkbox("Gauche", value=True, key="dos_gauche")
                    
                dossier_right = False
                if "U" in type_canape:
                    dossier_right = st.checkbox("Droit", value=True, key="dos_droit")

        with st.container(border=True):
            st.markdown("### Confort & Options")
            
            cf1, cf2 = st.columns(2)
            with cf1:
                type_coussins = st.selectbox("Type de coussins", ["auto", "65", "80", "90", "valise", "p", "g"])
                type_mousse = st.selectbox("Qualité Mousse", ["HR35", "HR45", "D30", "D25"])
            with cf2:
                epaisseur = st.number_input("Épaisseur Assise (cm)", 15, 35, 25, 5)
                
            st.markdown("---")
            st.markdown("**Options supplémentaires**")
            opt1, opt2, opt3 = st.columns(3)
            with opt1:
                nb_coussins_deco = st.number_input("Coussins déco", 0, 10, 0)
            with opt2:
                nb_traversins_supp = st.number_input("Traversins extra", 0, 5, 0)
            with opt3:
                st.write("") # Spacer
                st.write("") 
                has_surmatelas = st.checkbox("Ajouter Surmatelas")

    # --- ONGLET 3 : CLIENT ---
    with tab_client:
        with st.container(border=True):
            st.markdown("### Coordonnées du Client")
            st.info("Ces informations apparaîtront sur le PDF généré.")
            
            nom_client = st.text_input("Nom complet / Entreprise")
            email_client = st.text_input("Email")


# --- COLONNE DROITE : PRÉVISUALISATION & PRIX ---
with col_preview:
    
    # La "Carte" de résultat collante
    with st.container(border=True):
        st.markdown("### 👁️ Aperçu et Devis")
        
        # Bouton de génération principale
        if st.button("🔄 Mettre à jour l'aperçu", key="generate", type="primary", use_container_width=True):
            with st.spinner("Calcul en cours..."):
                try:
                    # 1. Générer le schéma
                    fig = generer_schema_canape(
                        type_canape, tx, ty, tz, profondeur,
                        acc_left, acc_right, acc_bas,
                        dossier_left, dossier_bas, dossier_right,
                        meridienne_side, meridienne_len, type_coussins
                    )
                    
                    # Affichage propre du matplotlib
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                    
                    # 2. Calculer le prix
                    prix_details = calculer_prix_total(
                        type_canape, tx, ty, tz, profondeur,
                        type_coussins, type_mousse, epaisseur,
                        acc_left, acc_right, acc_bas,
                        dossier_left, dossier_bas, dossier_right,
                        nb_coussins_deco, nb_traversins_supp,
                        has_surmatelas, has_meridienne
                    )
                    
                    # Stockage session state
                    st.session_state['prix_details'] = prix_details

                    st.markdown("---")
                    
                    # Affichage Prix Style "Facture"
                    p1, p2 = st.columns([2, 1])
                    with p1:
                        st.markdown("**Total HT**")
                        st.markdown("TVA (20%)")
                    with p2:
                        st.markdown(f"<div style='text-align:right'>{prix_details['prix_ht']:.2f} €</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:right'>{prix_details['tva']:.2f} €</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Gros Total
                    t1, t2 = st.columns([1, 2])
                    with t1:
                        st.markdown("### Total TTC")
                    with t2:
                        st.markdown(f"<h2 style='text-align:right; color:#0f172a; margin:0;'>{prix_details['total_ttc']:.2f} €</h2>", unsafe_allow_html=True)
                    
                    # Indicateurs Marge
                    with st.expander("Données internes (Marge)"):
                        m1, m2 = st.columns(2)
                        m1.metric("Coût Revient", f"{prix_details['cout_revient_ht']} €")
                        m2.metric("Marge", f"{prix_details['marge_ht']} €", f"{prix_details['taux_marge']}%")

                except Exception as e:
                    st.error(f"Oups ! Une erreur dans la configuration : {str(e)}")

        else:
            # Placeholder si pas encore généré
            st.info("Cliquez sur 'Mettre à jour' pour voir votre configuration.")
            st.markdown("""
                <div style="background-color: #f1f5f9; border-radius: 8px; height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
                    Aperçu du schéma ici
                </div>
            """, unsafe_allow_html=True)

    # Bouton PDF
    if st.button("📄 Télécharger le Devis PDF", type="secondary", use_container_width=True):
        if not nom_client:
            st.toast("⚠️ Veuillez renseigner le nom du client dans l'onglet 'Client'.", icon="⚠️")
        else:
            with st.spinner("Génération du PDF..."):
                try:
                    # Régénération propre pour le PDF
                    fig_pdf = generer_schema_canape(
                        type_canape, tx, ty, tz, profondeur,
                        acc_left, acc_right, acc_bas,
                        dossier_left, dossier_bas, dossier_right,
                        meridienne_side, meridienne_len, type_coussins
                    )
                    img_buffer = BytesIO()
                    fig_pdf.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                    img_buffer.seek(0)
                    plt.close(fig_pdf)
                    
                    # Recalcul pour être sûr
                    prix_final = calculer_prix_total(
                        type_canape, tx, ty, tz, profondeur,
                        type_coussins, type_mousse, epaisseur,
                        acc_left, acc_right, acc_bas,
                        dossier_left, dossier_bas, dossier_right,
                        nb_coussins_deco, nb_traversins_supp,
                        has_surmatelas, has_meridienne
                    )
                    
                    config = {
                        'type_canape': type_canape,
                        'dimensions': {'tx': tx, 'ty': ty, 'tz': tz, 'profondeur': profondeur},
                        'options': {
                            'acc_left': acc_left, 'acc_right': acc_right, 'acc_bas': acc_bas,
                            'dossier_left': dossier_left, 'dossier_bas': dossier_bas, 'dossier_right': dossier_right,
                            'meridienne_side': meridienne_side, 'meridienne_len': meridienne_len,
                            'type_coussins': type_coussins, 'type_mousse': type_mousse, 'epaisseur': epaisseur
                        },
                        'client': {'nom': nom_client, 'email': email_client}
                    }
                    
                    pdf_data = generer_pdf_devis(config, prix_final, schema_image=img_buffer)
                    
                    st.download_button(
                        label="📥 Cliquez pour télécharger",
                        data=pdf_data,
                        file_name=f"Devis_{nom_client.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erreur PDF: {str(e)}")
