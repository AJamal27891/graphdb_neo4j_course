import json
import os
import random
import uuid
from datetime import datetime, timedelta

from faker import Faker
from neo4j import GraphDatabase


class Neo4jDataGenerator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.fake = Faker()

    def close(self):
        self.driver.close()

    def generate_customers(self, num_customers):
        with self.driver.session() as session:
            for _ in range(num_customers):
                customer_data = {
                    "id": f"C{str(uuid.uuid4())[:8]}",
                    "name": self.fake.name(),
                    "email": self.fake.email(),
                    "phone": self.fake.phone_number(),
                    "address": self.fake.address(),
                    "created_at": self.fake.date_time_this_year().isoformat(),
                    "risk_score": round(random.uniform(0, 1), 2),
                    "segment": random.choice(["Premium", "Standard", "Basic"]),
                }

                session.run(
                    """
                    CREATE (c:Customer {
                        id: $id,
                        name: $name,
                        email: $email,
                        phone: $phone,
                        address: $address,
                        created_at: datetime($created_at),
                        risk_score: $risk_score,
                        segment: $segment
                    })
                """,
                    customer_data,
                )

    def generate_products(self, num_products):
        categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]
        with self.driver.session() as session:
            # Create categories first
            for category in categories:
                session.run(
                    """
                    MERGE (c:Category {name: $name})
                """,
                    {"name": category},
                )

            # Create products
            for _ in range(num_products):
                product_data = {
                    "id": f"P{str(uuid.uuid4())[:8]}",
                    "name": self.fake.product_name(),
                    "price": round(random.uniform(10, 1000), 2),
                    "category": random.choice(categories),
                    "description": self.fake.text(max_nb_chars=200),
                    "stock": random.randint(0, 100),
                }

                session.run(
                    """
                    MATCH (c:Category {name: $category})
                    CREATE (p:Product {
                        id: $id,
                        name: $name,
                        price: $price,
                        description: $description,
                        stock: $stock
                    })
                    CREATE (p)-[:BELONGS_TO]->(c)
                """,
                    product_data,
                )

    def generate_orders(self, num_orders):
        with self.driver.session() as session:
            customers = session.run("MATCH (c:Customer) RETURN c.id AS id").values()
            products = session.run("MATCH (p:Product) RETURN p.id AS id").values()

            for _ in range(num_orders):
                order_products = random.sample(products, random.randint(1, 5))
                order_data = {
                    "id": f"O{str(uuid.uuid4())[:8]}",
                    "customer_id": random.choice(customers)[0],
                    "date": self.fake.date_time_this_year().isoformat(),
                    "status": random.choice(
                        ["PENDING", "PROCESSING", "COMPLETED", "SHIPPED"]
                    ),
                    "products": [p[0] for p in order_products],
                }

                session.run(
                    """
                    MATCH (c:Customer {id: $customer_id})
                    CREATE (o:Order {
                        id: $id,
                        date: datetime($date),
                        status: $status
                    })
                    CREATE (c)-[:PLACED]->(o)
                    WITH o
                    UNWIND $products as product_id
                    MATCH (p:Product {id: product_id})
                    CREATE (o)-[:CONTAINS]->(p)
                """,
                    order_data,
                )

    def generate_reviews(self, num_reviews):
        with self.driver.session() as session:
            customers = session.run("MATCH (c:Customer) RETURN c.id AS id").values()
            products = session.run("MATCH (p:Product) RETURN p.id AS id").values()

            for _ in range(num_reviews):
                review_data = {
                    "id": f"R{str(uuid.uuid4())[:8]}",
                    "customer_id": random.choice(customers)[0],
                    "product_id": random.choice(products)[0],
                    "rating": random.randint(1, 5),
                    "text": self.fake.text(max_nb_chars=200),
                    "date": self.fake.date_time_this_year().isoformat(),
                }

                session.run(
                    """
                    MATCH (c:Customer {id: $customer_id})
                    MATCH (p:Product {id: $product_id})
                    CREATE (r:Review {
                        id: $id,
                        rating: $rating,
                        text: $text,
                        date: datetime($date)
                    })
                    CREATE (c)-[:WROTE]->(r)
                    CREATE (r)-[:ABOUT]->(p)
                """,
                    review_data,
                )

    def generate_transactions(self, num_transactions):
        with self.driver.session() as session:
            customers = session.run("MATCH (c:Customer) RETURN c.id AS id").values()

            # Generate some devices first
            devices = []
            for _ in range(
                int(num_transactions * 0.2)
            ):  # Assume each device is used multiple times
                devices.append(
                    {
                        "id": f"D{str(uuid.uuid4())[:8]}",
                        "type": random.choice(["Mobile", "Desktop", "Tablet"]),
                        "browser": random.choice(["Chrome", "Firefox", "Safari"]),
                        "os": random.choice(["iOS", "Android", "Windows", "MacOS"]),
                    }
                )

            # Create transactions
            for _ in range(num_transactions):
                device = random.choice(devices)
                transaction_data = {
                    "id": f"T{str(uuid.uuid4())[:8]}",
                    "customer_id": random.choice(customers)[0],
                    "amount": round(random.uniform(10, 1000), 2),
                    "date": self.fake.date_time_this_year().isoformat(),
                    "status": random.choice(["SUCCESS", "PENDING", "FAILED"]),
                    "risk_score": round(random.uniform(0, 1), 2),
                    "device": device,
                    "location": {
                        "city": self.fake.city(),
                        "country": self.fake.country(),
                        "latitude": float(self.fake.latitude()),
                        "longitude": float(self.fake.longitude()),
                    },
                }

                session.run(
                    """
                    MATCH (c:Customer {id: $customer_id})
                    MERGE (d:Device {id: $device.id})
                    ON CREATE SET 
                        d.type = $device.type,
                        d.browser = $device.browser,
                        d.os = $device.os
                    CREATE (t:Transaction {
                        id: $id,
                        amount: $amount,
                        date: datetime($date),
                        status: $status,
                        risk_score: $risk_score
                    })
                    CREATE (l:Location {
                        city: $location.city,
                        country: $location.country,
                        latitude: $location.latitude,
                        longitude: $location.longitude
                    })
                    CREATE (c)-[:MADE]->(t)
                    CREATE (t)-[:USES]->(d)
                    CREATE (t)-[:FROM]->(l)
                """,
                    transaction_data,
                )

    def generate_supply_chain(self, num_suppliers):
        with self.driver.session() as session:
            # Generate suppliers
            for _ in range(num_suppliers):
                supplier_data = {
                    "id": f"S{str(uuid.uuid4())[:8]}",
                    "name": self.fake.company(),
                    "contact": self.fake.name(),
                    "email": self.fake.company_email(),
                    "address": self.fake.address(),
                }

                session.run(
                    """
                    CREATE (s:Supplier {
                        id: $id,
                        name: $name,
                        contact: $contact,
                        email: $email,
                        address: $address
                    })
                """,
                    supplier_data,
                )

            # Connect suppliers to products
            session.run(
                """
                MATCH (s:Supplier), (p:Product)
                WITH s, p, rand() as r
                WHERE r < 0.2
                CREATE (s)-[:SUPPLIES]->(p)
            """
            )

    def generate_marketing_campaigns(self, num_campaigns):
        with self.driver.session() as session:
            campaign_types = ["Email", "Social", "Display", "Search"]

            for _ in range(num_campaigns):
                campaign_data = {
                    "id": f"M{str(uuid.uuid4())[:8]}",
                    "name": f"Campaign {self.fake.word()}",
                    "type": random.choice(campaign_types),
                    "start_date": self.fake.date_time_this_year().isoformat(),
                    "budget": round(random.uniform(1000, 10000), 2),
                    "status": random.choice(["ACTIVE", "PLANNED", "COMPLETED"]),
                }

                session.run(
                    """
                    CREATE (m:MarketingCampaign {
                        id: $id,
                        name: $name,
                        type: $type,
                        start_date: datetime($start_date),
                        budget: $budget,
                        status: $status
                    })
                """,
                    campaign_data,
                )

            # Connect campaigns to customers with engagement metrics
            session.run(
                """
                MATCH (m:MarketingCampaign), (c:Customer)
                WITH m, c, rand() as r
                WHERE r < 0.1
                CREATE (c)-[:ENGAGED_WITH {
                    engagement_score: rand(),
                    date: datetime()
                }]->(m)
            """
            )


def main():
    # Initialize generator
    generator = Neo4jDataGenerator(
        uri="neo4j://neo4j:7687",
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    try:
        # Generate base data
        generator.generate_customers(100)
        generator.generate_products(50)
        generator.generate_orders(200)
        generator.generate_reviews(150)

        # Generate business scenario data
        generator.generate_transactions(300)
        generator.generate_supply_chain(10)
        generator.generate_marketing_campaigns(5)

    finally:
        generator.close()


if __name__ == "__main__":
    main()
