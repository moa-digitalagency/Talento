"""
Service de validation pour emails et numéros de téléphone
Utilise email-validator et phonenumbers pour une validation production-ready
"""

from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
import re


class ValidationResult:
    """Classe pour encapsuler le résultat d'une validation"""
    def __init__(self, is_valid, normalized_value=None, error_message=None, details=None):
        self.is_valid = is_valid
        self.normalized_value = normalized_value
        self.error_message = error_message
        self.details = details or {}
    
    def __bool__(self):
        return self.is_valid


class EmailValidator:
    """Validateur d'email avec vérification de délivrabilité"""
    
    @staticmethod
    def validate(email_str, check_deliverability=True):
        """
        Valide un email et le normalise
        
        Args:
            email_str: L'email à valider
            check_deliverability: Si True, vérifie que le domaine existe (DNS check)
        
        Returns:
            ValidationResult avec email normalisé ou message d'erreur
        """
        if not email_str:
            return ValidationResult(
                is_valid=False,
                error_message="L'email est requis"
            )
        
        try:
            # Validation complète avec vérification DNS
            emailinfo = validate_email(
                email_str, 
                check_deliverability=check_deliverability
            )
            
            # Normaliser l'email (minuscules, format standard)
            normalized = emailinfo.normalized
            
            return ValidationResult(
                is_valid=True,
                normalized_value=normalized,
                details={
                    'domain': emailinfo.domain,
                    'local_part': emailinfo.local_part,
                    'ascii_email': emailinfo.ascii_email
                }
            )
            
        except EmailNotValidError as e:
            # Messages d'erreur en français pour l'utilisateur
            error_messages = {
                'The email address is not valid': "L'adresse email n'est pas valide",
                'The domain name': "Le nom de domaine",
                'does not exist': "n'existe pas",
                'The part after the @-sign': "La partie après le @",
                'is not valid': "n'est pas valide",
                'The email address contains invalid characters': "L'email contient des caractères invalides"
            }
            
            error_str = str(e)
            french_error = error_str
            
            # Traduire les erreurs courantes
            for eng, fr in error_messages.items():
                french_error = french_error.replace(eng, fr)
            
            return ValidationResult(
                is_valid=False,
                error_message=french_error
            )


