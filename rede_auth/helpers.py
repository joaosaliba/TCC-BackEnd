import re
from django.db.models import Max, Min
import random
import logging
import datetime
helper_time = [('00:00', '00:00'), ('00:30', '00:30'), ('01:00', '01:00'), ('01:30', '01:30'), ('02:00', '02:00'), ('02:30', '02:30'), ('03:00', '03:00'), ('03:30', '03:30'), ('04:00', '04:00'), ('04:30', '04:30'), ('05:00', '05:00'), ('05:30', '05:30'), ('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'), ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30')]

days_dict = {0: {'previous': 6, 'after': 1}, 1: {'previous': 1, 'after': 2}, 2: {'previous': 1, 'after': 3}, 3: {'previous': 2, 'after': 4}, 4: {'previous': 3, 'after': 5}, 5: {'previous': 4, 'after': 6}, 6: {'previous': 5, 'after': 0}}

time_dict = {'00:00': {'previous': '23:30', 'after': '00:30'}, '00:30': {'previous': '00:00', 'after': '01:00'}, '01:00': {'previous': '00:30', 'after': '01:30'}, '01:30': {'previous': '01:00', 'after': '02:00'}, '02:00': {'previous': '01:30', 'after': '02:30'}, '02:30': {'previous': '02:00', 'after': '03:00'}, '03:00': {'previous': '02:30', 'after': '03:30'}, '03:30': {'previous': '03:00', 'after': '04:00'}, '04:00': {'previous': '03:30', 'after': '04:30'}, '04:30': {'previous': '04:00', 'after': '05:00'}, '05:00': {'previous': '04:30', 'after': '05:30'}, '05:30': {'previous': '05:00', 'after': '06:00'}, '06:00': {'previous': '05:30', 'after': '06:30'}, '06:30': {'previous': '06:00', 'after': '07:00'}, '07:00': {'previous': '06:30', 'after': '07:30'}, '07:30': {'previous': '07:00', 'after': '08:00'}, '08:00': {'previous': '07:30', 'after': '08:30'}, '08:30': {'previous': '08:00', 'after': '09:00'}, '09:00': {'previous': '08:30', 'after': '09:30'}, '09:30': {'previous': '09:00', 'after': '10:00'}, '10:00': {'previous': '09:30', 'after': '10:30'}, '10:30': {'previous': '10:00', 'after': '11:00'}, '11:00': {'previous': '10:30', 'after': '11:30'}, '11:30': {'previous': '11:00', 'after': '12:00'}, '12:00': {'previous': '11:30', 'after': '12:30'}, '12:30': {'previous': '12:00', 'after': '13:00'}, '13:00': {'previous': '12:30', 'after': '13:30'}, '13:30': {'previous': '13:00', 'after': '14:00'}, '14:00': {'previous': '13:30', 'after': '14:30'}, '14:30': {'previous': '14:00', 'after': '15:00'}, '15:00': {'previous': '14:30', 'after': '15:30'}, '15:30': {'previous': '15:00', 'after': '16:00'}, '16:00': {'previous': '15:30', 'after': '16:30'}, '16:30': {'previous': '16:00', 'after': '17:00'}, '17:00': {'previous': '16:30', 'after': '17:30'}, '17:30': {'previous': '17:00', 'after': '18:00'}, '18:00': {'previous': '17:30', 'after': '18:30'}, '18:30': {'previous': '18:00', 'after': '19:00'}, '19:00': {'previous': '18:30', 'after': '19:30'}, '19:30': {'previous': '19:00', 'after': '20:00'}, '20:00': {'previous': '19:30', 'after': '20:30'}, '20:30': {'previous': '20:00', 'after': '21:00'}, '21:00': {'previous': '20:30', 'after': '21:30'}, '21:30': {'previous': '21:00', 'after': '22:00'}, '22:00': {'previous': '21:30', 'after': '22:30'}, '22:30': {'previous': '22:00', 'after': '23:00'}, '23:00': {'previous': '22:30', 'after': '23:30'}, '23:30': {'previous': '23:00', 'after': '00:00'}}


def validate_cpf(cpf: str) -> bool:

    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """

    # Verifica a formatação do CPF
    #if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
    #    return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:

        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:

        return False

    return True

import re
def validate_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.
 
    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False
 
    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall('\d', str(cnpj)))
    
    if (not cnpj) or (len(cnpj) < 14):
            return False
    
    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]
    
    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)
    
    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return True
    return False


def get_random_object(queryset):
    min_id = queryset.aggregate(min_id=Min("id"))['min_id']
    max_id = queryset.aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        selected = queryset.filter(pk=pk).first()
        if selected:
            return selected



