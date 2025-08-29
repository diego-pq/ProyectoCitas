# Importaciones de Flask para la aplicación web
from flask import Flask, render_template, request, redirect, flash

# Importaciones para el envío de correos electrónicos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Importaciones para la API de Google Calendar
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuración de la aplicación Flask ---
app = Flask(__name__)
app.secret_key = 'clave-secreta'

# --- Configuración para el envío de correos electrónicos (tu código existente) ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'citareservar@gmail.com'
EMAIL_PASSWORD = 'vdwryhwagulbhvak'

# --- Configuración y función para la API de Google Calendar ---
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_creds():
    """Obtiene y refresca las credenciales de Google."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_calendar_event(start_time_str, summary_text, description_text, attendees_list):
    """
    Crea un evento en Google Calendar con invitados.
    
    Args:
        start_time_str (str): La fecha y hora de inicio del evento.
        summary_text (str): El título del evento.
        description_text (str): La descripción del evento.
        attendees_list (list): Una lista de diccionarios con los correos de los invitados.
    """
    creds = get_google_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        start_time = datetime.datetime.fromisoformat(start_time_str)
        end_time = start_time + datetime.timedelta(hours=1)
        
        event = {
            'summary': summary_text,
            'description': description_text,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'attendees': attendees_list,
        }

        event = service.events().insert(
            calendarId='primary', 
            body=event,
            sendUpdates='all' 
        ).execute()
        
        print(f"Evento creado: {event.get('htmlLink')}")
        return True
    except HttpError as error:
        print(f"Ocurrió un error en la API de Google: {error}")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return False

# --- Ruta principal de la aplicación ---
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

        # Tu código existente para el envío de correo
        email_sent = False
        try:
            # ... (tu código para enviar el correo) ...
            email_sent = True
        except Exception as e:
            print("Error al enviar el correo:", e)
            email_sent = False

        # --- LÓGICA ACTUALIZADA: Crear evento con invitados estáticos y dinámicos ---
        calendar_event_created = False
        try:
            fecha_hora_completa = f"{date}T{hora}:00"
            summary_text = f"Cita con {nombre}"
            description_text = f"Servicio: {tipo_una}\nTeléfono: {telefono}\nNotas: {notas or 'Ninguna'}"
            
            # --- Preparar la lista de invitados ---

            attendees_list = [
                {'email': email},  # Correo del cliente
                # {'email': 'julanito333@gmail.com'},  # correo estático

            ]
            
            calendar_event_created = create_calendar_event(fecha_hora_completa, summary_text, description_text, attendees_list)
        except Exception as e:
            print("Error al crear el evento de Google Calendar:", e)
            
        # Lógica para los mensajes flash
        if email_sent and calendar_event_created:
            flash('Cita agendada. Se envió un correo y se creó un evento en Google Calendar.', 'success')
        elif email_sent:
            flash('Cita agendada, pero hubo un error al crear el evento en Google Calendar. Revise la consola del servidor.', 'warning')
        elif calendar_event_created:
            flash('Se creó un evento en Google Calendar, pero hubo un error al enviar el correo.', 'warning')
        else:
            flash('Hubo un error al agendar la cita. No se pudo enviar el correo ni crear el evento en Google Calendar.', 'danger')

        return redirect('/')

    return render_template('form.html')

if __name__ == '__main__':
    print("Iniciando proceso de autenticación de Google...")
    try:
        get_google_creds()
        print("Autenticación de Google exitosa. Ahora puedes usar el formulario.")
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        print("Asegúrate de que tu archivo 'credentials.json' esté en el directorio correcto.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
