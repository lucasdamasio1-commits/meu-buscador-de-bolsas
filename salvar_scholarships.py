from supabase import create_client
import os

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_scholarships(data):

    if not data:
        print("Nenhum dado para salvar")
        return

    supabase.table("scholarships")\
        .upsert(data, on_conflict="link")\
        .execute()

    print("Dados salvos no Supabase:", len(data))
