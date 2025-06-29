import sqlite3

# Connexion à la base
conn = sqlite3.connect("bankily.db")
cursor = conn.cursor()

# Données utilisateurs
users = [
    (1000, "MH2025", "Mahfoudh", "ar", "Utilisateur"),
    (1001, "ID2025", "Idriss", "ar", "Utilisateur"),
    (1002, "HR2025", "Haroun", "ar", "Utilisateur"),
    (1003, "GH2025", "Ghazali", "ar", "Utilisateur"),
    (1004, "ME2025", "Meftah", "ar", "Utilisateur"),
    (2000, "AD2025", "Bechir", "fr", "Admin"),
    (2001, "AD2026", "Sidi Aly", "fr", "Admin")
]

# Données points
points = [
    ("Socogim", "MH2025", 0),      # capital à saisir plus tard
    ("Bawadi", "ID2025", 0),
    ("Kossovo", "HR2025", 0),
    ("Tarhil", "GH2025", 0),
    ("Istanbul", "ME2025", 0)
]

# Insertion dans les tables
cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)", users)
cursor.executemany("INSERT OR IGNORE INTO points VALUES (?, ?, ?)", points)

conn.commit()
conn.close()

print("✅ Données initiales insérées avec succès.")
