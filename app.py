from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'clave-secreta'  


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'instalacionesyeminus@gmail.com'
EMAIL_PASSWORD = 'mfjsthdtvacefkft'  

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        notas = request.form['notas']
        tipo_una = request.form['tipo_una']
        telefono = request.form['telefono']
        date = request.form ['date']
        hora = request.form ['date']

        asunto = "Nuevo formulario enviado"

        try:
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8">
                <style>
                  body {{
                    font-family: Arial, sans-serif;
                    background-color: 
                    padding: 20px;
                    color: 
                  }}
                  .card {{
                    background-color: 
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                  }}
                  .field {{
                    margin: 10px 0;
                  }}
                  .label {{
                    font-weight: bold;
                  }}
                </style>
              </head>
              <body>
                <div class="card">
                  <h2>📋 Nueva cita agendada</h2>
                  <div class="field"><span class="label">👤 Nombre:</span> {nombre}</div>
                  <div class="field"><span class="label">📧 Email:</span> {email}</div>
                  <div class="field"><span class="label">💅 Servicio:</span> {tipo_una}</div>
                  <div class="field"><span class="label">📝 Notas:</span> {notas or 'Ninguna'}</div>
                  <div class="field"><span class="label">📱 telefono:</span> {telefono}</div>
                  <div class="field"><span class="label">📅 date:</span> {date}</div>
                  <div class="field"><span class="label">🕜 hora:</span> {hora}</div>
                  
                </div>
              </body>
            </html>
            """

            
            msg = MIMEMultipart("alternative")
            msg['Subject'] = asunto
            msg['From'] = EMAIL_FROM
            msg['To'] = email

            
            msg.attach(MIMEText(html_body, "html"))

            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.send_message(msg)

            flash('Cita agendada. Revise su correo y Google Calendar.', 'success')

        except Exception as e:
            print("Error al enviar el correo:", e)
            flash('Error al enviar el correo.', 'danger')

        return redirect('/')

    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
