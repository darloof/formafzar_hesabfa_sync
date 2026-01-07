from services.hesabfa_client import HesabfaClient


async def create_invoice(
    client: HesabfaClient,
    contact_code: int,
    formafzar_invoice: dict,
):
    invoice = {
        "contactCode": contact_code,
        "date": formafzar_invoice["date"],
        "dueDate": formafzar_invoice.get("due_date"),
        "items": [
            {
                "description": item["title"],
                "quantity": item["qty"],
                "unitPrice": item["price"],
                "discount": item.get("discount", 0),
            }
            for item in formafzar_invoice["items"]
        ],
        "notes": formafzar_invoice.get("notes"),
    }

    return await client.post(
        "/invoice/save",
        {"invoice": invoice},
    )
