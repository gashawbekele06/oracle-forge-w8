"""
Minimal demo seed — inserts ~30 records into PostgreSQL and MongoDB
for the Oracle Forge demo video. Completes in under 2 minutes.

Usage:
    python scripts/seed_demo_minimal.py
"""
import asyncio
import os
import sys
from pathlib import Path

try:
    import asyncpg
except ImportError:
    print("Installing asyncpg...")
    os.system(f"{sys.executable} -m pip install asyncpg pymongo -q")
    import asyncpg

from pymongo import MongoClient

BUSINESSES = [
    ("bizid_001", "The Cozy Corner",       "Indianapolis, Indiana. Great coffee and wifi.",  120, 1, "IN"),
    ("bizid_002", "Indy Grill House",       "Indianapolis, Indiana. Best burgers in town.",    310, 1, "IN"),
    ("bizid_003", "Broad Ripple Bistro",    "Indianapolis, Indiana. French cuisine.",           88, 1, "IN"),
    ("bizid_004", "Mass Ave Diner",         "Indianapolis, Indiana. Classic American diner.",  205, 1, "IN"),
    ("bizid_005", "Fountain Square Cafe",   "Indianapolis, Indiana. Artisan sandwiches.",       67, 1, "IN"),
    ("bizid_006", "Circle City Steakhouse", "Indianapolis, Indiana. Premium steaks.",          412, 1, "IN"),
    ("bizid_007", "Speedway Smokehouse",    "Indianapolis, Indiana. BBQ and ribs.",            189, 1, "IN"),
    ("bizid_008", "Garfield Park Eats",     "Indianapolis, Indiana. Comfort food.",             54, 1, "IN"),
    ("bizid_009", "Canal Walk Coffee",      "Indianapolis, Indiana. Specialty coffee.",        143, 1, "IN"),
    ("bizid_010", "Meridian Street Sushi",  "Indianapolis, Indiana. Fresh sushi rolls.",       237, 1, "IN"),
    ("bizid_011", "Phoenix Diner",          "Phoenix, Arizona. Breakfast all day.",            178, 1, "AZ"),
    ("bizid_012", "Vegas Eats",             "Las Vegas, Nevada. Late night food.",             502, 1, "NV"),
    ("bizid_013", "Portland Brew",          "Portland, Oregon. Craft beer and snacks.",        321, 1, "OR"),
    ("bizid_014", "Austin BBQ Joint",       "Austin, Texas. Texas-style BBQ.",                 445, 1, "TX"),
    ("bizid_015", "Seattle Fish Market",    "Seattle, Washington. Fresh seafood.",             267, 1, "WA"),
]

REVIEWS = [
    ("rev_001", "usr_001", "bizref_001", 5, "2024-01-10", "Amazing coffee, best in Indy!"),
    ("rev_002", "usr_002", "bizref_001", 4, "2024-02-14", "Great place, a bit crowded."),
    ("rev_003", "usr_003", "bizref_001", 5, "2024-03-01", "Love the wifi and atmosphere."),
    ("rev_004", "usr_001", "bizref_002", 5, "2024-01-20", "Best burgers I've ever had."),
    ("rev_005", "usr_004", "bizref_002", 4, "2024-02-28", "Solid food, good portions."),
    ("rev_006", "usr_002", "bizref_002", 5, "2024-03-15", "Indy Grill never disappoints."),
    ("rev_007", "usr_003", "bizref_003", 3, "2024-01-05", "Decent French food."),
    ("rev_008", "usr_005", "bizref_003", 4, "2024-02-10", "Nice ambiance, pricey."),
    ("rev_009", "usr_001", "bizref_004", 4, "2024-01-18", "Classic diner vibes."),
    ("rev_010", "usr_002", "bizref_004", 5, "2024-02-22", "Perfect breakfast spot."),
    ("rev_011", "usr_003", "bizref_005", 4, "2024-03-05", "Great sandwiches."),
    ("rev_012", "usr_004", "bizref_006", 5, "2024-01-25", "Best steak in Indianapolis."),
    ("rev_013", "usr_005", "bizref_006", 5, "2024-02-15", "Worth every penny."),
    ("rev_014", "usr_001", "bizref_007", 4, "2024-03-20", "Smoky, tender ribs."),
    ("rev_015", "usr_002", "bizref_008", 3, "2024-01-30", "Simple but filling."),
    ("rev_016", "usr_003", "bizref_009", 5, "2024-02-08", "Specialty lattes are amazing."),
    ("rev_017", "usr_004", "bizref_010", 4, "2024-03-12", "Fresh sushi, fast service."),
    ("rev_018", "usr_005", "bizref_010", 5, "2024-01-14", "Best sushi outside Japan."),
]

