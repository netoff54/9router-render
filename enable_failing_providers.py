import sqlite3

# Connect to database
conn = sqlite3.connect('9router-data/db/data.sqlite')
cursor = conn.cursor()

# Re-enable previously disabled providers
providers_to_enable = ['mistral', 'groq', 'cloudflare-ai', 'cohere']

print("Re-enabling providers:")
print("=" * 60)

for provider in providers_to_enable:
    cursor.execute("UPDATE providerConnections SET isActive = 1 WHERE provider = ?", (provider,))
    affected_rows = cursor.rowcount
    print(f"{provider.upper()}: Re-enabled {affected_rows} connection(s)")

conn.commit()

# Verify the changes
print("\nVerifying changes:")
print("=" * 60)

for provider in providers_to_enable:
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
print("Providers have been re-enabled successfully")
print("Note: These providers will still fail until you update their API keys")
