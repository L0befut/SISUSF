# =============================================================================
# utils/validators.py
# =============================================================================

import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida CPF brasileiro"""
        cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Verifica primeiro dígito
        sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = (sum_digits * 10) % 11
        if digit1 == 10:
            digit1 = 0
        
        if int(cpf[9]) != digit1:
            return False
        
        # Verifica segundo dígito
        sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = (sum_digits * 10) % 11
        if digit2 == 10:
            digit2 = 0
        
        return int(cpf[10]) == digit2
    
    @staticmethod
    def validate_cns(cns: str) -> bool:
        """Valida Cartão Nacional de Saúde"""
        cns = re.sub(r'\D', '', cns)
        
        if len(cns) != 15:
            return False
        
        # Validação simplificada - implementar algoritmo completo se necessário
        if cns.startswith(('1', '2', '7', '8', '9')):
            return True
        
        return False
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_cep(cep: str) -> bool:
        """Valida CEP brasileiro"""
        cep = re.sub(r'\D', '', cep)
        return len(cep) == 8
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida telefone brasileiro"""
        phone = re.sub(r'\D', '', phone)
        return len(phone) in [10, 11]  # com ou sem 9 no celular
