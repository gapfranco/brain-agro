"""
Funções utilitarias
"""


def valida_cnpj(cnpj):
    cnpj = "".join(c for c in cnpj if c.isdigit())
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0

    # Verifica se os dígitos calculados são iguais aos fornecidos
    if int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2:
        return True

    return False


def validar_cpf(cpf):
    cpf = "".join(c for c in cpf if c.isdigit())

    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0

    # Verifica se os dígitos calculados são iguais aos fornecidos
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True

    return False


def valida_cnpj_cpf(codigo):
    if len(codigo) == 14:
        return valida_cnpj(codigo)
    return validar_cpf(codigo)


def valida_areas(
    area_total: int, area_vegetacao: int, area_cultura: int
) -> str:
    if area_total < 0 or area_vegetacao < 0 or area_cultura < 0:
        return "Áreas inválidas"
    if area_total < area_vegetacao + area_cultura:
        return "Áreas de vegetação e cultura excedem a área total"
    return ""
