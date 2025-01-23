# Use Neo4j 5.26.0 base image
FROM neo4j:5.26.0

# Install system tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    htop \
    nano \
    curl \
    procps && \
    rm -rf /var/lib/apt/lists/*

# Specify download URLs for APOC Core and GDS Community versions
ENV APOC_URL=https://github.com/neo4j/apoc/releases/download/5.26.1/apoc-5.26.1-core.jar
ENV GDS_URL=https://github.com/neo4j/graph-data-science/releases/download/2.13.2/neo4j-graph-data-science-2.13.2.jar

# Create the plugins directory and download jar files
RUN mkdir -p /plugins && \
    wget -O /plugins/apoc-core.jar $APOC_URL && \
    wget -O /plugins/gds-community.jar $GDS_URL

# Neo4j configuration
ENV NEO4J_AUTH=none \
    NEO4J_dbms_memory_heap_max__size=4G \
    NEO4J_dbms_memory_pagecache_size=2G \
    NEO4J_dbms_security_procedures_unrestricted=gds.*,apoc.* \
    NEO4J_apoc_export_file_enabled=true \
    NEO4J_apoc_import_file_enabled=true

# Expose ports
EXPOSE 7474 7687

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f --max-time 5 http://localhost:7474 || exit 1

# Persist Neo4j data, logs, and imports
VOLUME /data /logs /import

# Start Neo4j
CMD ["neo4j"]