class PhoneValidator:
    """Validateur de numéro de téléphone international"""
    
    @staticmethod
    def validate(phone_str, default_region='MA'):
        """
        Valide un numéro de téléphone et le normalise au format international
        
        Args:
            phone_str: Le numéro de téléphone à valider
            default_region: Code pays ISO pour parser le numéro (défaut: MA pour Maroc)
        
        Returns:
            ValidationResult avec numéro formaté en E.164 ou message d'erreur
        """
        if not phone_str:
            return ValidationResult(
                is_valid=False,
                error_message="Le numéro de téléphone est requis"
            )
        
        # Nettoyer le numéro (enlever espaces et tirets)
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone_str)
        
        try:
            # Parser le numéro avec la région par défaut
            parsed_number = phonenumbers.parse(cleaned_phone, default_region)
            
            # Vérifier si le numéro est valide
            if not phonenumbers.is_valid_number(parsed_number):
                return ValidationResult(
                    is_valid=False,
                    error_message="Le numéro de téléphone n'est pas valide pour cette région"
                )
            
            # Vérifier si le numéro est possible (format correct)
            if not phonenumbers.is_possible_number(parsed_number):
                return ValidationResult(
                    is_valid=False,
                    error_message="Le format du numéro de téléphone est incorrect"
                )
            
            # Formater en différents formats
            e164_format = phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.E164
            )
            international_format = phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            national_format = phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.NATIONAL
            )
            
            # Récupérer des informations supplémentaires
            from phonenumbers import geocoder, carrier
            
            location = geocoder.description_for_number(parsed_number, 'fr')
            carrier_name = carrier.name_for_number(parsed_number, 'fr')
            number_type = phonenumbers.number_type(parsed_number)
            
            # Déterminer le type de numéro
            type_names = {
                0: 'Fixe',
                1: 'Mobile',
                2: 'Fixe ou Mobile',
                3: 'Numéro gratuit',
                4: 'Numéro surtaxé',
                5: 'Coût partagé',
                6: 'VoIP',
                7: 'Numéro personnel',
                10: 'UAN (Universal Access Number)',
                27: 'Messagerie vocale',
                28: 'Pager',
                99: 'Inconnu'
            }
            
            return ValidationResult(
                is_valid=True,
                normalized_value=e164_format,  # Format E.164 pour stockage
                details={
                    'formats': {
                        'e164': e164_format,
                        'international': international_format,
                        'national': national_format
                    },
                    'location': location or 'Non disponible',
                    'carrier': carrier_name or 'Non disponible',
                    'type': type_names.get(number_type, 'Inconnu'),
                    'country_code': f'+{parsed_number.country_code}',
                    'is_mobile': number_type == 1
                }
            )
            
        except NumberParseException as e:
            error_messages = {
                NumberParseException.INVALID_COUNTRY_CODE: 
                    "Le code pays est invalide",
                NumberParseException.NOT_A_NUMBER: 
                    "Ce n'est pas un numéro de téléphone valide",
                NumberParseException.TOO_SHORT_NSN: 
                    "Le numéro est trop court",
                NumberParseException.TOO_SHORT_AFTER_IDD: 
                    "Le numéro est trop court après l'indicatif international",
                NumberParseException.TOO_LONG: 
                    "Le numéro est trop long"
            }
            
            error_message = error_messages.get(
                e.error_type,
                f"Erreur de validation du numéro: {str(e)}"
            )
            
            return ValidationResult(
                is_valid=False,
                error_message=error_message
            )
    


class ValidationService:
    """Service principal de validation"""
    
    @staticmethod
    def validate_email(email, check_deliverability=True):
        """Valide un email"""
        return EmailValidator.validate(email, check_deliverability)
    
    @staticmethod
    def validate_phone(phone, country_code='MA'):
        """
        Valide un numéro de téléphone
        
        Args:
            phone: Le numéro de téléphone à valider
            country_code: Code pays ISO-2 (ex: 'MA', 'FR', 'US')
        
        Returns:
            ValidationResult avec le numéro validé ou une erreur
        """
        # Vérifier si le code pays est supporté
        if not country_code:
            country_code = 'MA'
        
        # Normaliser le code
        country_code = country_code.upper().strip()
        
        # Vérifier que phonenumbers supporte ce code pays
        try:
            calling_code = phonenumbers.country_code_for_region(country_code)
            if not calling_code or calling_code <= 0:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Le code pays '{country_code}' n'est pas reconnu pour la validation téléphonique. Veuillez sélectionner un pays valide."
                )
        except Exception:
            return ValidationResult(
                is_valid=False,
                error_message=f"Le code pays '{country_code}' n'est pas supporté pour la validation téléphonique. Veuillez sélectionner un pays valide."
            )
        
        # Le code pays est valide, procéder à la validation du numéro
        return PhoneValidator.validate(phone, country_code)
    
    @staticmethod
    def validate_contact_info(email, phone, country_code='MA'):
        """
        Valide à la fois email et téléphone
        
        Returns:
            dict avec les résultats de validation pour chaque champ
        """
        email_result = ValidationService.validate_email(email)
        phone_result = ValidationService.validate_phone(phone, country_code) if phone else ValidationResult(True)
        
        return {
            'email': email_result,
            'phone': phone_result,
            'is_valid': email_result.is_valid and phone_result.is_valid,
            'errors': {
                'email': email_result.error_message if not email_result.is_valid else None,
                'phone': phone_result.error_message if not phone_result.is_valid else None
            }
        }
