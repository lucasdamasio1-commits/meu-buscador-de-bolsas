from supabase_client import supabase

def salvar_scholarships(lista):

    for item in lista:

        data = {
            "title": item.get("title"),
            "description": item.get("description"),
            "provider": item.get("provider"),
            "link": item.get("link"),
            "deadline": item.get("deadline")
        }

        supabase.table("scholarship").insert(data).execute()
