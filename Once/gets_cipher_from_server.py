import subprocess

# Define the server and port
server = "13.229.93.88"
port = "9999"

# Open a file to store the hashes
with open("hash.txt", "w") as f:
    for _ in range(10):
        # Use subprocess to execute the nc command
        result = subprocess.run(
            ["nc", server, port],
            capture_output=True,
            text=True,
            timeout=10  # Set a timeout to avoid hanging indefinitely
        )
        
        # If there was output from the connection, write it to the file
        if result.stdout:
            f.write(result.stdout.strip() + "\n")
        else:
            print(f"Connection attempt {_+1} failed or no data received.")
