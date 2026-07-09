import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from supabase import create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key[:10] if supabase_key else 'None'}...")

if not supabase_url or not supabase_key:
    print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
    sys.exit(1)

try:
    sb = create_client(supabase_url, supabase_key)
    print("Client created successfully!")
    
    # Try listing users
    print("Trying to query 'users' table...")
    res = sb.table("users").select("*").limit(1).execute()
    print("Query success!")
    print(f"Data: {res.data}")
except Exception as e:
    print("Error occurred:")
    import traceback
    traceback.print_exc()
