#!/usr/bin/env python3

import requests
import subprocess
import os
import argparse
import getpass

def fetch_credentials_from_env():
    username = os.getenv('H1_API_USERNAME')
    api_token = os.getenv('H1_API_TOKEN')

    if not username or not api_token:
        print("Environment variables for API credentials are not set. Exiting.")
        return None, None

    return username, api_token

def fetch_scope_urls(username, api_key, program_handle):
    url = f"https://api.hackerone.com/v1/hackers/programs/{program_handle}/structured_scopes"
    headers = {
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers, auth=(username, api_key))
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    data = response.json()
    urls = []

    # Extract scope URLs from the API response
    for asset in data.get('data', []):
        if 'attributes' in asset and 'asset_identifier' in asset['attributes']:
            urls.append(asset['attributes']['asset_identifier'])

    return urls

def run_private_scope_command(username, token):
    try:
        # Run the private scope command and capture the output
        result = subprocess.run(
            ['bbscope', 'h1', '-u', username, '-t', token, '-p'],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def get_base_domain(url):
    domain_parts = url.split('.')
    if len(domain_parts) >= 2:
        return '.'.join(domain_parts[-2:])
    return url

def create_folder_and_write_file(base_path, domain_base, scope_name, urls):
    # Create the full path if it does not exist
    full_path = os.path.join(base_path, domain_base, scope_name)
    os.makedirs(full_path, exist_ok=True)

    # Define the file path
    file_path = os.path.join(full_path, f"{scope_name}-scope.txt")

    # Write the URLs to the file
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + "\n")

    print(f"Scope URLs have been written to {file_path}")

def create_single_folder_and_write_file(base_path, program_handle, urls):
    # Create the full path if it does not exist
    full_path = os.path.join(base_path, program_handle)
    os.makedirs(full_path, exist_ok=True)

    # Define the file path
    file_path = os.path.join(full_path, f"{program_handle}-scope.txt")

    # Write the URLs to the file
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + "\n")

    print(f"Scope URLs have been written to {file_path}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Fetch and organize scope information from HackerOne public and enrolled private programs.',
        epilog='Example usage:\n'
               '  ./get-h1-scope.py -p\n'
               '  (Fetch the private program scope you are enrolled in)\n\n'
               '  ./get-h1-scope.py netflix\n'
               '  (When using a program handle, the input should be the program name as it appears in the URL, e.g.\n'
               ' "netflix" for https://hackerone.com/netflix/policy_scopes.\n\n'
               ' Baptiste Bellecour.\n\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-p', action='store_true',
        help='Fetch the private program scope you are enrolled in. The output will be saved under \n'
             '"/home/<system_username>/bugBounty/private-bugbounty/<scope_name>/<scope_name>-scope.txt".\n\n'
    )
    parser.add_argument(
        'program_handle', nargs='?',
        help='The handle of the HackerOne program. Required if not using -p. \n'
             'The output will be saved under "/home/<system_username>/bugBounty/<program_handle>/<program_handle>-scope.txt".\n'
             'Example: For https://hackerone.com/netflix/policy_scopes, use "netflix" as the program handle.\n\n'
    )
    args = parser.parse_args()

    # Show help message if no arguments are provided
    if not args.p and not args.program_handle:
        parser.print_help()
        return

    # Fetch the API credentials from environment variables
    username, token = fetch_credentials_from_env()
    if not username or not token:
        print("API credentials could not be fetched. Exiting.")
        return

    # Get the current system user's username
    system_username = getpass.getuser()

    # Define the base path for creating folders
    base_path = f'/home/{system_username}/bugBounty'

    if args.p:
        # Run the private scope command and get the output
        output = run_private_scope_command(username, token)

        if output:
            # Split the output into lines (each line is a domain)
            urls = output.strip().split('\n')

            # Use "private-bugbounty" as the base name for the folder
            domain_base = "private-bugbounty"

            # Determine the base domain for the scope name
            if urls:
                base_domain = get_base_domain(urls[0])
                scope_name = base_domain.split('.')[0]
            else:
                scope_name = "unknown"

            # Create folder and write the scope URLs to the file
            create_folder_and_write_file(base_path, domain_base, scope_name, urls)
        else:
            print("No output from the private program scope command or an error occurred.")
    else:
        if not args.program_handle:
            print("Program handle is required when not using -p. Exiting.")
            return

        # Fetch scope URLs from the HackerOne API
        urls = fetch_scope_urls(username, token, args.program_handle)

        if urls:
            # Create folder and write the scope URLs to the file
            create_single_folder_and_write_file(base_path, args.program_handle, urls)
        else:
            print("No URLs found or an error occurred.")

    # Execute the sync script (optional, he is an a example on how to fire a script that will sync the results on your favorite cloud)
    # subprocess.run([f'/home/{system_username}/automation/sync_bug_bounty.sh'])

if __name__ == "__main__":
    main()

