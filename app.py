from flask import Flask, render_template, request, redirect, flash, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'clave-secreta'

# --- Configuración para correo ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'citareservar@gmail.com'
EMAIL_PASSWORD = 'vdwryhwagulbhvak'

# --- Página inicial ---
@app.route('/')
def inicio():
    return render_template('inicio.html')

# --- Formulario de agendamiento ---
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        notas = request.form['notas']
        tipo_una = request.form['tipo_una']
        telefono = request.form['telefono']
        date = request.form['date']
        hora = request.form['hora']

        email_sent = False
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM
            msg['To'] = email
            msg['Subject'] = 'Confirmación de Cita'

            body = f"""
            Hola {nombre},

            Tu cita ha sido agendada con éxito.

            🗓 Fecha: {date}
            ⏰ Hora: {hora}
            💅 Servicio: {tipo_una}
            📞 Teléfono: {telefono}
            📋 Notas: {notas or 'Ninguna'}

            ¡Gracias por agendar con nosotros!
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            email_sent = True
        except Exception as e:
            print("Error al enviar el correo:", e)
            email_sent = False

        if email_sent:
            flash('Cita agendada y correo de confirmación enviado.', 'success')
        else:
            flash('Hubo un error al enviar el correo de confirmación.', 'danger')

        return redirect(url_for('reserva_exitosa'))

    return render_template('form.html')

# --- Confirmación ---
@app.route('/reserva_exitosa')
def reserva_exitosa():
    return render_template('reserva_exitosa.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
