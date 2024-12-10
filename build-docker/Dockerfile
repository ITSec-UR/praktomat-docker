FROM ubuntu:jammy
EXPOSE 443/tcp

# Setup timezone
# Installing tzdata in the next step is required too
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system requirements
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -yq \
  apache2 \
  apache2-dev \
  libpq-dev \
  zlib1g-dev \
  libmysqlclient-dev \
  libsasl2-dev \
  libssl-dev \
  libffi-dev \
  swig \
  libapache2-mod-xsendfile \
  libapache2-mod-wsgi-py3  \
  git-core \
  libldap2-dev \
  python3-setuptools \
  python3-psycopg2 \
  python3-virtualenv \
  python3-pip \
  sudo \
  locales \
  tzdata \
  cron \
  libipc-run-perl \
  libdata-guid-perl \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  && rm -rf /var/lib/apt/lists/*

# Install java (openjdk-21)
RUN apt-get update && apt install -y openjdk-21-jdk junit4 junit && rm -rf /var/lib/apt/lists/*

#RUN ln -s /usr/bin/python3 /usr/bin/python

# Setup locale
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Install Docker
#RUN mkdir -p /etc/apt/keyrings
#RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
#RUN echo \
#  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
#RUN apt-get update && apt-get install -yq \
#  docker-ce-cli \
#  && rm -rf /var/lib/apt/lists/*

# Add users
RUN useradd -m praktomat && adduser praktomat sudo
RUN useradd -m tester && adduser tester sudo && adduser tester praktomat
COPY sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER praktomat
WORKDIR /home/praktomat
RUN git clone https://github.com/hso-praktomat/praktomat Praktomat && cd Praktomat
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/java
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/javac
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/java
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/javac

# Get wait-for-it.sh (used to wait for PostgreSQL to become available)
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh wait-for-it.sh
RUN sudo chmod 775 wait-for-it.sh

# Install Python requirements for Praktomat
RUN python3 -m pip install --upgrade pip && python3 -m pip install -U pip virtualenv setuptools wheel urllib3[secure]
RUN python3 -m pip install -r Praktomat/requirements.txt

# Install necessary libraries for rsa keys
COPY tools/create_rsakeys.py create_rsakeys.py
RUN sudo python3 -m pip install cryptography

# Set executable/search flag for directories (only) located inside of /home/praktomat/.local
# This is required for Apache in order to follow the symlinks to some files (referenced from static directory)
RUN chmod -R g+X .local

# Install Praktomat addons
ADD https://github.com/jplag/jplag/releases/download/v2.12.1-SNAPSHOT/jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar /opt/praktomat-addons/jplag.jar
ADD https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.14/checkstyle-8.14-all.jar /opt/praktomat-addons/checkstyle.jar
RUN sudo chown -R praktomat:praktomat /opt/praktomat-addons
RUN chmod -R 640 /opt/praktomat-addons/*

# Install safe-docker
#ADD https://raw.githubusercontent.com/nomeata/safe-docker/master/safe-docker /usr/local/bin/safe-docker

# Copy config file
COPY local.py Praktomat/src/settings/local.py

# Setup required directories
RUN mkdir -p debug-data work-data test-data

# Configure Apache2
ENV APACHE_RUN_USER=www-data
ENV APACHE_RUN_GROUP=www-data
RUN sudo adduser www-data praktomat
RUN sudo a2enmod macro
COPY praktomat.wsgi Praktomat/wsgi/praktomat.wsgi
COPY apache_praktomat_wsgi.conf Praktomat/documentation/apache_praktomat_wsgi.conf
RUN printf "\nInclude /home/praktomat/Praktomat/documentation/apache_praktomat_wsgi.conf\n" | sudo tee -a /etc/apache2/apache2.conf
COPY mpm_event.conf /etc/apache2/mods-available/mpm_event.conf

# Configure OpenLDAP
COPY ldapserver.pem /etc/ssl/certs/ldapserver.pem
RUN printf "\nTLS_CACERT    /etc/ssl/certs/ldapserver.pem\n" | sudo tee -a /etc/ldap/ldap.conf

# Initialize Praktomat
RUN COMPOSE_PROJECT_NAME="" PRAKTOMAT_NAME="" PRAKTOMAT_DOMAIN="" USE_LDAP="" POSTGRES_USER="" POSTGRES_PASSWORD="" POSTGRES_HOST="" POSTGRES_PORT="" python3 Praktomat/src/manage-local.py collectstatic --noinput --link

# Configure Cron to automatically run all checkers
COPY daily-cron.sh daily-cron.sh
RUN (crontab -l ; echo "0 2 * * * bash /home/praktomat/daily-cron.sh >> /home/praktomat/cronlog 2>&1") | crontab -

COPY run.sh run.sh
RUN sudo chmod 775 run.sh
ENTRYPOINT ["./run.sh"]