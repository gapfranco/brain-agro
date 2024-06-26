# brain-agro

#### Backend API cadastro agrícola

### Objetivos

API simples de demonstração usando Django Rest Framework.

### Requisitos

- Python 3.12

### Instalação

O ambiente de desenvolvimento foi montado utilizando poetry (https://python-poetry.org).

- Acessar o folder onde foi baixado.
  ```
  poetry install
  poetry shell
  ```
- Se não tiver o poetry instalado e preferir usar o virtualvenv de forma manual:
  ```
  python3 -m venv venv
  source venv/bin/activate (Mac/Linux)
  venv/Scripts/activate.bat (Windows)
  pip install -r agro_requirements.xtx
  ```

- Copiar o arquivo .env.modelo para .env e ajustar o ambiente para o banco de dados.
  O default é usar sqlite no proprio folder do projeto (dn.sqlite3)

- Criar as tabelas de banco de dados iniciais
  ```
  python manage.py migrate
  ```

- Opcionalmente, criar um usuário para acessar o admin do django
  ```
  python manage.py createsuperuser
  ```

- Foi criado um comando para gerar registros fake para testar:
  ```
  python manage.py fake_data
  ```
  cada chamada desse comando vai criar 10 fazendas com culturas aleatórias.

- Iniciar o serviço
  ```
  python manage.py runserver
  ```

Escuta a porta 8000 no protocolo HTTP. Para encerrá-lo digitar CTRL-C

### Operação

Com o serviço rodando já pode chamar os endpoints criados.
Para auxiliar nos testes usando Postman, importar a collection e ambientes incluidos no folder **postman**
na raiz do projeto.

---
### Endpoints

#### Listar fazendas

`POST /api/query/`

com o corpo:

```
{
  "cidade": "",
  "uf": "",
  "culturas": "Cana,Café"
}
```
- cidade: Nome da cidade para filtrar a lista de fazendas
- uf: Estado para filtar a lista de fazendas
- culturas: Lista de culturas seperadas por "," para fitrar a lista de fazenas.

As culturas podem ser: Soja, Milho, Algodão, Café e Cana.

Qualquer parâmetro em branco ou não informado defativa o filtro por ele.

---
#### Criar fazendas

`POST /api/cria_fazenda/`

com o corpo no padrão:

```
{
  "codigo": "07346324870",
  "nome_fazenda": "Aurora",
  "nome_produtor": "Gonçalo",
  "cidade": "Ribeirão Preto",
  "uf": "SP",
  "area_total": 300,
  "area_vegetacao": 80,
  "area_cultura": 200,
  "culturas": [
    {
      "cultura": "Soja",
      "area": 100
    },
    {
      "cultura": "Cana",
      "area": 30
    },
    {
      "cultura": "Algodão",
      "area": 40
    }
  ]
}
```
Vai criar uma nova fazenda ou propriedade com os dados informados e as culturas plantadas.

Faz as seguintes validações:
- Campos obrigatórios (menos culturas)
- Campo código deve ser um CPF ou CNPJ validos
- Campo area_total deve ser maior ou igual area_vegetacao + area_cultura
- Se houver culturas plantadas, a soma de suas áreas deve ser menor ou igual a area_cultura

**Response**

Retorna JSON com os dados da fazenda criada.

**Erros**

Havendo erros, retorna os detalhes em JSON. Por exemplo:

```
{
  "codigo": [
    "CPF ou CNPJ inválido"
  ]
}
```
ou
```
{
  "non_field_errors": [
    "Áreas de vegetação e cultura excedem a área total"
  ]
}
```
---
#### Alterar fazendas

`PATCH /api/altera_fazenda/99`

Passando o id da fzenda na url e os campos que quer alterar no corpo:
```
{
  "nome_fazenda": "Aurorinha",
  "culturas": [
    {
      "cultura": "Cana",
      "area": 10
    }
  ]
}
```
Faz as mesmas validações da inclusão.

> **IMPORTANTE:** Na alteração, se houver a campo *culturas*, o que for informado
  vai substituir **todas** as culturas que estavam cadastradas anteriormente.
  No emplo acima, se a fazenda tinha culturas de *Café* e *Algodão*, depois dessa alteração
  terá apenas a cultura de *Cana*.

**Response**

Retorna JSON com os dados da fazenda alterada.

**Erros**

Havendo erros, retorna os detalhes em JSON

---
#### Excluir fazendas

`DELETE /api/altera_fazenda/99`

Passando o id da fazenda na url. A fazenda com esse id e todas as suas culturas serão escluidas.

---
#### Excluir culturas de uma fazendas

`GET /api/excluir_culturas/99`

Passando o id da fazenda na url. Todas as culturas da fazenda serão excluidas.

---
#### Resumo

`GET /api/resumo`

Retorna os totais cadastrados
```
{
  "fazendas": 12,
  "area_total": 2160,
  "area_cultura": 2160,
  "area_vegetacao": 950
}
```

---
#### Resumo por Estados

`GET /api/resumo_estado`

Retorna um resumo por estado
```
[
  {
    "uf": "MG",
    "fazendas": 2,
    "area_total": 260,
    "area_cultura": 260,
    "area_vegetacao": 180
  },
  {
    "uf": "SP",
    "fazendas": 10,
    "area_total": 1900,
    "area_cultura": 1900,
    "area_vegetacao": 770
  }
]
```

---
#### Resumo por Estados e culturas

`GET /api/resumo_uf_culturas`

Retorna um resumo por estado e cultura
```
[
  {
    "tipo_cultura": "Cana",
    "fazenda__uf": "MG",
    "total_area": 100
  },
  {
    "tipo_cultura": "Cana",
    "fazenda__uf": "SP",
    "total_area": 50
  },
  {
    "tipo_cultura": "Soja",
    "fazenda__uf": "SP",
    "total_area": 20
  }
]
```
---
#### Resumo por culturas

`GET /api/resumo_culturas`

Retorna um resumo por culturas
```
[
  {
    "tipo_cultura": "Cana",
    "total_area": 150
  },
  {
    "tipo_cultura": "Soja",
    "total_area": 20
  }
]
```

---
### Testes

Usando o **PyTest** para realizar os testes. Foram criados 2 tasks no pyproject.toml:

1. **task test** - Rodas todos os testes
2. **task coverage** - Roda todos os testes com cobertura

Chamar na linha de comando na raiz do projeto. Por exemplo:

```
task coverage

```

---
### Dados de teste

O comando **fake_data** gera dados de teste no banco de dados em grupos de 10;

```
python manage.py fake_data

```
