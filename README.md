## Getting Started

### Setup confluent cloud env vars

If you are using Linux/WSL.

```bash
export BOOTSTRAP_SERVERS="<CCLOUD_BOOTSTRAP_SERVER>"
export SASL_JAAS_CONFIG="org.apache.kafka.common.security.plain.PlainLoginModule required username='<CCLOUD_API_KEY>' password='<CCLOUD_API_SECRET>';"
export SASL_JAAS_CONFIG_PROPERTY_FORMAT="org.apache.kafka.common.security.plain.PlainLoginModule required username='<CCLOUD_API_KEY>' password='<CCLOUD_API_SECRET>';"
export REPLICATOR_SASL_JAAS_CONFIG="org.apache.kafka.common.security.plain.PlainLoginModule required username='<CCLOUD_API_KEY>' password='<CCLOUD_API_SECRET>';"
export BASIC_AUTH_CREDENTIALS_SOURCE="USER_INFO"
export SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO="<SCHEMA_REGISTRY_API_KEY>:<SCHEMA_REGISTRY_API_SECRET>"
export SCHEMA_REGISTRY_URL="https://<SCHEMA_REGISTRY_ENDPOINT>"
export CLOUD_KEY="<CCLOUD_API_KEY>"
export CLOUD_SECRET="<CCLOUD_API_SECRET>"
export KSQLDB_ENDPOINT=""
export KSQLDB_BASIC_AUTH_USER_INFO=""
```

Otherwise, edit the docker-compose.yml to manually point the above environment variables to their values.

### Build and Startup the Environment

To use the custom sink and source connectors we have to build and start the Docker containers.

```bash
docker-compose up --build
```

This will start the following Docker containers:

- `connect`=> Kafka Connect. This services uses a [custom Docker image](Dockerfile) which is based
  on `confluentinc/cp-kafka-connect-base`.
> the logs from the container *connect* just run `docker logs quickstart-connect`


When all containers are started you can access different services like

- **Kafka Connect Rest API** => http://localhost:8083/

As default [Avro](https://avro.apache.org/) will be used as value and key convertor. If you want to change the default settings just
adapt the [docker-compose.yml](docker-compose.yml)
file for the Kafka Connect service or override the settings in connector config.

```yaml
environment:
  CONNECT_KEY_CONVERTER: io.confluent.connect.avro.AvroConverter
  CONNECT_KEY_CONVERTER_SCHEMA_REGISTRY_URL: $SCHEMA_REGISTRY_URL

  CONNECT_VALUE_CONVERTER: io.confluent.connect.avro.AvroConverter
  CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL: $SCHEMA_REGISTRY_URL
```

Or set the converter in connector config:

```json
{
  "name": "random-source-schemaless",
  "config": {
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter"
  }
}
```

### Let’s Deploy Some Connectors

First we have to check if Kafka Connect is available.

```bash
curl http://localhost:8083/
```

When Kafka Connect is up and running you should see a response like this.

```json
{
  "version":"7.0.1-ce",
  "commit":"1fd5b634a621c986",
  "kafka_cluster_id":"lkc-x9qyz"
}
```

To deploy a connector,

```bash
curl -X POST http://localhost:8083/connectors  \
    -H "Content-Type: application/json" \
    --data @config/jdbc-sink-smt.json
```

### To add/modify connector plugins

Change the Dockerfile,

```
# Install connector plugins with the confluent-hub cli
# confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.0.0
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-s3:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-datagen:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest

RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:latest
RUN confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:latest
```
stop the containers.

```bash
docker-compose down
```

and then re run this command:

```bash
docker-compose up --build
```

## TODO

3. ~add a postgres container for jdbc sink~
4. ~confirm if trace logs happen~
5. python avro producer
6. ~hot reload~
7. ~tests~
8. CI/CD


## Legalese

Copyright © 2022 [Platformatory](https://platformatory.io/) | See [LICENCE](LICENSE) for full details.
