# flask-graphene-neo4j
An example flask API integrating Graphene and Neo4j

### Prerequisite

Neo-4j database is installed and running.

### Installation

    pipenv install

### Execution

Set Neo4j environment variables.

    export NEO4J_URL="<NEO4J_BOLT_URL>"
    
    export NEO4J_USERNAME="<NEO4J_USERNAME>"
    
    export NEO4J_PASSWORD="<NEO4J_PASSWORD>"
    
Start flask app by specifying the desired port.

    python application.py --port 5000

Open GrapiQL interface on web browser.

    http://localhost:5000/graphql
    
Refer to api.txt and play around with commands.

### Description

Refer to blog post.
    
