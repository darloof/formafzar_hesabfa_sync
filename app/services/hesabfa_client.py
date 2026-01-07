import httpx

HESABFA_BASE_URL = "https://api.hesabfa.com/v1"


class HesabfaClient:
    def __init__(self, api_key, user_id, password, login_token):
        self.auth = {
            "apiKey": api_key,
            "userId": user_id,
            "password": password,
            "loginToken": login_token,
        }

    async def post(self, path: str, payload: dict):
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(
                f"{HESABFA_BASE_URL}{path}",
                json={**self.auth, **payload},
            )
            res.raise_for_status()
            return res.json()
