from database.postgres import PostgresDB

from config.settings import DB_CONFIG


db = PostgresDB(DB_CONFIG)

companies = db.get_companies()

print(f"\nCompanies : {len(companies)}\n")

for company in companies[:20]:

    print(company)

db.close()