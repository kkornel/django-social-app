from django.core.mail import send_mail

from djangoapp.settings import EMAIL_FROM_EMAIL

# def send_reset_password_email(user):
#     token = user.get_token(3600,
#                            current_app.config['SECURITY_RESET_PASSWORD_SALT'])
#     reset_url = url_for('users.reset_password_token',
#                         token=token,
#                         _external=True)
#     html = render_template('users/mail_reset_password.html',
#                            reset_url=reset_url)
#     subject = 'Password Reset Request'
#     send_email(user.email, subject, html)

# def send_verification_email(user):
#     token = user.get_token(None,
#                            current_app.config['SECURITY_VERIFY_EMAIL_SALT'])
#     confirm_url = url_for('users.confirm_email', token=token, _external=True)
#     html = render_template('users/mail_verify_email.html',
#                            confirm_url=confirm_url)
#     subject = 'Please confirm your email'
#     send_email(user.email, subject, html)


def send_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        EMAIL_FROM_EMAIL,
        [to_email],
        fail_silently=False,
        html_message=message,
    )
