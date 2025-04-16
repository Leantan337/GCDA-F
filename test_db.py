#!/usr/bin/env python
"""
Database connection test script for Railway deployment debugging.
"""
import os
import sys
import json
import dj_database_url
from urllib.parse import urlparse

# Get DATABASE_URL from environment
database_url = os.environ.get('DATABASE_URL', '')
print(f"DATABASE_URL: {database_url}")

# Print parsed parts
if database_url:
    try:
        # Parse with urlparse
        print("\n== URLPARSE OUTPUT ==")
        parsed_url = urlparse(database_url)
        print(f"Scheme: {parsed_url.scheme}")
        print(f"Netloc: {parsed_url.netloc}")
        print(f"Path: {parsed_url.path}")
        print(f"Username: {parsed_url.username}")
        print(f"Password: [REDACTED]")
        print(f"Hostname: {parsed_url.hostname}")
        print(f"Port: {parsed_url.port}")
        
        # Parse with dj_database_url
        print("\n== DJ_DATABASE_URL OUTPUT ==")
        config = dj_database_url.parse(database_url)
        safe_config = {k: v if k != 'PASSWORD' else '[REDACTED]' for k, v in config.items()}
        print(f"Config: {json.dumps(safe_config, indent=2)}")
        
        # Try a basic connection test
        print("\n== CONNECTION TEST ==")
        try:
            import psycopg2
            print("Attempting to connect to PostgreSQL...")
            conn = psycopg2.connect(
                dbname=parsed_url.path[1:],
                user=parsed_url.username,
                password=parsed_url.password,
                host=parsed_url.hostname,
                port=parsed_url.port
            )
            print("Connection successful!")
            conn.close()
        except Exception as e:
            print(f"Connection failed: {e}")
            
        # Try network-related checks
        print("\n== NETWORK CHECKS ==")
        try:
            import socket
            print(f"Attempting to resolve hostname: {parsed_url.hostname}")
            ip_address = socket.gethostbyname(parsed_url.hostname)
            print(f"Resolved to IP: {ip_address}")
            
            print(f"Attempting to connect to socket: {parsed_url.hostname}:{parsed_url.port}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((parsed_url.hostname, parsed_url.port))
            print("Socket connection successful!")
            s.close()
        except Exception as e:
            print(f"Network check failed: {e}")
        
    except Exception as e:
        print(f"Error parsing database URL: {e}")
else:
    print("No DATABASE_URL found in environment variables.")

print("\n== ENVIRONMENT ==")
for key in os.environ:
    if key.startswith('RAILWAY_') or key.startswith('DATABASE_'):
        print(f"{key}: {os.environ[key] if not 'SECRET' in key and not 'PASSWORD' in key else '[REDACTED]'}")

# Print Python and system info
print("\n== SYSTEM INFO ==")
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
