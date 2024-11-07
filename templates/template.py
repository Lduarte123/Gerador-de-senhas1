import sys
import os
sys.path.append(os.path.abspath(os.curdir))
from model.password import Password
from views.pagina_inicial import FermetHasher

action = input("Digite 1 para uma nova senha ou 2 para salvar uma senha: ")

match action:
    case '1':
        if Password.get() is None or len(Password.get()) == 0:
            key, path = FermetHasher.create_key(archive=True)  # Corrigido para "archive"
            print("Sua Chave foi criada com sucesso, salve-a com cuidado.")
            print(f'Chave: {key.decode("utf-8")}')
            if path:
                print('Chave salva no arquivo, lembre-se de remover o arquivo após a transferência de local')
                print(f'Caminho: {path}')
        else:
            key_input = input('Digite sua chave usada para criptografia, use sempre a mesma chave:')
            key = key_input.encode('utf-8')  # Convertendo a chave para bytes
                   
        domain = input("Dominio: ")
        password = input("Senha: ")
        fernet_user = FermetHasher(key)
        p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
        p1.save()
    case '2':
        # código para salvar a senha
        pass

