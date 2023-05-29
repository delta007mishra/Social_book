# # from django.contrib.auth.password_validation import BaseValidator
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _


# class UppercaseLowercaseValidator(BaseValidator):
#     def validate(self, password, user=None):
#         if not any(char.isupper() for char in password):
#             raise ValidationError(
#                 _("The password must contain at least one uppercase letter."),
#                 code='password_no_upper',
#             )
#         if not any(char.islower() for char in password):
#             raise ValidationError(
#                 _("The password must contain at least one lowercase letter."),
#                 code='password_no_lower',
#             )

#     def get_help_text(self):
#         return _(
#             "Your password must contain at least one uppercase letter and one lowercase letter."
#         )



















# from django.contrib.auth.password_validation import get_password_validators
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# class UppercaseLowercaseValidator:
#     def validate(self, password, user=None):
#         validators = get_password_validators()

#         for validator in validators:
#             try:
#                 validator.validate(password, user)
#             except ValidationError as e:
#                 if validator.__class__.__name__ in ['UppercaseValidator', 'LowercaseValidator']:
#                     raise ValidationError(e)

#     def get_help_text(self):
#         return "Ensure the password contains at least one uppercase letter and one lowercase letter."

#     def get_validator_config(self):
#         return None