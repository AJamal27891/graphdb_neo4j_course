#!/usr/bin/env python3
import os
import time

from neo4j import GraphDatabase


def verify_auth():
    uri = os.getenv("NEO4J_URI", "neo4j://neo4j:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "testpassword123")

    print(f"\nVerifying Neo4j authentication...")
    print(f"URI: {uri}")
    print(f"User: {user}")
    print(f"Password: {password}")

    max_retries = 5
    for attempt in range(max_retries):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                # Try to get the current user
                result = session.run("CALL dbms.security.showCurrentUser()")
                current_user = result.single()
                print(f"\nSuccessfully authenticated!")
                print(f"Current user details: {current_user}")
                driver.close()
                return True
        except Exception as e:
            print(f"\nAttempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Waiting 5 seconds before retry...")
                time.sleep(5)
    return False


if __name__ == "__main__":
    success = verify_auth()
    if not success:
        print("\nFailed to verify authentication after multiple attempts")
    exit(0 if success else 1)
