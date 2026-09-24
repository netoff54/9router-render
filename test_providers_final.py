import sqlite3
import json
import requests

# Connect to database
conn = sqlite3.connect('9router-data/db/data.sqlite')
cursor = conn.cursor()

# Get provider connections
cursor.execute('SELECT * FROM providerConnections')
connections = cursor.fetchall()

print("Testing Active Provider Connections:")
print("=" * 60)

# Test endpoints for different providers
provider_endpoints = {
    'nvidia': 'https://integrate.api.nvidia.com/v1/models',
    'mistral': 'https://api.mistral.ai/v1/models',
    'gemini': 'https://generativelanguage.googleapis.com/v1/models',
    'groq': 'https://api.groq.com/openai/v1/models',
    'openrouter': 'https://openrouter.ai/api/v1/models',
    'cloudflare-ai': 'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search',
    'cerebras': 'https://api.cerebras.ai/v1/models',
    'cohere': 'https://api.cohere.ai/v1/models',
    'llm7': None,  # Custom provider, need specific endpoint
    'bazaarlink': None,  # Custom provider
    'ollama': None,  # Local provider
    'kiro': None  # OAuth provider
}

active_count = 0
success_count = 0

for connection in connections:
    # connection tuple: (id, provider, authType, name, email, priority, isActive, data, createdAt, updatedAt)
    provider = connection[1]
    name = connection[3]
    is_active = connection[6]
    data_json = connection[7]

    # Skip inactive providers
    if not is_active:
        continue

    active_count += 1
    data = json.loads(data_json)

    print(f"\n{provider.upper()} - {name}")
    print(f"  Status: Active")

    # Check if provider has test endpoint
    endpoint = provider_endpoints.get(provider)
    if endpoint:
        # Extract API key if available
        api_key = data.get('apiKey')

        if api_key:
            # Format endpoint for cloudflare
            if provider == 'cloudflare-ai':
                provider_specific = data.get('providerSpecificData', {})
                if isinstance(provider_specific, str):
                    provider_specific = json.loads(provider_specific)
                account_id = provider_specific.get('accountId')
                if account_id:
                    endpoint = endpoint.format(account_id=account_id)
                else:
                    print(f"  [WARN] No account ID found")
                    continue

            # Test the connection
            headers = {}
            if provider == 'nvidia':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'mistral':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'gemini':
                headers['x-goog-api-key'] = api_key
            elif provider == 'groq':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'openrouter':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'cerebras':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'cohere':
                headers['Authorization'] = f'Bearer {api_key}'
            elif provider == 'cloudflare-ai':
                headers['Authorization'] = f'Bearer {api_key}'

            try:
                response = requests.get(endpoint, headers=headers, timeout=10)

                if response.status_code == 200:
                    print(f"  [OK] Connection successful")
                    success_count += 1
                    models = response.json()
                    if 'data' in models:
                        print(f"  [INFO] Available models: {len(models['data'])}")
                elif response.status_code == 401:
                    print(f"  [ERROR] Authentication failed (401)")
                elif response.status_code == 403:
                    print(f"  [ERROR] Forbidden (403)")
                elif response.status_code == 404:
                    print(f"  [ERROR] Not found (404) - Endpoint or API key invalid")
                elif response.status_code == 429:
                    print(f"  [WARN] Rate limited (429)")
                else:
                    print(f"  [ERROR] Error: {response.status_code} - {response.text[:100]}")

            except requests.exceptions.Timeout:
                print(f"  [ERROR] Connection timeout")
            except requests.exceptions.ConnectionError:
                print(f"  [ERROR] Connection error")
            except Exception as e:
                print(f"  [ERROR] Error: {str(e)}")
        else:
            print(f"  [WARN] No API key found")
    else:
        print(f"  [INFO] No test endpoint configured for {provider}")

conn.close()
print("\n" + "=" * 60)
print(f"Test completed: {success_count}/{active_count} active providers working")
