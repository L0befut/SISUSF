# =============================================================================
# README.md
# =============================================================================

"""
# SISUSF - Sistema de Saúde da Família

Sistema de gestão para Unidades Básicas de Saúde (UBS) focado na Estratégia Saúde da Família.

## 🏥 Funcionalidades

### ✅ Implementadas no Piloto
- **Autenticação e Controle de Acesso**
  - Login com diferentes perfis (Admin, Médico, Enfermeiro, ACS)
  - Sistema de permissões por funcionalidade
  - Logs de auditoria completos

- **Cadastro de Pacientes**
  - Dados pessoais completos
  - Validação de CPF e CNS
  - Endereço completo com CEP
  - Dados clínicos básicos (peso, altura, IMC, tipo sanguíneo)
  - Alergias e medicamentos de uso contínuo

- **Consulta de Pacientes**
  - Busca por nome, CPF ou CNS
  - Visualização completa dos dados
  - Interface intuitiva com tabelas

- **Dashboard**
  - Estatísticas em tempo real
  - Total de pacientes cadastrados
  - Pacientes cadastrados no mês
  - Consultas do dia e do mês
  - Interface com cards visuais

- **Auditoria**
  - Log de todas as operações
  - Rastreamento de alterações
  - Controle de usuários e IPs

### 🔄 Em Desenvolvimento
- Agendamento de consultas
- Prontuário eletrônico
- Controle de medicamentos
- Cadastro de famílias
- Relatórios avançados
- Sistema de backup automático

## 🛠️ Tecnologias

- **Backend**: Python 3.8+
- **Interface**: PyQt5
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Segurança**: bcrypt para senhas
- **Relatórios**: ReportLab

## ⚙️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/sisusf.git
cd sisusf
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
1. Crie um banco de dados PostgreSQL:
```sql
CREATE DATABASE sisusf;
CREATE USER sisusf_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE sisusf TO sisusf_user;
```

2. Configure as variáveis de ambiente criando um arquivo `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sisusf
DB_USER=sisusf_user
DB_PASSWORD=sua_senha
SECRET_KEY=sua_chave_secreta_aqui
```

### 4. Execute o sistema
```bash
python run.py
```

## 👤 Usuários Padrão

O sistema cria automaticamente os seguintes usuários para teste:

| Perfil | Email | Senha |
|--------|-------|-------|
| Administrador | admin@sisusf.com | admin123 |
| Médico | medico@sisusf.com | medico123 |
| Enfermeiro | enfermeiro@sisusf.com | enfermeiro123 |

⚠️ **IMPORTANTE**: Altere essas senhas em produção!

## 📊 Estrutura do Banco

### Principais Tabelas
- `usuarios` - Profissionais do sistema
- `pacientes` - Dados dos pacientes
- `enderecos` - Endereços dos pacientes
- `familias` - Núcleos familiares
- `consultas` - Consultas médicas e procedimentos
- `medicamentos` - Controle de estoque
- `dispensacoes` - Dispensação de medicamentos
- `logs_auditoria` - Auditoria do sistema

## 🔒 Segurança

- Senhas criptografadas com bcrypt
- Validação rigorosa de CPF e CNS
- Logs de auditoria completos
- Controle de sessão por usuário
- Validação de permissões por operação

## 📋 Validações

### CPF
- Algoritmo oficial da Receita Federal
- Verificação de dígitos verificadores
- Detecção de sequências inválidas

### CNS (Cartão Nacional de Saúde)
- Validação básica de formato
- Verificação de numeração válida

### Dados Clínicos
- IMC calculado automaticamente
- Validação de faixas de valores (peso, altura)
- Formatação automática de dados

## 🚀 Arquitetura

```
sisusf/
├── app/                 # Aplicação principal
├── models/              # Modelos de dados (SQLAlchemy)
├── views/               # Interface gráfica (PyQt5)
├── controllers/         # Lógica de negócio
├── db/                  # Configuração e conexão do banco
├── utils/               # Utilitários (validação, formatação)
├── config/              # Configurações do sistema
└── resources/           # Recursos visuais
```

## 📝 Licença

[...]

## 🤝 Contribuindo

[...]

## 📞 Suporte

Para suporte e dúvidas:
- Email: [...]
- Issues: [...]

## 📈 Roadmap

### Versão 1.1
- [ ] Prontuário eletrônico completo
- [ ] Agendamento de consultas
- [ ] Módulo de vacinação
- [ ] Relatórios gerenciais

### Versão 1.2
- [ ] Integração com e-SUS AB
- [ ] Módulo de territorialização
- [ ] App mobile para Agentes Comunitários
- [ ] Dashboard avançado com gráficos

### Versão 2.0
- [ ] Integração com ...
- [ ] Telemedicina básica
- [ ] Prontuário compartilhado
- [ ] 

---

**SISUSF** - Desenvolvido com ❤️ para a Saúde Pública Brasileira
"""