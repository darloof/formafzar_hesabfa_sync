from services.hesabfa_client import HesabfaClient


async def get_contact_by_mobile(client: HesabfaClient, mobile: str):
    result = await client.post(
        "/contact/getContacts",
        {
            "queryInfo": {
                "take": 1,
                "filters": [
                    {"property": "Mobile", "operator": "=", "value": mobile}
                ],
            }
        },
    )

    contacts = result.get("List", [])
    return contacts[0] if contacts else None


async def create_contact(client: HesabfaClient, contact_data: dict):
    return await client.post(
        "/contact/save",
        {"contact": contact_data},
    )


async def get_or_create_contact(client: HesabfaClient, formafzar_contact: dict):
    contact = await get_contact_by_mobile(client, formafzar_contact["mobile"])
    if contact:
        return contact

    result = await create_contact(
        client,
        {
            "name": formafzar_contact["name"],
            "mobile": formafzar_contact["mobile"],
            "email": formafzar_contact.get("email"),
            "address": formafzar_contact.get("address"),
            "contactType": 1,
            "active": True,
        },
    )
    return result["Contact"]
