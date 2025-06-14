import hashlib
import os
import json

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """Calculate the hash of a file using the specified hash algorithm."""
    hash_func = hashlib.new(hash_algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def save_hashes(directory, output_file, hash_algorithm='sha256'):
    """Calculate and save hashes of all files in a directory."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = calculate_file_hash(file_path, hash_algorithm)
    
    with open(output_file, 'w') as f:
        json.dump(file_hashes, f, indent=4)

if __name__ == "__main__":
    target_url = input("Enter target URL (with http/https): ").strip()

    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            scan_xss(target_url)
            scan_sql_injection(target_url)
        else:
            print("[-] Unable to reach the target URL.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")
