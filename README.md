# Running Praktomat in a Docker container

This repository is a containerized version of [KIT Praktomat](https://github.com/KITPraktomatTeam/Praktomat) for [University of Regensburg (Prof. Kesdogan)](https://itsec.ur.de).  

## Install to localhost
For test purposes you can simply install a local setup.  
```bash
docker-compose up -d
```  

The following environment variables need to be set (`.env` file) for running the container.
- `COMPOSE_PROJECT_NAME`: This is the ID of your Praktomat instance. You can run multiple instances, e.g. one per course. Practically, this defines where you'll reach your Praktomat instance, e.g. https://localhost/your-praktomat-id.
- `PRAKTOMAT_NAME`: This is the name of your site. It will be displayed at the top of the web interface.
- `PRAKTOMAT_DOMAIN`: The domain under which your instance(s) will be reachable
- `PRAKTOMAT_ADMIN`: The email address of the administrator for the Praktomat instance
- `USE_LDAP`: Set to `True` to use LDAP for authentication, otherwise local registration is used. If set to `True` local registration is disabled.
- `POSTGRES_HOST`: PostgreSQL hostname (container name). Make sure that the host is accessible, i.e. it must be in the same network (or namespace) as the Pratomat.
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password. It can also point to a file (like docker secrets).

Two containers are going to be created and started. One container contains a PostgreSQL database and one container contains the actual Praktomat application.  

To create a superuser open the CLI of the Praktomat container you just started. The container name usually looks like <COMPOSE_PROJECT_NAME>_praktomat.

```bash
docker exec -it <container name> /bin/bash
```
Then execute the following command to interactively create a superuser:

```bash
python3 Praktomat/src/manage-local.py createsuperuser
```

The application is accessible on http://PRAKTOMAT_DOMAIN/COMPOSE_PROJECT_NAME.

## Build docker container
The `build-docker` directory contains all necessary files to build the praktomat docker container. This project is specifically designed for the context of the University of Regensburg. If the project is to be used for other universities, settings must be made in the `local.py` file. By default, the superuser `praktomat` (ID: 1) is created without a password which is useful for automated grading (see https://github.com/GithubKesdogan/praktomat-utils).

### LDAP
For authentication with LDAP over TLS the certificate can be generated with `tools/get-ldap-cert.sh`. After login, connect to the praktomat container and make yourself a superuser.
```bash
docker exec -it <container name> /bin/bash
python3 Praktomat/src/manage-local.py makesuperuser --username <username>
```

## Persistent data (volumes)
You should specify volumes to enable persistent data after a crash.
- PostgreSQL: `/var/lib/postgresql/data`
- Praktomat:
    - `/home/praktomat/debug-data`
    - `/home/praktomat/test-data`
    - `/home/praktomat/work-data`

## Rancher
You can set secrets as environment variables with `Prefix or Alias` field. For healthcheck you can use
- PostgreSQL: `pg_isready -d praktomat`
- Praktomat: HTTP request to `/` returns a successful status