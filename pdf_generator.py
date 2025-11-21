from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

def generer_pdf_devis(config, prix_details, schema_image=None):
    """
    Génère un PDF de devis compact (1 page) avec Prix TTC uniquement.
    """
    buffer = BytesIO()
    # Marges réduites à 1cm pour s'assurer que tout tient sur une page
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1*cm, bottomMargin=1*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # --- DÉFINITION DES STYLES ---

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    header_info_style = ParagraphStyle(
        'HeaderInfo',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    
    # Style spécifique pour le GROS PRIX
    price_style = ParagraphStyle(
        'PriceStyle',
        parent=styles['Heading2'],
        fontSize=16,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=10
    )
    
    column_header_style = ParagraphStyle(
        'ColumnHeaderStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        alignment=TA_LEFT,
        spaceAfter=2
    )

    detail_style = ParagraphStyle(
        'DetailStyle',
        parent=styles['Normal'],
        fontSize=8, # Police légèrement réduite pour gain de place
        leading=10,
        textColor=colors.black,
        alignment=TA_LEFT
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceBefore=5
    )
    
    # =================== 1. EN-TÊTE ===================
    titre = Paragraph("MON CANAPÉ MAROCAIN", title_style)
    elements.append(titre)
    
    # =================== 2. INFORMATIONS (HAUT) ===================
    type_canape = config['type_canape']
    dims = config['dimensions']
    
    # Formatage des dimensions
    if "U" in type_canape:
        dim_str = f"{dims.get('ty',0)}x{dims.get('tx',0)}x{dims.get('tz',0)}"
    elif "L" in type_canape:
        dim_str = f"{dims.get('ty',0)}x{dims.get('tx',0)}"
    else:
        dim_str = f"{dims.get('tx',0)}x{dims.get('profondeur',0)}"
        
    mousse_type = config['options'].get('type_mousse', 'HR35')
    
    # Textes Oui/Non/Avec/Sans
    dossier_txt = 'Avec' if config['options'].get('dossier_bas') else 'Sans'
    acc_txt = 'Oui' if (config['options'].get('acc_left') or config['options'].get('acc_right')) else 'Non'

    # Bloc technique
    infos_techniques = [
        f"<b>Dimensions:</b> {dim_str} cm",
        f"<b>Confort:</b> {mousse_type}",
        f"<b>Dossiers:</b> {dossier_txt} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Accoudoirs:</b> {acc_txt}"
    ]
    
    # Bloc Client
    client = config['client']
    infos_client = []
    if client['nom']: infos_client.append(f"<b>Nom:</b> {client['nom']}")
    if client['email']: infos_client.append(f"<b>Email:</b> {client['email']}")
    
    full_header_text = " &nbsp; | &nbsp; ".join(infos_techniques)
    if infos_client:
        full_header_text += "<br/><br/>" + " &nbsp; - &nbsp; ".join(infos_client)
        
    elements.append(Paragraph(full_header_text, header_info_style))
    
    # --- GESTION DYNAMIQUE DES DESCRIPTIONS DE MOUSSE ---
    descriptions_mousse = {
        'D25': "La mousse D25 est une mousse polyuréthane de 25kg/m3. Elle est très ferme, parfaite pour les habitués des banquettes marocaines classiques.",
        'D30': "La mousse D30 est une mousse polyuréthane de 30kg/m3. Elle est ultra ferme, idéale pour ceux qui recherchent un canapé très ferme.",
        'HR35': "La mousse HR35 est une mousse haute résilience de 35kg/m3. Elle est semi ferme confortable, parfaite pour les adeptes des salons confortables.<br/>Les mousses haute résilience reprennent rapidement leur forme initiale et donc limitent l’affaissement dans le temps.",
        'HR45': "La mousse HR45 est une mousse haute résilience de 45kg/m3. Elle est ferme confortable, parfaite pour les adeptes des salons confortables mais pas trop moelleux.<br/>Les mousses haute résilience reprennent rapidement leur forme initiale et donc limitent l’affaissement dans le temps."
    }
    
    # Récupération du texte correspondant, ou HR35 par défaut
    texte_mousse = descriptions_mousse.get(mousse_type, descriptions_mousse['HR35'])
    
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(f"<i>{texte_mousse}</i>", header_info_style))
    
    elements.append(Spacer(1, 0.3*cm))

    # =================== 3. SCHÉMA (AUTO-REDIMENSIONNÉ) ===================
    if schema_image:
        try:
            img = Image(schema_image)
            # On limite la hauteur pour être sûr que ça tienne sur une page
            # Largeur max 18cm, Hauteur max 11cm
            avail_width = 18 * cm
            avail_height = 11 * cm 
            
            img_w = img.imageWidth
            img_h = img.imageHeight
            
            # Sécurité pour éviter division par zéro
            if img_w > 0:
                aspect = img_h / float(img_w)
            else:
                aspect = 1.0

            if aspect > (avail_height / avail_width):
                # Limité par la hauteur
                img.drawHeight = avail_height
                img.drawWidth = avail_height / aspect
            else:
                # Limité par la largeur
                img.drawWidth = avail_width
                img.drawHeight = avail_width * aspect
            
            elements.append(img)
        except Exception:
            elements.append(Paragraph("<i>(Schéma non disponible)</i>", header_info_style))

    elements.append(Spacer(1, 0.5*cm))

    # =================== 4. PRIX TOTAL UNIQUEMENT ===================
    # On affiche uniquement le gros prix total, aligné à droite
    montant_ttc = f"{prix_details['total_ttc']:.2f} €"
    elements.append(Paragraph(f"PRIX TOTAL TTC : {montant_ttc}", price_style))
    
    # Ligne de séparation
    elements.append(Paragraph("<hr width='100%' color='black'/>", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # =================== 5. BAS DE PAGE (COLONNES) ===================
    
    # Colonne Gauche
    col_gauche = []
    col_gauche.append(Paragraph("Ce que le tarif comprend :", column_header_style))
    inclus_items = [
        "Livraison bas d'immeuble",
        "Fabrication 100% artisanale France",
        "Choix du tissu n'impacte pas le devis",
        "Paiement 2 à 6 fois sans frais",
        "Livraison 5 à 7 semaines",
        "Housses déhoussables"
    ]
    for item in inclus_items:
        col_gauche.append(Paragraph(f"• {item}", detail_style))

    # Colonne Droite
    col_droite = []
    col_droite.append(Paragraph("Détail des cotations :", column_header_style))
    
    h_mousse = config['options'].get('epaisseur', 25)
    h_assise = 46 if h_mousse > 20 else 40
    
    cotations_items = [
        "Accoudoir: 15cm large / 60cm haut",
        "Dossier: 10cm large / 70cm haut",
        "Coussins: 65/80/90cm large",
        f"Profondeur assise: {config['dimensions']['profondeur']} cm",
        f"Hauteur assise: {h_assise} cm (Mousse {h_mousse}cm)"
    ]
    for item in cotations_items:
        col_droite.append(Paragraph(f"• {item}", detail_style))

    # Tableau pour les colonnes
    table_footer = Table([[col_gauche, col_droite]], colWidths=[9.5*cm, 9.5*cm])
    table_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(table_footer)
    
    # =================== 6. FOOTER ===================
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("FRÉVENT 62270", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
