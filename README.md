# Stripe test case

![](https://github.com/afoninsb/Stripe/actions/workflows/stripe_workflow.yml/badge.svg)


## Technology stack

Python 3.10, Django 4.1.6, Stripe 5.1.1

## [Demo](http://158.160.10.11)

### Основное задание
http://51.250.96.200/item/1/

### Дополнительные задания
http://51.250.96.200/ - главная
http://51.250.96.200/admin/ - админ-панель

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```bash
SECRET_KEY="django-insecure-&_pndsdx9^mn#dsdsgvl!)^1a8hbfdbfhnhn#jhngfistm+w"
STRIPE_PUBLIC_KEY=pk_test_51MaLDMEk83dfbdbgwuoUcEzeMSo0Gbfgbb6YoH6AlKrzPJNgfbfdsf9i3cSZp1ENpQPxUYB5v7re9D8vAYdJAl00KQr9GJe1
STRIPE_SECRET_KEY=sk_test_51MaLDMasfgnhnh8lQi2FShmfg9ogbgnfdgf7akHZNYTu6P3EzVP3egfjghjhfgVZTa2pV001dHr0UNY

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_pass
DB_HOST=db
DB_PORT=5432
```

## Run Locally

Clone the project

```bash
  git@github.com:afoninsb/Stripe.git
```

Go to the '/infra/' in the project directory and up docker-compose

```bash
  cd my-project/infra
  sudo docker-compose up -d --build
```

In another terminal window
```bash
  cd my-project/infra
  sh start.sh
```
The following will happen:
  - collect static
  - run migrations
  - load test data
  - a superuser will be created

Go to the http://localhost/
