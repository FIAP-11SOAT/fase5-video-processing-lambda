# AWS Lambda Authentication System - Clean Architecture

Sistema de autenticação serverless implementado com AWS Lambda, Cognito e Clean Architecture.

## 🏗️ Arquitetura

Este projeto implementa **Clean Architecture** com separação clara de camadas:

- **Domain Layer**: Entidades e regras de negócio
- **Application Layer**: Casos de uso
- **Infrastructure Layer**: Integrações AWS (Cognito)
- **Presentation Layer**: Handlers Lambda

Veja [ARCHITECTURE.md](ARCHITECTURE.md) para documentação detalhada.

## 📦 Lambdas

### 1. Auth Lambda
Lambda de autenticação com 4 rotas:

- `POST /register` - Registrar novo usuário
- `POST /authenticate` - Autenticar usuário
- `GET /user-info` - Obter informações do usuário
- `GET /user-by-id/{user_id}` - Buscar usuário por ID

**Tecnologias**: AWS Cognito, Python 3.11

### 2. Alert Lambda
Lambda para processar alertas do CloudWatch via SNS.

**Trigger**: SNS Topic subscrito a alarmes do CloudWatch

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- AWS CLI configurado
- Terraform >= 1.0
- Make

### Instalação

```bash
# Clonar repositório
git clone <repo-url>
cd fase5-video-processing-lambda

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
make install
```

### Executar Testes

```bash
# Executar todos os testes
make test

# Executar com cobertura (mínimo 80%)
make coverage

# Ver relatório HTML de cobertura
open htmlcov/index.html
```

### SonarQube

```bash
# Gerar coverage XML e rodar análise do SonarQube
make coverage
make sonar
```

O projeto está configurado para exigir **mínimo de 80% de cobertura** de testes.

### Deploy

```bash
# 1. Empacotar lambdas
make package

# 2. Deploy infraestrutura
cd deploy/terraform
terraform init
terraform plan
terraform apply

# Ou usar o Makefile
make deploy
```

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── auth_lambda/          # Lambda de autenticação
│   │   ├── domain/           # Camada de domínio
│   │   ├── application/      # Casos de uso
│   │   ├── infrastructure/   # Integrações AWS
│   │   └── presentation/     # Handlers
│   └── alert_lambda/         # Lambda de alertas
├── deploy/
│   └── terraform/            # Infraestrutura como código
├── tests/                    # Testes unitários
├── requirements.txt          # Dependências Python
├── Makefile                  # Comandos úteis
└── ARCHITECTURE.md           # Documentação da arquitetura
```

## 🧪 Testes

Implementação de testes unitários com PyTest:

```bash
# Rodar testes
pytest

# Com cobertura
pytest --cov=src

# Específico
pytest tests/test_auth_use_cases.py
```

## 🔒 Segurança

- **AWS Cognito**: Gerenciamento seguro de senhas e tokens
- **Política de senhas**: Mínimo 8 caracteres, maiúsculas, minúsculas, números e símbolos
- **JWT Tokens**: Autenticação stateless
- **IAM**: Princípio do menor privilégio
- **Variáveis de ambiente**: Dados sensíveis protegidos

## 📊 Cognito Configuration

O Cognito é configurado via Terraform com:

- Username/Password authentication
- Email como atributo de username
- Política de senhas robusta
- Token expiration configurado
- Advanced security mode habilitado

## 🛠️ Comandos Disponíveis

```bash
make help      # Mostrar ajuda
make install   # Instalar dependências
make test      # Executar testes
make lint      # Executar linting
make format    # Formatar código
make clean     # Limpar artefatos
make package   # Empacotar lambdas
make deploy    # Deploy com Terraform
```

## 🔧 Variáveis de Ambiente

### Auth Lambda
```
COGNITO_USER_POOL_ID=<user-pool-id>
COGNITO_CLIENT_ID=<client-id>
ENVIRONMENT=dev
```

### Alert Lambda
```
ENVIRONMENT=dev
```

## 📝 Exemplos de Uso

### Registrar Usuário

```bash
curl -X POST https://api-url/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "SenhaSegura123!",
    "email": "usuario@example.com"
  }'
```

### Autenticar

```bash
curl -X POST https://api-url/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "SenhaSegura123!"
  }'
```

### Obter Informações do Usuário

```bash
curl -X GET https://api-url/user-info \
  -H "Authorization: Bearer <access-token>"
```

### Buscar Usuário por ID

```bash
curl -X GET https://api-url/user-by-id/<user-id>
```

## 🎯 Clean Architecture Benefits

1. **Testabilidade**: Lógica de negócio testável sem dependências externas
2. **Flexibilidade**: Fácil substituição de implementações
3. **Manutenibilidade**: Separação clara de responsabilidades
4. **Independência**: Core agnóstico de frameworks
5. **Escalabilidade**: Fácil adição de novos recursos

## 📚 Documentação Adicional

- [ARCHITECTURE.md](ARCHITECTURE.md) - Documentação detalhada da arquitetura
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte do curso de Pós-Graduação FIAP - Fase 5.

## 👥 Autores

FIAP Pós-Graduação - Fase 5
