
# MDA

## Clone repository (v1.3.2)

```
cd ~
git clone https://github.com/5GZORRO/mda.git
cd mda
git checkout tags/1.3.2
```

## Configure MDA

`.env`

```
POSTGRES_USER=postgres
POSTGRES_PW=myPassword
POSTGRES_HOST=172.15.0.195
POSTGRES_PORT=5432
POSTGRES_DB=mda_development
RESET_DB=true

# Kafka config
KAFKA_HOST=172.15.0.195
KAFKA_PORT=9092

# MDA config
NUM_READING_THREADS=1
NUM_AGGREGATION_THREADS=0
```

Create `.env` with above contents

## Start MDA

```
docker-compose -f docker-compose-development.yml up --build
```
