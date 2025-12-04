import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_KEY não foram definidos no .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

