
import re

def validar_cpf(cpf: str) -> bool:
    return bool(re.fullmatch(r"\d{11}", cpf))

def validar_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

def validar_nome(nome: str) -> bool:
    return len(nome.strip()) >= 3
