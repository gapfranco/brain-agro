# brain-agro

## Backend API cadastro agrícola

### Objetivos

API simples de demonstração usando Django Rest Framework.

### Requisitos

- Python 3.12

### Instalação

- Acessar o folder onde foi baixado.
- Usando o poetry
  ```
  poetry install
  poetry shell
  ```
- Usando virtualenv manual:
  ```
  python3 -m venv venv
    source venv/bin/activate (Mac/Linux)
  venv/Scripts/activate.bat (Windows)
  ```
- Copiar o arquivo .env.modelo para .env e ajustar o ambiente para o banco de dados.
  O default é usar sqlite no proprio folder do projeto (dn.sqlite3)

- Iniciar o serviço
  ```
  python manage.py runserver
  ```

Escuta a porta 8000 no protocolo HTTP. Para encerrá-lo digitar CTRL-C

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
### Testes

Usando o **PyTest** para realizar testes unitários básicos. Para rodar os testes, basta
chamar o comando `pytest` de dentro do diretório do serviço, após ativar o virtual environmente
do python.
