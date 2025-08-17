"""
এনক্রিপশন এবং নিরাপত্তা ইউটিলিটি
Encryption and Security Utilities
"""

import base64
import secrets
import json
from typing import Optional, Dict, Any

# Try to import cryptography modules
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    print("⚠️ cryptography not installed. Using mock encryption.")
    CRYPTOGRAPHY_AVAILABLE = False
    
    class MockFernet:
        def encrypt(self, data):
            return base64.b64encode(data)
        def decrypt(self, data):
            return base64.b64decode(data)
    
    Fernet = lambda x: MockFernet()

# Try to import bcrypt
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    print("⚠️ bcrypt not installed. Using simple hash.")
    BCRYPT_AVAILABLE = False

from config.settings import config

class SecurityManager:
    """নিরাপত্তা ম্যানেজার - Security Manager"""
    
    def __init__(self):
        self.fernet = None
        if CRYPTOGRAPHY_AVAILABLE and config.ENCRYPTION_KEY:
            try:
                self.fernet = Fernet(config.ENCRYPTION_KEY.encode())
            except:
                # Generate new key if invalid
                self.fernet = Fernet(Fernet.generate_key())
        elif CRYPTOGRAPHY_AVAILABLE:
            self.fernet = Fernet(Fernet.generate_key())
    
    def generate_encryption_key(self) -> str:
        """Generate new encryption key"""
        if CRYPTOGRAPHY_AVAILABLE:
            return Fernet.generate_key().decode()
        else:
            return "mock-encryption-key-" + secrets.token_urlsafe(16)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not self.fernet:
            return data  # Return as-is if no encryption key
        
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception:
            return data  # Return as-is if encryption fails
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not self.fernet:
            return encrypted_data
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception:
            return encrypted_data  # Return as-is if decryption fails
    
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        if BCRYPT_AVAILABLE:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        else:
            # Simple mock hash for testing
            return f"mock-hash-{hash(password)}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        if BCRYPT_AVAILABLE:
            try:
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            except Exception:
                return False
        else:
            # Simple mock verification
            return hashed == f"mock-hash-{hash(password)}"
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    def is_admin_user(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in config.ADMIN_USER_IDS
    
    def is_super_admin(self, user_id: int) -> bool:
        """Check if user is super admin"""
        return user_id == config.SUPER_ADMIN_ID
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potential XSS patterns
        dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
        sanitized = text
        
        for pattern in dangerous_patterns:
            sanitized = sanitized.replace(pattern, '')
        
        return sanitized.strip()
    
    def validate_file_type(self, filename: str) -> bool:
        """Validate file type for uploads"""
        allowed_extensions = {
            'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 
            'mp4', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar'
        }
        
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    def encrypt_user_data(self, data: Dict[str, Any]) -> str:
        """Encrypt user data for backup"""
        json_data = json.dumps(data, ensure_ascii=False)
        return self.encrypt_data(json_data)
    
    def decrypt_user_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt user data from backup"""
        try:
            decrypted = self.decrypt_data(encrypted_data)
            return json.loads(decrypted)
        except Exception:
            return {}

# Global instance
security = SecurityManager()