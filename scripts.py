import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# URL da API
API_URL = os.getenv('API_URL')
TOKEN_URL = os.getenv('TOKEN_URL')

# Função para obter token JWT
def get_jwt_token():
    auth_data = {"username": "userTest", "password": "userPass"}
    response = requests.post(TOKEN_URL, data=auth_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Falha ao obter token JWT")


# Função para enviar dados do CSV para a API
def enviar_dados_csv(csv_file):
    token = get_jwt_token()
    users = pd.read_csv(csv_file, sep=",", encoding="utf-8")
    
    total_registros = users.shape[0]
    
    for index, row in users.iterrows():
        user_data = {
            "nome": row["nome"],
            "email": row["email"],
            "cpf": row["cpf"],
            "data_nascimento": row["data_nascimento"]
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(API_URL, json=user_data, headers=headers)
        if response.status_code == 201:
            print(
                f"Usuário {index + 1} de {total_registros} | nome: {row['nome']} | cadastrado com sucesso!"
            )
        else:
            print(
                f"Erro ao cadastrar usuário {row['nome']}: {response.status_code}"
            )

# Executar o script
if __name__ == "__main__":
    enviar_dados_csv("./data/users.csv")