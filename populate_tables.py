import uuid
import time
import psycopg2
from psycopg2.extras import execute_batch

def connect():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host="postgres", port=5432,
                database="airflow", user="postgres", password="postgres"
            )
            print("✅ Connecté à PostgreSQL")
            return conn
        except:
            print(f"⏳ Attente... ({i+1}/10)")
            time.sleep(3)
    raise Exception("❌ Impossible de se connecter")


conn = connect()
cur  = conn.cursor()

# 1. Récupérer le premier user
cur.execute("SELECT id FROM users LIMIT 1")
user = cur.fetchone()
if user is None:
    print("❌ Aucun user — crée d'abord un compte via http://localhost:8001/docs")
    exit(1)
user_id = user[0]
print(f"✅ User : {user_id}")


# 2. Peupler customers depuis segment_data (contient SegmentName)
cur.execute("SELECT COUNT(*) FROM customers")
if cur.fetchone()[0] > 0:
    print("⏭️  customers déjà peuplé")
else:
    cur.execute('SELECT "Age", "Income", "SegmentName" FROM segment_data')
    rows = cur.fetchall()
    data = [(str(uuid.uuid4()), int(float(r[0])), float(r[1]), r[2] or "Unknown") for r in rows]
    execute_batch(cur, """
        INSERT INTO customers (id, age, income, segment_label)
        VALUES (%s, %s, %s, %s)
    """, data)
    print(f"✅ {len(data)} customers insérés")


# 3. Peupler campaigns depuis segment_data
cur.execute("SELECT COUNT(*) FROM campaigns")
if cur.fetchone()[0] > 0:
    print("⏭️  campaigns déjà peuplé")
else:
    cur.execute('SELECT DISTINCT "CampaignType", "AdSpend", "CampaignChannel" FROM segment_data')
    rows = cur.fetchall()
    data = [(str(uuid.uuid4()), r[0], float(r[1]), r[2], "active", user_id) for r in rows]
    execute_batch(cur, """
        INSERT INTO campaigns (id, name, budget, channel, status, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, data)
    print(f"✅ {len(data)} campaigns insérées")


# 4. Vérification
conn.commit()
cur.execute("SELECT COUNT(*) FROM customers")
print(f"✅ Total customers : {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM campaigns")
print(f"✅ Total campaigns : {cur.fetchone()[0]}")

conn.close()
print("🎉 Terminé !")