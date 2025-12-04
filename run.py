# =============================================================================
# run.py
# =============================================================================
#!/usr/bin/env python3
"""
SISUSF - Sistema de Saúde da Família
Inicializador principal do sistema

Para executar:
    python run.py

Requisitos:
- Python 3.8+
- PostgreSQL 12+
- Dependências listadas em requirements.txt
"""

import sys
import os

# Adicionar o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.main import main

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 SISUSF - Sistema de Saúde da Família")
    print("   Versão 1.0.0 - Piloto")
    print("=" * 60)
    print()
    
    # Verificar versão do Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    
    print("🚀 Iniciando aplicação...")
    print()
    
    try:
        exit_code = main()
        print()
        print("👋 Sistema encerrado")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print()
        print("⚠️ Sistema interrompido pelo usuário")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)