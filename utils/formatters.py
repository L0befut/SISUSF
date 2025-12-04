# =============================================================================
# utils/formatters.py
# =============================================================================

import re

class Formatters:
    @staticmethod
    def format_cpf(cpf: str) -> str:
        """Formata CPF: 12345678901 -> 123.456.789-01"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    @staticmethod
    def format_cns(cns: str) -> str:
        """Formata CNS: 123456789012345 -> 123 4567 8901 2345"""
        cns = re.sub(r'\D', '', cns)
        if len(cns) == 15:
            return f"{cns[:3]} {cns[3:7]} {cns[7:11]} {cns[11:]}"
        return cns
    
    @staticmethod
    def format_cep(cep: str) -> str:
        """Formata CEP: 12345678 -> 12345-678"""
        cep = re.sub(r'\D', '', cep)
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Formata telefone"""
        phone = re.sub(r'\D', '', phone)
        if len(phone) == 10:
            return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
        elif len(phone) == 11:
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        return phone
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Remove caracteres especiais mantendo apenas números"""
        return re.sub(r'\D', '', text) if text else ''