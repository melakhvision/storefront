# storefront
install pipenv with 
```bash
pip install pipenv
```
## Install requirements from Pipfile
```bash
pipenv install
```
## convert pipfile and pipfile.lock to requirements.txt

```bash
pipenv lock -r > requirements.txt
```



### Fix django mysql connection issue on Dockerfile
```bash
RUN apk add gcc musl-dev mariadb-dev
```