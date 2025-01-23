#!/usr/bin/env python3
import os
import sys
import time
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from neo4j import GraphDatabase


def wait_for_neo4j(http_port, max_retries=30, delay=2):
    """Wait for Neo4j HTTP endpoint to become available"""
    url = f"http://neo4j:{http_port}"
    for i in range(max_retries):
        try:
            print(f"Attempting to connect to {url}")
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ Neo4j HTTP endpoint is accessible at {url}")
                return True
            else:
                print(f"Received status code {response.status_code} from {url}")
        except requests.exceptions.ConnectionError as e:
            print(
                f"Waiting for Neo4j to start (attempt {i + 1}/{max_retries}). Error: {str(e)}"
            )
            time.sleep(delay)
    return False


def test_bolt_connection(uri, user, password):
    """Test direct bolt connection"""
    try:
        print(f"\nTesting direct bolt connection to {uri}")
        # Try both neo4j:// and bolt:// protocols
        if uri.startswith("neo4j://"):
            alternate_uri = uri.replace("neo4j://", "bolt://")
            uris_to_try = [uri, alternate_uri]
        else:
            alternate_uri = uri.replace("bolt://", "neo4j://")
            uris_to_try = [uri, alternate_uri]

        for test_uri in uris_to_try:
            try:
                print(f"Attempting connection with {test_uri}")
                driver = GraphDatabase.driver(test_uri, auth=(user, password))
                driver.verify_connectivity()
                print(f"✅ Successfully connected using {test_uri}")
                driver.close()
                return True
            except Exception as e:
                print(f"❌ Failed to connect using {test_uri}. Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Bolt connection test failed: {str(e)}")
        return False


def test_neo4j_connection():
    # Load environment variables
    load_dotenv()

    # Get connection details with explicit debugging
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    print("\nEnvironment Variables:")
    print(f"NEO4J_URI: {'SET' if uri else 'MISSING'} = {uri}")
    print(f"NEO4J_USER: {'SET' if user else 'MISSING'} = {user}")
    print(
        f"NEO4J_PASSWORD: {'SET' if password else 'MISSING'} = {'*' * len(password) if password else 'MISSING'}"
    )

    if not all([uri, user, password]):
        print("❌ Missing required environment variables!")
        print("Required variables: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD")
        return False

    # Parse URI to get host and port
    parsed_uri = urlparse(uri)
    neo4j_host = parsed_uri.hostname
    neo4j_port = parsed_uri.port or 7687
    http_port = 7474  # Default Neo4j HTTP port

    print(f"\nConnection Details:")
    print(f"- URI: {uri}")
    print(f"- User: {user}")
    print(f"- Host: {neo4j_host}")
    print(f"- Bolt Port: {neo4j_port}")
    print(f"- HTTP Port: {http_port}")

    # Test direct bolt connection first
    if not test_bolt_connection(uri, user, password):
        print("❌ Direct bolt connection failed")
        return False

    # Wait for Neo4j HTTP endpoint
    if not wait_for_neo4j(http_port):
        print("❌ Neo4j HTTP endpoint did not become available")
        return False

    try:
        print("\nTesting full database functionality...")
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            # Test basic query
            try:
                print("Testing basic query...")
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] == 1:
                    print("✅ Basic query successful")
                else:
                    print("❌ Basic query failed")
                    return False
            except Exception as e:
                print(f"❌ Basic query failed: {str(e)}")
                return False

            # Get Neo4j version
            try:
                print("Getting Neo4j version...")
                version = session.run(
                    "CALL dbms.components() YIELD name, versions RETURN versions[0] as version"
                ).single()
                print(f"✅ Connected to Neo4j version: {version['version']}")
            except Exception as e:
                print(f"❌ Version check failed: {str(e)}")
                return False

            # Test write permissions
            try:
                print("Testing write permissions...")
                session.run(
                    """
                    CREATE (n:TestNode {test: true})
                    DELETE n
                """
                )
                print("✅ Write permissions verified")
            except Exception as e:
                print(f"❌ Write test failed: {str(e)}")
                return False

            print("\n✅ All Neo4j connection tests passed!")
            return True

    except Exception as e:
        print(f"\n❌ Connection test failed: {str(e)}")
        return False
    finally:
        if "driver" in locals():
            driver.close()


if __name__ == "__main__":
    success = test_neo4j_connection()
    sys.exit(0 if success else 1)
