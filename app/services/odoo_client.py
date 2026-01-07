import requests
import json

class OdooClient:
    def __init__(self, url, db, api_key):
        """
        :param url: The base URL of your Odoo instance (e.g., https://my-company.odoo.com)
        :param db: The name of your Odoo database
        :param api_key: Your Odoo API Key (Generated under My Profile -> Account Security)
        """
        self.url = url.rstrip('/')
        self.db = db
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Odoo-Database': db
        }

    def _call(self, model, method, params):
        endpoint = f"{self.url}/json/2/{model}/{method}"
        response = requests.post(endpoint, headers=self.headers, json=params)
        
        if response.status_code != 200:
            raise Exception(f"Odoo API Error {response.status_code}: {response.text}")
            
        return response.json()

    def create(self, model, values):
        """
        Creates a record.
        :param values: Dictionary of field values (e.g. {'name': 'New Contact'})
        """
        # Note: Odoo expects a list of dictionaries for create
        return self._call(model, 'create', {'vals_list': [values]})

    def read(self, model, ids, fields=None):
        """
        Reads specific records.
        :param ids: List of record IDs to read
        :param fields: List of fields to fetch (optional)
        """
        params = {'ids': ids}
        if fields:
            params['fields'] = fields
        return self._call(model, 'read', params)

    def search_read(self, model, domain=None, fields=None, limit=10):
        """
        Search for records and read them in one call.
        :param domain: Odoo domain filter, e.g. [['is_company', '=', True]]
        """
        params = {
            'domain': domain or [],
            'fields': fields or [],
            'limit': limit
        }
        return self._call(model, 'search_read', params)

    def delete(self, model, ids):
        """
        Deletes (unlinks) records.
        :param ids: List of record IDs to delete
        """
        return self._call(model, 'unlink', {'ids': ids})