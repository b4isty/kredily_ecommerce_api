# Kredily Ecommerce API

## Installation and run

Clone this repo
```bash
git clone 
```
To run the project use docker run command below
```bash
docker-compose up --build
```

To enter into docker terminal use below command
```bash
docker-compose exec <container_name>  bash
```

To run tests go to docker terminal and run
```bash
python manage.py test
```


To create a user go to register API at ```api/sign-up```
Sample payload
```bash
{
    "username": "test_user",
    "password": "abc@123"
}
```


To login navigate to ```api/token/```
Sample payload
```bash
{
    "username": "test_user",
    "password": "abc@123"
}

```


It will return a token. Use that token in header to authenticate the user on other APIs

To refresh token navigate to ```api/token/refresh/``` accordingly with following payload

```bash
{
    "token": "your token"
}
```


For detail API documentation check below API doc link

```bash
http://127.0.0.1:8000/doc/
