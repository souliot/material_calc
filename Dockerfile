FROM python:3.10.7

WORKDIR /app

RUN apt-get update && \
  apt-get upgrade -y && \
  apt install gfortran-9 liblapack-dev -y && \
  cp /usr/bin/gfortran-9 /usr/bin/gfortran && \
  apt-get autoclean && \
  rm -rf /var/lib/apt/lists/*

ADD ./libs/vaspkit.1.4.1.linux.x64.tar.gz /app/libs
ADD ./libs/ElATools-1.7.3.tar.gz /app/libs

COPY ./libs/Makefile_ElaTools /app/libs/ElATools-1.7.3/soc/Makefile

ENV PATH=/app/libs/vaspkit.1.4.1/bin:/app/libs/ElATools-1.7.3/bin:$PATH

COPY ./requirements.txt /app/requirements.txt 

RUN cd /app/libs/ElATools-1.7.3/soc && \
  chmod +x run_path.sh && \
  echo -e "/app/libs/ElATools-1.7.3/db/\nn" | ./run_path.sh && \
  make && make clean && \
  pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./material_calc /app/material_calc

CMD ["uvicorn", "material_calc.main:app", "--host", "0.0.0.0", "--port", "80"]