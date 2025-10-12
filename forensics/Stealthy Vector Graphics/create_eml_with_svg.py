# create_eml_with_svg.py
from email.message import EmailMessage
from email.utils import formatdate
import mimetypes

# Read SVG content
with open("suspicious.svg", "rb") as f:
    svg_data = f.read()

# Create the email
msg = EmailMessage()
msg['From'] = 'rob.banks1337@payyourpal.com'
msg['To'] = 'oparker@e-corp.com'
msg['Subject'] = 'URGENT: Payment Missed'
msg['Date'] = formatdate(localtime=True)

msg.set_content("""\
Hi,

According to our records, you have missed a payment of:
                
$927.84 USD
                
Please find the attached invoice and pay as soon as possible.

Best,
PayYourPal
""")

# Guess the MIME type of the SVG file
mime_type, _ = mimetypes.guess_type("suspicious.svg")
maintype, subtype = mime_type.split('/')

# Attach the SVG
msg.add_attachment(svg_data, maintype=maintype, subtype=subtype, filename="invoice.pdf.svg")

# Save to .eml
with open("challenge_email.eml", "wb") as f:
    f.write(msg.as_bytes())

print("✅ challenge_email.eml created.")
