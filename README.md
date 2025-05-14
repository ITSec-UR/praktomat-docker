# Running Praktomat in a Docker container

This repository provides a containerized version of [KIT Praktomat](https://github.com/KITPraktomatTeam/Praktomat) for the [University of Regensburg (Prof. Kesdogan)](https://itsec.ur.de). 

## Setting Up Praktomat Locally
For testing purposes, you can set up a local instance of Praktomat using Docker Compose. To start the application, run:  
```bash
docker compose up -d
```  

### Required Environment Variables
Create a `.env` file with the following variables:

- `COMPOSE_PROJECT_NAME`: ID of your Praktomat instance (e.g., course name). This determines the sub-path of your URL (e.g., `https://localhost/your-praktomat-id`).
- `PRAKTOMAT_NAME`: Name displayed on the web interface.
- `PRAKTOMAT_DOMAIN`: Domain where your Praktomat will be accessible.
- `PRAKTOMAT_ADMIN`: Email address of the Praktomat admin.
- `USE_LDAP`: Set to `True` to enable LDAP authentication (disables local registration).
- `POSTGRES_HOST`: Hostname of your PostgreSQL service (e.g., `db`). Must be on the same Docker network.
- `POSTGRES_DB`: Database name.
- `POSTGRES_USER`: Database user.
- `POSTGRES_PASSWORD`: Database password (or path to a Docker secret file).

### Accessing the Application
Two containers will be started: one for the PostgreSQL database and one for the Praktomat application.

To create a superuser:

```bash
docker exec -it <container_name> /bin/bash
python3 Praktomat/src/manage-local.py createsuperuser
```

Your Praktomat instance will be accessible at:

```
http://PRAKTOMAT_DOMAIN/COMPOSE_PROJECT_NAME
```

## Build docker container
Inside the `build-docker` directory:
```bash
make build
```

This builds the Praktomat Docker image. By default, it creates a `praktomat` superuser (ID: 1) with no password, which is useful for automated grading (see [praktomat-utils](https://github.com/GithubKesdogan/praktomat-utils)).

> Note: For adapting to a different university, modify the `local.py` configuration.

## LDAP
To use LDAP with TLS, generate a certificate:
```bash
build-docker/tools/get-ldap-cert.sh
```

Then make your user a superuser:
```bash
docker exec -it <container name> /bin/bash
python3 Praktomat/src/manage-local.py makesuperuser --username <username>
```

## Persistent Volumes
For persistent storage, mount the following volumes:
- PostgreSQL: `/var/lib/postgresql/data`
- Praktomat:
    - `/home/praktomat/debug-data`
    - `/home/praktomat/test-data`
    - `/home/praktomat/work-data`

## Rancher Deployment Notes
- You can pass secrets as environment variables using the `Prefix or Alias` field.
- Health checks:
  - PostgreSQL: `pg_isready -d praktomat`
  - Praktomat: HTTP request to `/` should return a 200 status.
- When creating the workload:
  - Go to advanced options.
  - Enable `Privilege Escalation`.