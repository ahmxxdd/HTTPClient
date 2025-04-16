import requests  # For making HTTP requests
import json      # For handling JSON data
import sys       # For exiting the program in case of errors

# Function to collect user input for the HTTP request
def get_user_input():
    url = input("Enter the request URL: ").strip()  # Get and strip the URL
    method = input("Enter HTTP method (GET, POST, PUT, DELETE): ").strip().upper()  # Get the method and convert to uppercase

    # Get headers from user input
    print("\nEnter headers (key:value), one per line. Leave empty to stop:")
    headers = {}
    while True:
        line = input()
        if not line.strip():
            break  # Exit loop on empty input
        try:
            key, value = line.split(":", 1)  # Split header line into key and value
            headers[key.strip()] = value.strip()
        except ValueError:
            print("Invalid header format. Use key:value")  # Handle malformed input

    # Get request body for POST or PUT
    body = None
    if method in ['POST', 'PUT']:
        print("\nEnter request body (press Enter to skip):")
        body = input()

    return url, method, headers, body  # Return all user inputs

# Function to send the HTTP request
def send_request(url, method, headers, body):
    try:
        # Use requests library to send the HTTP request with a 10 second timeout
        response = requests.request(method, url, headers=headers, data=body, timeout=10)
        return response  # Return the response object
    except requests.exceptions.RequestException as e:
        # Print error and exit if any request issue occurs
        print(f"\nError: {e}")
        sys.exit(1)

# Function to display and format the response
def format_response(response):
    print("\nResponse Received:")
    print(f"\nStatus Code: {response.status_code}")  # Print status code

    print("\nHeaders:")
    for key, value in response.headers.items():  # Print each header
        print(f"{key}: {value}")

    print("\nBody:")
    # Check content type to determine how to format the body
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            # Parse and print JSON response
            parsed_json = response.json()
            # Use JSON dump string for parsing
            print(json.dumps(parsed_json, indent=2)) # 2 spaces per indent
        except json.JSONDecodeError:
            # If parsing fails, just print raw text
            print(response.text)
    else:
        # Print body as plain text for non-JSON responses
        print(response.text)

# Main function to run the program
def main():
    print("=== Enhanced HTTP Client ===\n")
    
    # Get all necessary inputs from the user
    url, method, headers, body = get_user_input()
    
    # Send the HTTP request and handle potential errors
    try:
        response = send_request(url, method, headers, body)
        # Format and display the response
        format_response(response)
    except requests.exceptions.RequestException as e:
        # Handle and display any connection error
        print(f"\nInvalid URL or connection error: {e}")
        sys.exit(1)

# Run the program when the script is executed directly
if __name__ == "__main__":
    main()
