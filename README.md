# EcoAção

Aplicação web em Python para registrar atitudes sustentáveis, marcá-las como concluídas e acompanhar o progresso. O projeto usa Flask, SQLite, templates Jinja e CSS responsivo.

## Requisitos

- Python 3.10 ou superior
- pip

## Executar no Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000). O banco de dados é criado automaticamente em `instance/ecoacao.sqlite3`.

## Executar os testes

```powershell
python -m unittest discover -s tests -v
```

## Conceitos demonstrados

- Rotas e formulários HTTP com Flask
- Persistência com SQLite e consultas parametrizadas
- Validação de entrada no servidor
- Separação entre aplicação, acesso a dados e interface
- Testes automatizados com `unittest`

Para implantação, defina uma variável de ambiente `SECRET_KEY` forte e use um servidor WSGI apropriado; `python app.py` é destinado ao desenvolvimento local.
