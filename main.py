from fastapi import FastAPI, Form
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from reportlab.lib.units import inch
from fastapi.responses import StreamingResponse
from reportlab.lib.utils import simpleSplit
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from pathlib import Path


import os

app = FastAPI()

PDF_MAP = {
    'nsa_sra_gracas.pdf': 'Nossa Senhora das Graças',
    'nsa_sra_aparecida.pdf': 'Nossa Senhora Aparecida'
}



app = FastAPI()

# Set up the templates directory for Jinja2
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Path to the folder with base PDF templates
BASE_PDF_DIR = Path("pdf_files")

@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "pdf_files": PDF_MAP})

def _get_consacration_text(text):
    return f"""Dou-Vos graças por Vos terdes aniquilado a Vós mesmo, tomando a forma de escravo, para livrar-me da cruel escravidão do demônio. Eu Vos louvo e glorifico por Vos terdes querido submeter em tudo a Maria, Vossa Mãe Santíssima, a fim de, por Ela, tornar-me Vosso fiel escravo.
    Entretanto, ai de mim, criatura ingrata e infiel! Não guardei os votos e promessas que tão solenemente Vos fiz no meu Batismo. Não cumpri as minhas obrigações; não mereço ser chamado Vosso filho, nem Vosso escravo; e, como nada há em mim que não mereça a Vossa repulsa e a Vossa cólera, não ouso aproximar-me por mim mesmo da Vossa Santíssima e Augustíssima Majestade.
    Recorro, pois, à intercessão e à misericórdia de Vossa Mãe Santíssima, que me destes por medianeira junto de Vós. É por intermédio d'Ela que espero obter de Vós a contrição e o perdão dos meus pecados, a aquisição e conservação da Sabedoria. Ave, pois, ó Maria Imaculada, Tabernáculo Vivo da Divindade, onde a Eterna Sabedoria escondida quer ser adorada pelos anjos e pelos homens. 
    Ave, ó Rainha do Céu e da Terra, a cujo Império é submetido tudo o que há abaixo de Deus. Ave, ó Seguro Refúgio dos pecadores, cuja misericórdia a ninguém despreza. Atendei ao desejo que tenho da Divina Sabedoria, e recebei, para isso, os votos e ofertas apresentados pela minha baixeza.
    Eu, {text}, infiel pecador, renovo e ratifico hoje, nas Vossas mãos, as promessas do meu Batismo: renuncio para sempre a Satanás, às suas pompas e suas obras, e dou-me inteiramente a Jesus Cristo, a Sabedoria Encarnada, para o seguir, levando a minha Cruz, todos os dias da minha vida. E para lhe ser mais fiel do que até agora tenho sido, escolho-Vos hoje, ó Maria, na presença de toda a Corte Celeste, por minha Mãe e Senhora. 
    Entrego-Vos e consagro-Vos, na qualidade de escravo, o meu corpo e a minha alma, os meus bens interiores e exteriores, e o próprio valor das minhas boas obras passadas, presentes e futuras, deixando-Vos pleno e inteiro direito de dispor de mim e de tudo o que me pertence, sem exceção alguma, segundo o Vosso agrado e para maior glória de Deus, no tempo e na eternidade.
    Recebei, ó Benigníssima Virgem, esta pequenina oferta da minha escravidão, em união e em honra à submissão que a Sabedoria Eterna quis ter à Vossa Maternidade; em homenagem ao poder que ambos tendes sobre este vermezinho e miserável pecador; em ação de graças pelos privilégios com que largamente Vos favoreceu a Trindade Santíssima. 
    Protesto que quero, de hoje em diante e firmemente, como Vosso verdadeiro escravo, buscar a Vossa honra e obedecer-Vos em todas as coisas.
    Ó Mãe Admirável, apresentai-me ao Vosso amado Filho na condição de escravo perpétuo, a fim de que, tendo-me resgatado por Vós, por Vós também me receba propiciamente.
    Ó Mãe de Misericórdia, concedei-me a graça de obter a Verdadeira Sabedoria de Deus, e de colocar-me, para isso, entre o número daqueles que amais, ensinais, guiais, sustentais e protegeis como filhos e escravos Vossos.
    Ó Virgem Fiel, tornai-me em tudo um tão perfeito discípulo, imitador e escravo da Sabedoria Encarnada, Jesus Cristo, Vosso Filho, que eu chegue um dia, por Vossa intercessão e a Vosso exemplo, à plenitude da sua idade na Terra e da sua glória no Céu. Amém. Assim seja."""

@app.post("/generate_consacration_file/")
async def generate_consacration_file(name: str = Form(...), pdf_template: str = Form(...)):
    # Step 1: Read the existing PDF from the server
    pdf_path = f"pdf_files/{pdf_template}"
    if not os.path.exists(pdf_path):
        return {"error": "PDF file not found on the server"}

    pdf_text = _get_consacration_text(name)

    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        pdf_writer = PdfWriter()

        # Step 2: Add text to the first page
        buffer = BytesIO()
        can = canvas.Canvas(buffer, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Palatino', 'pala.ttf'))
            
        # Step 1: Set margins (1 inch on all sides)
        left_margin = 0.25 * inch
        right_margin = 0.25 * inch
        top_margin = 8.3 * inch  # Starting from near the top of the page

        # Step 2: Set the font to Palatino with size 11
        can.setFont("Palatino", 11)

        # Step 3: Define paragraph indentation (e.g., 0.5 inch)
        paragraph_indent = 0.5 * inch

        max_width = 8.5 * inch - left_margin - right_margin  # Page width minus the margins

        # Create a text object starting at the left margin and top margin
        text_object = can.beginText(left_margin, top_margin)

        # Step 4: Split text into paragraphs and add indentation for the first line
        paragraphs = pdf_text.split("\n")  # Assuming paragraphs are separated by double line breaks


        for para in paragraphs:
            # Step 5: Split the paragraph into lines that fit within the specified width
            lines = simpleSplit(para, "Palatino", 11, max_width)

            # Indent the first line of each paragraph
            first_line = " " * 4 + lines[0]  # Add spaces to indent the first line

            # Add the first line with indentation
            text_object.textLine(first_line)

            # Add the remaining lines (without indentation)
            for line in lines[1:]:
                text_object.textLine(line)

            # Add some space between paragraphs
            text_object.moveCursor(0, 2)  
            
        can.drawText(text_object)
        # Save the canvas
        can.save()

        # Step 3: Merge the new text onto the first page of the uploaded PDF
        buffer.seek(0)
        new_pdf = PdfReader(buffer)

        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            if i == 0:  # Merge only on the first page
                page.merge_page(new_pdf.pages[0])
            pdf_writer.add_page(page)

        # Step 4: Write the modified PDF to a buffer
        output_buffer = BytesIO()
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        file_name = f"{name.split(' ')[0].lower()}_consagracao_{pdf_template}"
        # Return the modified PDF as a downloadable file
        headers = {
            "Content-Disposition": f"attachment; filename={file_name}",
        }

        return StreamingResponse(output_buffer, headers=headers, media_type="application/pdf")


# Running FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
