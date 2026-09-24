import sqlite3
import json

# Connect to database
conn = sqlite3.connect('9router-data/db/data.sqlite')
cursor = conn.cursor()

print("Provider Key Update Tool")
print("=" * 60)
print("Enter new API keys in format: provider_name:new_api_key")
print("Type 'done' when finished")
print("=" * 60)

while True:
    user_input = input("\nEnter provider:key (or 'done'): ").strip()

    if user_input.lower() == 'done':
        break

    if ':' not in user_input:
        print("Invalid format. Use: provider_name:new_api_key")
        continue

    provider, new_key = user_input.split(':', 1)
    provider = provider.strip().lower()
    new_key = new_key.strip()

    # Check if provider exists
    cursor.execute("SELECT name, data FROM providerConnections WHERE provider = ?", (provider,))
    connections = cursor.fetchall()

    if not connections:
        print(f"Provider '{provider}' not found in database")
        continue

    print(f"\nUpdating {provider.upper()} connections:")
    for name, data_json in connections:
        data = json.loads(data_json)
        old_key = data.get('apiKey', 'N/A')
        print(f"  - {name}: {old_key[:10]}...{old_key[-4:] if len(old_key) > 14 else old_key} -> {new_key[:10]}...{new_key[-4:]}")

        # Update the API key
        data['apiKey'] = new_key
        data['testStatus'] = 'active'  # Reset test status

        cursor.execute(
            "UPDATE providerConnections SET data = ? WHERE provider = ? AND name = ?",
            (json.dumps(data), provider, name)
        )

    conn.commit()
    print(f"Updated {len(connections)} connection(s) for {provider.upper()}")

conn.close()
print("\n" + "=" * 60)
print("Key updates completed successfully")
print("Run 'python test_providers_final.py' to test the updated connections")
