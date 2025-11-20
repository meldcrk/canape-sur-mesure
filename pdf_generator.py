"""
Module de génération de devis PDF
Utilise reportlab pour créer des PDF professionnels
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generer_pdf_devis(config, prix_details):
    """
    Génère un PDF de devis professionnel
    
    Args:
        config: Dictionnaire avec la configuration du canapé
        prix_details: Dictionnaire avec les détails de prix
    
    Returns:
        BytesIO: Buffer contenant le PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Conteneur pour les éléments du PDF
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les sections
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=8,
        spaceBefore=4,
        leftIndent=0
    )
    
    # Style pour les détails techniques
    detail_style = ParagraphStyle(
        'DetailStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        spaceAfter=4,
        leftIndent=10
    )
    
    # Style pour le footer
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    # =================== TITRE ===================
    titre = Paragraph("MON CANAPÉ MAROCAIN", title_style)
    elements.append(titre)
    elements.append(Spacer(1, 0.8*cm))
    
    # =================== DIMENSIONS DU CANAPÉ ===================
    type_canape = config['type_canape']
    dimensions = config['dimensions']
    
    # Déterminer le format des dimensions selon le type
    if "Simple" in type_canape or "S" in type_canape:
        dim_text = f"<b>Dimensions du canapé :</b> {dimensions['tx']}cm"
    elif "L" in type_canape:
        dim_text = f"<b>Dimensions du canapé :</b> {dimensions['ty']}x{dimensions['tx']}cm"
    else:  # U
        dim_text = f"<b>Dimensions du canapé :</b> {dimensions['ty']}x{dimensions['tx']}x{dimensions['tz']}cm"
    
    elements.append(Paragraph(dim_text, section_style))
    
    # =================== CARACTÉRISTIQUES ===================
    profondeur_text = f"<b>Profondeur :</b> {dimensions['profondeur']}cm"
    elements.append(Paragraph(profondeur_text, section_style))
    
    # Type de mousse
    mousse = config['options'].get('type_mousse', 'D25')
    mousse_text = f"<b>Mousse :</b> {mousse}"
    elements.append(Paragraph(mousse_text, section_style))
    
    # Dossiers
    has_dossier = (config['options'].get('dossier_left', False) or 
                   config['options'].get('dossier_bas', False) or 
                   config['options'].get('dossier_right', False))
    dossier_text = f"<b>Dossier :</b> {'Avec' if has_dossier else 'Sans'}"
    elements.append(Paragraph(dossier_text, section_style))
    
    # Accoudoirs
    nb_accoudoirs = sum([
        config['options'].get('acc_left', False),
        config['options'].get('acc_right', False),
        config['options'].get('acc_bas', False)
    ])
    accoudoir_text = f"<b>Accoudoirs :</b> {nb_accoudoirs}"
    elements.append(Paragraph(accoudoir_text, section_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # =================== INFORMATIONS CLIENT ===================
    if config['client']['nom']:
        nom_text = f"<b>Nom :</b> {config['client']['nom']}"
        elements.append(Paragraph(nom_text, section_style))
        
        if config['client']['email']:
            email_text = f"<b>Email :</b> {config['client']['email']}"
            elements.append(Paragraph(email_text, section_style))
    
    elements.append(Spacer(1, 1*cm))
    
    # =================== LIGNE DE SÉPARATION ===================
    line_data = [['', '']]
    line_table = Table(line_data, colWidths=[17*cm, 0])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#3498DB')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # =================== INCLUS DANS LE TARIF REMISÉ ===================
    inclus_title = Paragraph("<b>Le tarif remisé comprend :</b>", section_style)
    elements.append(inclus_title)
    elements.append(Spacer(1, 0.3*cm))
    
    inclus_items = [
        "📦 la livraison en bas d'immeuble",
        "🛋️ la fabrication 100% artisanal et en France",
        "✨ le choix du tissu n'impacte pas le devis",
        "👍🏻 possibilité de régler de 2 à 6 fois sans frais",
        "😁 délai de livraison entre 5 à 7 semaines",
        "🌱 les housses de matelas et coussins déhoussables"
    ]
    
    for item in inclus_items:
        elements.append(Paragraph(f"• {item}", detail_style))
    
    elements.append(Spacer(1, 0.8*cm))
    
    # =================== DÉTAIL DES COTATIONS ===================
    cotations_title = Paragraph("<b>Voici le détail des cotations de votre canapé :</b>", section_style)
    elements.append(cotations_title)
    elements.append(Spacer(1, 0.3*cm))
    
    cotations_items = [
        "• accoudoir : 15cm de largeur, 60cm de hauteur",
        "• dossier : 10cm de largeur, 70cm de hauteur",
        "• coussins : 65cm, 80cm, 90cm de largeur, 45cm de hauteur",
        "• profondeur d'assise : 70cm (possibilité de faire sur mesure)",
        "• hauteur d'assise : 46cm",
        "• hauteur de mousse : 25 cm"
    ]
    
    for item in cotations_items:
        elements.append(Paragraph(item, detail_style))
    
    elements.append(Spacer(1, 1*cm))
    
    # =================== TABLEAU DES PRIX ===================
    # Titre du tableau
    prix_title = Paragraph("<b>DÉTAIL DU DEVIS</b>", section_style)
    elements.append(prix_title)
    elements.append(Spacer(1, 0.3*cm))
    
    # Préparer les données du tableau
    prix_data = [['Désignation', 'Prix (€)']]
    
    for item, prix in prix_details['details'].items():
        prix_data.append([item, f"{prix:.2f} €"])
    
    # Ligne de sous-total
    prix_data.append(['', ''])
    prix_data.append(['SOUS-TOTAL HT', f"{prix_details['sous_total']:.2f} €"])
    prix_data.append(['TVA (20%)', f"{prix_details['tva']:.2f} €"])
    prix_data.append(['', ''])
    
    # Ligne de total
    prix_data.append(['TOTAL TTC', f"{prix_details['total_ttc']:.2f} €"])
    
    # Créer le tableau
    table_prix = Table(prix_data, colWidths=[12*cm, 5*cm])
    
    # Style du tableau
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]
    
    # Style pour le sous-total
    sous_total_row = len(prix_data) - 4
    table_style.extend([
        ('FONTNAME', (0, sous_total_row), (-1, sous_total_row + 1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, sous_total_row), (-1, sous_total_row), 1, colors.black),
    ])
    
    # Style pour le total
    total_row = len(prix_data) - 1
    table_style.extend([
        ('FONTNAME', (0, total_row), (-1, total_row), 'Helvetica-Bold'),
        ('FONTSIZE', (0, total_row), (-1, total_row), 14),
        ('BACKGROUND', (0, total_row), (-1, total_row), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, total_row), (-1, total_row), colors.whitesmoke),
        ('LINEABOVE', (0, total_row), (-1, total_row), 2, colors.black),
    ])
    
    table_prix.setStyle(TableStyle(table_style))
    elements.append(table_prix)
    elements.append(Spacer(1, 1.5*cm))
    
    # =================== FOOTER ===================
    footer_text = Paragraph("<b>FRÉVENT 62270</b>", footer_style)
    elements.append(footer_text)
    
    # Générer le PDF
    doc.build(elements)
    
    # Retourner le buffer
    buffer.seek(0)
    return buffer
