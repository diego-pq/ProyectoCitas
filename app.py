# Importaciones de Flask para la aplicación web
from flask import Flask, render_template, request, redirect, flash

# Importaciones para el envío de correos electrónicos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Configuración de la aplicación Flask ---
app = Flask(__name__)
app.secret_key = 'clave-secreta'

# --- Configuración para el envío de correos electrónicos ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'citareservar@gmail.com'
EMAIL_PASSWORD = 'vdwryhwagulbhvak'

# --- Ruta principal con el formulario ---
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        notas = request.form['notas']
        tipo_una = request.form['tipo_una']
        telefono = request.form['telefono']
        date = request.form['date']
        hora = request.form['hora']

        # --- Envío de correo electrónico ---
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

        # --- Mensajes flash según resultado del correo ---
        if email_sent:
            flash('Cita agendada y correo de confirmación enviado.', 'success')
        else:
            flash('Hubo un error al enviar el correo de confirmación.', 'danger')

        return redirect('/reserva_exitosa')

    return render_template('form.html')

# --- Ruta para la página de confirmación ---
@app.route('/reserva_exitosa')
def reserva_exitosa():
    return render_template('reserva_exitosa.html')

# --- Inicio de la aplicación ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
