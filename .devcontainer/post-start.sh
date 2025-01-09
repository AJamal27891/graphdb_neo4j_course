#!/bin/bash

# Wait for Neo4j to be ready
echo "Waiting for Neo4j to be ready..."
timeout=60
elapsed=0
while ! cypher-shell -a bolt://neo4j:7687 -u neo4j -p ${NEO4J_PASSWORD} 'RETURN 1;' &>/dev/null; do
    if [ "$elapsed" -ge "$timeout" ]; then
        echo "Timeout waiting for Neo4j"
        exit 1
    fi
    sleep 1
    elapsed=$((elapsed+1))
    echo "Waiting... ($elapsed seconds)"
done

echo "Neo4j is ready!"

# Create indexes and constraints
echo "Setting up Neo4j indexes and constraints..."
cypher-shell -a bolt://neo4j:7687 -u neo4j -p ${NEO4J_PASSWORD} '
CREATE INDEX customer_id IF NOT EXISTS FOR (c:Customer) ON (c.id);
CREATE INDEX product_id IF NOT EXISTS FOR (p:Product) ON (p.id);
CREATE INDEX order_id IF NOT EXISTS FOR (o:Order) ON (o.id);
'