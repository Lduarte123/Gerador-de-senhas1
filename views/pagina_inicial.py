import string, secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FermetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / "keys"
    
    def __init__(self, key):
        # Verifique se a chave está no formato correto
        if not isinstance(key, bytes):
            key = key.encode()
        
        # Inicialize o Fernet com a chave fornecida
        self.fernet = Fernet(key)
        
    @classmethod
    def _get_random_string(cls, length=15):
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for i in range(length))
    
    @classmethod   
    def create_key(cls, archive=False):
        # Gera uma nova chave válida para Fernet
        key = Fernet.generate_key()  # Essa linha garante que a chave esteja no formato correto
        print("Generated key:", key)  # Exibe a chave para depuração

        if archive:
            return key, cls.archive_key(key)
        
        return key, None

    @classmethod
    def archive_key(cls, key):
        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(length=5)}.key'
        cls.KEY_DIR.mkdir(exist_ok=True)  # Cria o diretório se não existir
        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)
        return cls.KEY_DIR / file
    
    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decrypt(self, value):
        if isinstance(value, str):
            value = value.encode()  # Garante que o valor esteja em bytes para descriptografia
        
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken:
            return 'Token inválido'


# Gerando uma chave válida e testando a classe
key, _ = FermetHasher.create_key()  # Gera uma nova chave válida de 32 bytes
fernet_lucas = FermetHasher(key)
encrypted_value = fernet_lucas.encrypt("Exemplo de texto")
print("Texto encriptado:", encrypted_value)
print("Texto decriptado:", fernet_lucas.decrypt(encrypted_value))
