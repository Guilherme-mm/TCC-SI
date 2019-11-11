FROM neo4j:3.5

LABEL maintainer = "Guilherme Muller <guilherme.muller.m@gmail.com>"
LABEL version = 0.0.1
LABEL description = "The neo4j image of the application"

RUN echo "CREATE CONSTRAINT ON (n:Actor) ASSERT n.id IS UNIQUE" > installation-cypher-script.cql
