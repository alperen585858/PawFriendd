from .supabase import supabase, supabase_admin
from typing import Dict, List, Any, Optional

class Database:
    @staticmethod
    def insert_data(table_name: str, data: Dict[str, Any]) -> Dict:
        """
        Insert data into a specified table
        """
        try:
            response = supabase.table(table_name).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error inserting data: {str(e)}")

    @staticmethod
    def select_all(table_name: str) -> List[Dict]:
        """
        Select all records from a specified table
        """
        try:
            response = supabase.table(table_name).select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error selecting data: {str(e)}")

    @staticmethod
    def select_by_id(table_name: str, id: int) -> Optional[Dict]:
        """
        Select a record by ID from a specified table
        """
        try:
            response = supabase.table(table_name).select("*").eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error selecting data by ID: {str(e)}")

    @staticmethod
    def update_by_id(table_name: str, id: int, data: Dict[str, Any]) -> Dict:
        """
        Update a record by ID in a specified table
        """
        try:
            response = supabase.table(table_name).update(data).eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error updating data: {str(e)}")

    @staticmethod
    def delete_by_id(table_name: str, id: int) -> Dict:
        """
        Delete a record by ID from a specified table
        """
        try:
            response = supabase.table(table_name).delete().eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error deleting data: {str(e)}")

    @staticmethod
    def custom_query(table_name: str, query: Any) -> List[Dict]:
        """
        Execute a custom query on a specified table
        """
        try:
            response = query.execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error executing custom query: {str(e)}") 