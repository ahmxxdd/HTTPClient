import requests
import json
import sys

def get_user_input():
    url = input("Enter the request URL: ").strip()
    method = input("Enter HTTP method (GET, POST, PUT, DELETE): ").strip().upper()

    print("\nEnter headers (key:value), one per line. Leave empty to stop:")
    headers = {}
    while True:
        line = input()
        if not line.strip():
            break
        try:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            print("Invalid header format. Use key:value")

    body = None
    if method in ['POST', 'PUT']:
        print("\nEnter request body (press Enter to skip):")
        body = input()

    return url, method, headers, body

def send_request(url, method, headers, body):
    try:
        response = requests.request(method, url, headers=headers, data=body, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def format_response(response):
    print("\n✅ Response Received:")
    print(f"\nStatus Code: {response.status_code}")
    print("\nHeaders:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\nBody:")
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            parsed_json = response.json()
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            print(response.text)
    else:
        print(response.text)

def main():
    print("=== Enhanced HTTP Client ===\n")
    
    # Get user input
    url, method, headers, body = get_user_input()
    
    # Try sending the request and handle invalid URLs
    try:
        response = send_request(url, method, headers, body)
        format_response(response)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Invalid URL or connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