MONGO_BUSINESSES = [
    {
        "business_id": "bizref_001", "name": "The Cozy Corner",
        "city": "Indianapolis", "state": "IN", "stars": 4.7,
        "review_count": 120, "categories": "Coffee, Wifi"
    },
    {
        "business_id": "bizref_002", "name": "Indy Grill House",
        "city": "Indianapolis", "state": "IN", "stars": 4.6,
        "review_count": 310, "categories": "Burgers, American"
    },
    {
        "business_id": "bizref_003", "name": "Broad Ripple Bistro",
        "city": "Indianapolis", "state": "IN", "stars": 3.5,
        "review_count": 88, "categories": "French, Fine Dining"
    },
    {
        "business_id": "bizref_004", "name": "Mass Ave Diner",
        "city": "Indianapolis", "state": "IN", "stars": 4.5,
        "review_count": 205, "categories": "Diners, Breakfast"
    },
    {
        "business_id": "bizref_005", "name": "Fountain Square Cafe",
        "city": "Indianapolis", "state": "IN", "stars": 4.0,
        "review_count": 67, "categories": "Cafes, Sandwiches"
    },
    {
        "business_id": "bizref_006", "name": "Circle City Steakhouse",
        "city": "Indianapolis", "state": "IN", "stars": 4.9,
        "review_count": 412, "categories": "Steakhouses, American"
    },
    {
        "business_id": "bizref_007", "name": "Speedway Smokehouse",
        "city": "Indianapolis", "state": "IN", "stars": 4.2,
        "review_count": 189, "categories": "BBQ, American"
    },
    {
        "business_id": "bizref_008", "name": "Garfield Park Eats",
        "city": "Indianapolis", "state": "IN", "stars": 3.3,
        "review_count": 54, "categories": "Comfort Food"
    },
    {
        "business_id": "bizref_009", "name": "Canal Walk Coffee",
        "city": "Indianapolis", "state": "IN", "stars": 4.8,
        "review_count": 143, "categories": "Coffee, Specialty"
    },
    {
        "business_id": "bizref_010", "name": "Meridian Street Sushi",
        "city": "Indianapolis", "state": "IN", "stars": 4.5,
        "review_count": 237, "categories": "Sushi, Japanese"
    },
]

MONGO_REVIEWS = [
    {"review_id": f"rev_{str(i).zfill(3)}", "business_id": f"bizref_{str((i % 10) + 1).zfill(3)}",
     "stars": [5, 4, 5, 4, 3, 5, 4, 3, 4, 5][i % 10], "text": "Great place!"}
    for i in range(1, 19)
]


async def seed_postgres(dsn: str) -> None:
    print(f"Connecting to PostgreSQL: {dsn.split('@')[-1]}")
    conn = await asyncpg.connect(dsn)
    try:
        # Drop and recreate tables
        await conn.execute("""
            DROP TABLE IF EXISTS review CASCADE;
            DROP TABLE IF EXISTS business_category CASCADE;
            DROP TABLE IF EXISTS "user" CASCADE;
            DROP TABLE IF EXISTS business CASCADE;
        """)
        await conn.execute("""
            CREATE TABLE business (
                business_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                review_count INT,
                is_open INT,
                attributes TEXT DEFAULT '',
                hours TEXT DEFAULT '',
                state_code TEXT,
                accepts_credit_cards BOOLEAN DEFAULT true,
                has_wifi BOOLEAN DEFAULT false,
                primary_categories TEXT DEFAULT ''
            );
        """)
        await conn.execute("""
            CREATE TABLE review (
                review_id TEXT PRIMARY KEY,
                user_id TEXT,
                business_id TEXT,
                stars INT,
                date TEXT,
                text TEXT
            );
        """)
        await conn.execute("""
            CREATE TABLE "user" (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                review_count INT DEFAULT 0,
                yelping_since TEXT DEFAULT '2020-01-01',
                useful INT DEFAULT 0,
                funny INT DEFAULT 0,
                cool INT DEFAULT 0,
                elite TEXT DEFAULT ''
            );
        """)

        # Insert businesses
        for b in BUSINESSES:
            await conn.execute(
                "INSERT INTO business(business_id,name,description,review_count,is_open,state_code) VALUES($1,$2,$3,$4,$5,$6)",
                *b
            )

        # Insert reviews
        for r in REVIEWS:
            await conn.execute(
                "INSERT INTO review(review_id,user_id,business_id,stars,date,text) VALUES($1,$2,$3,$4,$5,$6)",
                *r
            )

        # Insert dummy users
        for uid in ["usr_001", "usr_002", "usr_003", "usr_004", "usr_005"]:
            await conn.execute(
                'INSERT INTO "user"(user_id,name) VALUES($1,$2)',
                uid, uid.replace("usr_", "User ")
            )

        count = await conn.fetchval("SELECT COUNT(*) FROM business")
        print(f"PostgreSQL seeded: {count} businesses, {len(REVIEWS)} reviews.")
    finally:
        await conn.close()


def seed_mongo(uri: str, db_name: str) -> None:
    print(f"Connecting to MongoDB: {uri}")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]
    db.business.drop()
    db.review.drop()
    db.business.insert_many(MONGO_BUSINESSES)
    db.review.insert_many(MONGO_REVIEWS)
    print(f"MongoDB seeded: {len(MONGO_BUSINESSES)} businesses, {len(MONGO_REVIEWS)} reviews.")


async def main() -> None:
    dsn = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/oracleforge")
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongo_db = os.getenv("MONGODB_DATABASE", "yelp_db")

    await seed_postgres(dsn)
    seed_mongo(mongo_uri, mongo_db)
    print("\nDemo seed complete. Ready for recording.")


if __name__ == "__main__":
    asyncio.run(main())
