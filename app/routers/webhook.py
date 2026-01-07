from fastapi import APIRouter, status
from schemas.formafzar import FormafzarWebhook
from services.hesabfa_client import HesabfaClient
from services.contact_service import get_or_create_contact
from services.invoice_service import create_invoice

router = APIRouter(prefix="/webhook")


@router.post("/formafzar", status_code=status.HTTP_200_OK)
async def formafzar_webhook(payload: FormafzarWebhook):
    client = HesabfaClient(
        api_key="API_KEY",
        user_id="USER_ID",
        password="PASSWORD",
        login_token="LOGIN_TOKEN",
    )

    # 1️⃣ Contact
    contact = await get_or_create_contact(
        client,
        payload.contact.dict(),
    )

    # 2️⃣ Invoice
    invoice = await create_invoice(
        client,
        contact_code=contact["Code"],
        formafzar_invoice=payload.invoice.dict(),
    )

    return {
        "status": "success",
        "contact_code": contact["Code"],
        "invoice_code": invoice["Invoice"]["Code"],
    }
