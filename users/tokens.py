import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
"""
Django has internal APIs for creating One Time Link with users details. 
PasswordResetTokenGenerator API is used for generating token. 
Extend PasswordResetTokenGenerator to generate a unique token. 
This will make use of SECRET_KEY of current project.
"""


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active))


account_activation_token = TokenGenerator()
