"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Module de chiffrement des données sensibles
Utilise Fernet (chiffrement symétrique) pour protéger les données
"""
from cryptography.fernet import Fernet
from flask import current_app
import base64
import hashlib


class EncryptionService:
    """Service de chiffrement/déchiffrement des données sensibles"""
    
    @staticmethod
    def _get_cipher():
        """Obtenir l'instance Fernet avec la clé de chiffrement"""
        key = current_app.config.get('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY n'est pas définie dans l'environnement")
        
        if isinstance(key, str):
            key_bytes = key.encode()
        else:
            key_bytes = key
        
        derived_key = base64.urlsafe_b64encode(hashlib.sha256(key_bytes).digest())
        return Fernet(derived_key)
    
    @staticmethod
    def encrypt(data):
        """
        Chiffrer des données
        
        Args:
            data (str): Données à chiffrer
            
        Returns:
            str: Données chiffrées (base64)
        """
        if not data:
            return None
        
        if not isinstance(data, str):
            data = str(data)
        
        cipher = EncryptionService._get_cipher()
        encrypted = cipher.encrypt(data.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt(encrypted_data):
        """
        Déchiffrer des données
        
        Args:
            encrypted_data (str): Données chiffrées
            
        Returns:
            str: Données déchiffrées
        """
        if not encrypted_data:
            return None
        
        if not isinstance(encrypted_data, str):
            encrypted_data = str(encrypted_data)
        
        try:
            cipher = EncryptionService._get_cipher()
            decrypted = cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            # Si le déchiffrement échoue (mauvaise clé), retourner None au lieu de lever une erreur
            # Cela évite les erreurs 500 lors de la lecture de données chiffrées avec une ancienne clé
            from flask import current_app
            current_app.logger.warning(f"Échec du déchiffrement (clé incorrecte?): {str(e)[:100]}")
            return None
    
    @staticmethod
    def generate_key():
        """
        Générer une nouvelle clé de chiffrement
        
        Returns:
            str: Nouvelle clé (à stocker dans ENCRYPTION_KEY)
        """
        key = Fernet.generate_key()
        return key.decode()


def encrypt_sensitive_data(data):
    """Helper function pour chiffrer des données sensibles"""
    return EncryptionService.encrypt(data)


def decrypt_sensitive_data(encrypted_data):
    """Helper function pour déchiffrer des données sensibles"""
    return EncryptionService.decrypt(encrypted_data)
