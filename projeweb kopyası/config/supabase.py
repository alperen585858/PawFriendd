import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=f"https://{os.getenv('SUPABASE_URL')}",
    supabase_key=os.getenv('SUPABASE_KEY')
)

# Initialize Supabase admin client (for backend operations)
supabase_admin: Client = create_client(
    supabase_url=f"https://{os.getenv('SUPABASE_URL')}",
    supabase_key=os.getenv('SUPABASE_SERVICE_KEY')
) 