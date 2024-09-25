from . import UserGlobalData

db = UserGlobalData("./user_global_data.db")

db.create_table("""
balance INTEGER NOT NULL DEFAULT 0,
picture_favorites TEXT,
shipping_cart TEXT
""")

print(db.select("*"))