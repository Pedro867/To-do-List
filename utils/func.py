import smtplib
from email.message import EmailMessage
from functools import wraps
import os
from flask import redirect, url_for, session

def enviar_email(nome_usuario, email_destino):
    EMAIL_ORIGEM = os.getenv('EMAIL_ORIGEM')
    SENHA_APP    = os.getenv('SENHA_APP')

    msg = EmailMessage()
    msg['Subject'] = "Perfil Atualizado com Sucesso!"
    msg['From']    = EMAIL_ORIGEM
    msg['To']      = email_destino

    html_content = f"""
    <html>
        <body>
            <h2 style="color: #1e293b;">Olá, {nome_usuario}!</h2>
            <p>Seus dados de perfil foram atualizados em nosso sistema.</p>
            <p>Se você não realizou esta alteração, entre em contato com o suporte.</p>
            <hr>
            <footer style="font-size: 0.8em; color: gray;">Equipe Python Automation</footer>
        </body>
    </html>
    """
    msg.set_content("Seu perfil foi atualizado.")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ORIGEM, SENHA_APP)
        smtp.send_message(msg)

def valida_email(email):
    from email_validator import validate_email, EmailNotValidError
    try:
        email_dados = validate_email(email)
        email = email_dados.normalized
    except EmailNotValidError as e:
        return str(e)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function