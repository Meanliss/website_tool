import requests
import json

try:
    response = requests.get('http://localhost:8000/api/tools')
    data = response.json()
    
    print(f"Total tools: {len(data)}")
    print("\nTools list:")
    for i, tool in enumerate(data, 1):
        print(f"{i}. {tool['id']} - {tool['name']} ({tool['category']})")
    
    # Test stats endpoint
    stats_response = requests.get('http://localhost:8000/api/stats')
    stats = stats_response.json()
    print(f"\n--- Stats ---")
    print(json.dumps(stats, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
