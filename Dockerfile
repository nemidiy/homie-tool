FROM python:3.8-slim

# Set the working directory
WORKDIR /usr/src/homie-tool

# Copy your app's source code from your host to your image filesystem.
COPY . .

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY etc/requirements.txt .

RUN set -ex \
    && buildDeps=' \
	git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
	$buildDeps \
	freetds-bin \
	build-essential \
	default-libmysqlclient-dev \
	apt-utils \
	curl \
	rsync \
	netcat \
	libpq5 \
	locales \
	gpg \
	gzip \
	unzip \
	gpg-agent \
	net-tools \
	vim-tiny \
	mosquitto \
	mosquitto-clients \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && pip install -U pip setuptools wheel \
    && pip install -r requirements.txt \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
	/var/lib/apt/lists/* \
	/tmp/* \
	/var/tmp/* \
	/usr/share/man \
	/usr/share/doc \
	/usr/share/doc-base

RUN echo 'alias ll="ls -lrtah"' >> ~/.bashrc

CMD ["pytest"] # set default arg for entrypoint