import io
from fpdf import FPDF
from pypdf import PdfWriter, PdfReader
from pypdf.generic import DictionaryObject, NameObject, TextStringObject
from .common import register_token, random_creation_date, random_modification_date

def generate_pdf_honeytoken(server_url, output_file, description, title=None, author=None, content=None):
    """
    Genera un PDF con una OpenAction que redirige a un URL de tracking.
    """
    token_data = register_token(
        server_url, 
        token_type="pdf",
        description=description
    )
    tracking_url = token_data['tracking_url_link']

    # Creamos el PDF (con su título y contenido) usando la librería FPDF
    pdf = FPDF()
    pdf.add_page()

    # Escribimos en el PDF
    if title:
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(0, 20, title, ln=1, align='L')
    if content:
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, content)

    # Convertimos el PDF (creado con FPDF) para que pypdf pueda manipularlo
    pdf_buffer_str = pdf.output(dest='S')
    pdf_bytes = io.BytesIO(pdf_buffer_str.encode('latin-1'))

    # Usamos pypdf
    reader = PdfReader(pdf_bytes)
    writer = PdfWriter()

    writer.append_pages_from_reader(reader)
    
    # Agregamos metadata para que parezca más legítimo
    metadata = {}
    if title:
        metadata['/Title'] = title
    if author:
        metadata['/Author'] = author

    fake_creator = "Acrobat Pro 15.8.20082"
    metadata['/Creator'] = fake_creator
    metadata['/Producer'] = fake_creator

    # Fechas de creación y modificación
    c_date_iso = random_creation_date()
    m_date_iso = random_modification_date(c_date_iso)
    # Las convertimos a formato PDF (D:YYYYMMDDHHmmSSZ)
    c_date_pdf = f"D:{c_date_iso.replace('-', '').replace(':', '').replace('T', '')}"
    m_date_pdf = f"D:{m_date_iso.replace('-', '').replace(':', '').replace('T', '')}"

    metadata['/CreationDate'] = c_date_pdf
    metadata['/ModDate'] = m_date_pdf

    if metadata:
        writer.add_metadata(metadata)

    
    # Inyectamos la OpenAction
    uri_action = DictionaryObject({
        NameObject("/S"): NameObject("/URI"),
        NameObject("/URI"): TextStringObject(tracking_url)
    })
    writer._root_object.update({
        NameObject("/OpenAction"): uri_action
    })

    # Guardamos el PDF
    with open(output_file, "wb") as f:
        writer.write(f)