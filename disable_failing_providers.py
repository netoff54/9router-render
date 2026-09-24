import sqlite3

# Connect to database
conn = sqlite3.connect('9router-data/db/data.sqlite')
cursor = conn.cursor()

# Disable failing providers
failing_providers = ['mistral', 'groq', 'cloudflare-ai', 'cohere']

print("Disabling failing providers:")
print("=" * 60)

for provider in failing_providers:
    cursor.execute("UPDATE providerConnections SET isActive = 0 WHERE provider = ?", (provider,))
    affected_rows = cursor.rowcount
    print(f"{provider.upper()}: Disabled {affected_rows} connection(s)")

conn.commit()

# Verify the changes
print("\nVerifying changes:")
print("=" * 60)

for provider in failing_providers:
    cursor.execute("SELECT name, isActive FROM providerConnections WHERE provider = ?", (provider,))
    connections = cursor.fetchall()

    if connections:
        print(f"\n{provider.upper()}:")
        for name, is_active in connections:
            status = "Active" if is_active else "Disabled"
            print(f"  - {name}: {status}")
    else:
        print(f"\n{provider.upper()}: No connections found")

conn.close()
print("\n" + "=" * 60)
print("Failing providers have been disabled successfully")
