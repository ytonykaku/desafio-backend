# Desafio de Backend

## Pré-requisitos

Para executar este projeto, você precisará ter instalado em sua máquina:

* Docker
* Docker Compose

## Como Executar

1. **Clone o repositório:**

   ```bash
   git clone git@github.com:ytonykaku/desafio-backend.git
   cd desafio-backend
   ```

2. **Construa e suba os containers:**

   ```bash
   docker-compose up --build
   ```

   Após a execução, a API estará disponível em `http://localhost:5000`.

* **Exemplo de Uso (URL para o navegador):**

  ```
  http://localhost:5000/analisador-git?usuario=gitpython-developers&repositorio=gitpython

  http://localhost:5000/analisador-git?usuario=hmontazeri&repositorio=is-vegan
  http://127.0.0.1:5000/analisador-git?usuario=ytonykaku&repositorio=athlead-ods
  http://127.0.0.1:5000/analisador-git?usuario=sh3-sistemas&repositorio=vexis3
  127.0.0.1:5000/analisador-git?usuario=spatie&repositorio=dashboard.spatie.be
  http://127.0.0.1:5000/analisador-git?usuario=spatie&repositorio=package-skeleton-laravel
  ```

  ```
  http://localhost:5000/analisador-git/buscar?autor1=Sebastian&autor2=Tim
  http://127.0.0.1:5000/analisador-git/buscar?autor1=ton
  http://127.0.0.1:5000/analisador-git/buscar?autor1=ton&autor2=Alex
  ```

## Executando os Testes (Opcional)

Com o container da aplicação em execução, você pode rodar a suíte de testes unitários e de integração com o seguinte comando:

```bash
docker-compose exec web pytest
```
