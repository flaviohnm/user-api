import csv
from faker import Faker
import random

# Configuração do Faker para dados em português
fake = Faker('pt_BR')

# Função para gerar CPF no formato XXX.XXX.XXX-XX
def gerar_cpf():
    cpf = [random.randint(0, 9) for _ in range(11)]
    cpf = f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"
    return cpf

# Função para gerar data de nascimento no formato YYYY-MM-DD
def gerar_data_nascimento():
    return fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d')

# Gerar 1000 usuários fictícios
usuarios = []
for _ in range(200):
    nome = fake.name()
    email = fake.profile()['mail']
    cpf = gerar_cpf()
    data_nascimento = gerar_data_nascimento()
    usuarios.append([nome, email, cpf, data_nascimento])

# Salvar os dados em um arquivo CSV
with open('./data/users.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['nome', 'email', 'cpf', 'data_nascimento'])  # Cabeçalho
    writer.writerows(usuarios)

print("Arquivo './data/users.csv' gerado com sucesso!")