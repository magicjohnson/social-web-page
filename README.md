# Project install

## Clone repository

```
$ git clone git@github.com:magicjohnson/social-web-page.git
```

## Run commands for initial setup:

```
cd social-web-page
make first_run
```

## Check application is up and running

Go to browser and open the url http://127.0.0.1:8000/admin/

to create superuser run:
```
$ make createsuperuser
```

## Import vacancies

```
$ make import_vacancies
```

# Run/Stop

to run application use command:

```
$ make start
```

to stop:

```
$ make stop
```
