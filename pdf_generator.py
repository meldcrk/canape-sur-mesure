from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import datetime

def generate_pdf(
    output_path: str,
    dimensions: str,
    profondeur: str,
    mousse: str,
    dossier: str,
    accoudoirs: str,
    nom: str,
    email: str
):

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["BodyText"]

    story = []

    # -------------------------------------------------------------------------
    # TITRE
    # -------------------------------------------------------------------------
    story.append(Paragraph("MON CANAPÉ MAROCAIN", title_style))
    story.append(Spacer(1, 16))

    # -------------------------------------------------------------------------
    # INFORMATIONS DU CANAPÉ / CLIENT
    # -------------------------------------------------------------------------
    info_text = f"""
    <b>Dimensions du canapé :</b> {dimensions} <br/>
    <b>Profondeur :</b> {profondeur} cm <br/>
    <b>Mousse :</b> {mousse} <br/>
    <b>Dossier :</b> {dossier} <br/>
    <b>Accoudoirs :</b> {accoudoirs} <br/>
    <b>Nom :</b> {nom} <br/>
    <b>Email :</b> {email} <br/>
    """

    story.append(Paragraph(info_text, normal_style))
    story.append(Spacer(1, 20))

    # -------------------------------------------------------------------------
    # TARIF REMISÉ
    # -------------------------------------------------------------------------
    tarif_text = """
    Il faut savoir que le tarif remisé comprend : <br/>
    - la livraison en bas d’immeuble 📦 <br/>
    - la fabrication 100% artisanal et en France 🛋️ <br/>
    - le choix du tissu n’impacte pas le devis ✨ <br/>
    - possibilité de régler de 2 à 6 fois sans frais 👍🏻 <br/>
    - délai de livraison entre 5 à 7 semaines 😁 <br/>
    - et les housses de matelas et coussins déhoussables 🌱 <br/>
    """
    story.append(Paragraph(tarif_text, normal_style))
    story.append(Spacer(1, 20))

    # -------------------------------------------------------------------------
    # COTATIONS
    # -------------------------------------------------------------------------
    cotations_text = """
    <b>Voici le détail des cotations de votre canapé :</b><br/>
    - accoudoir : 15cm de largeur, 60cm de hauteur<br/>
    - dossier : 10cm de largeur, 70cm de hauteur<br/>
    - coussins : 65cm, 80cm, 90cm de largeur, 45cm de hauteur<br/>
    - profondeur d'assise : 70cm (possibilité de faire sur mesure)<br/>
    - hauteur d'assise : 46cm<br/>
    - hauteur de mousse : 25 cm<br/>
    """
    story.append(Paragraph(cotations_text, normal_style))
    story.append(Spacer(1, 20))

    # -------------------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------------------
    story.append(Paragraph("FRÉVENT 62270", normal_style))
    story.append(Spacer(1, 12))

    date_text = datetime.datetime.now().strftime("PDF généré le %d/%m/%Y à %H:%M")
    story.append(Paragraph(date_text, normal_style))

    # -------------------------------------------------------------------------
    # GÉNÉRATION
    # -------------------------------------------------------------------------
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    pdf.build(story)

    return output_path
