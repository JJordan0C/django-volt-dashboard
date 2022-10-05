# using ubuntu LTS version
FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel libmariadb-dev build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/topbet/venv
ENV PATH="/home/topbet/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir gevent
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y \
 	python3.9 python3-gevent python3-tk libmariadb-dev python3-venv wkhtmltopdf locales && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/'        /etc/locale.gen \
 && sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen
ENV LANG it_IT.UTF-8
ENV LANGUAGE it_IT.UTF-8  
ENV LC_ALL it_IT.UTF-8 


RUN useradd --create-home topbet
COPY --from=builder-image /home/topbet/venv /home/topbet/venv

USER topbet
RUN mkdir /home/topbet/code
WORKDIR /home/topbet/code
COPY . .

EXPOSE 8000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

# activate virtual environment
ENV VIRTUAL_ENV=/home/topbet/venv
ENV PATH="/home/topbet/venv/bin:$PATH"

RUN python manage.py migrate

# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
