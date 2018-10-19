import datetime
import io
import os
import shutil
import urllib.request

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

dateToday = datetime.date.today()

# Change these values -----------------------------
userData = {
    'studiengang': 'Informationstechnik',
    'seminargruppe': '3IT16-1',
    'nachname': 'Grundig',
    'vorname': 'Hans',
    'anschrift': 'Hans-Grundig-Straße 25, 01307 Dresden',
    'semester': '4',
    'modul': '3IM-SWEE-00',
    'anzPruefungsteile': '1',
    'dringlichkeit': 'nein',
    'datum': dateToday.strftime("%d.%m.%Y")
}
# ---------------------------------------------------

url = 'http://www.ba-dresden.de/fileadmin/dresden/downloads/zentrale-dokumente/Formular_Antrag_auf_Einsicht_in_Pruefungsunterlagen_2015_12_11.pdf'
file_name = 'Antrag_Pruefungseinsicht' + '_' + userData['nachname'] + '.pdf'

# Download file from `url` and save as tempFile:
with urllib.request.urlopen(url) as response, open('tempFile.pdf', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

packet = io.BytesIO()
# create a new PDF with ReportLab
can = canvas.Canvas(packet, pagesize=A4)
can.setFont('Helvetica', 12)
can.drawString(140, 665, userData['studiengang'])
can.drawString(480, 665, userData['seminargruppe'])
can.drawString(110, 642, userData['nachname'])
can.drawString(355, 642, userData['vorname'])
can.drawString(230, 619, userData['anschrift'])
can.drawString( 90, 395, userData['semester'])
can.drawString(130, 395, userData['modul'])
can.drawString(350, 395, userData['anzPruefungsteile'])
can.drawString(450, 395, userData['dringlichkeit'])
can.drawString(110, 350, userData['datum'])
can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open('tempFile.pdf', 'rb'))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(file_name, "wb")
output.write(outputStream)
outputStream.close()

# delete tempFile
os.remove('tempFile.pdf')
