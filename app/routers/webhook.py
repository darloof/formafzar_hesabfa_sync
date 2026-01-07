from fastapi import APIRouter, status
from schemas.formafzar import FormafzarContactWebhook, FormafzarInvoiceWebhook
from services.hesabfa_client import HesabfaClient
from services.contact_service import get_or_create_contact
from services.invoice_service import create_invoice

import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("HESABFA_API_KEY")
USER_ID = os.getenv("HESABFA_USER_ID")
PASSWORD = os.getenv("HESABFA_PASSWORD")
LOGIN_TOKEN = os.getenv("HESABFA_LOGIN_TOKEN")

_missing = [name for name, val in (
    ("API_KEY", API_KEY),
    ("USER_ID", USER_ID),
    ("PASSWORD", PASSWORD),
    ("LOGIN_TOKEN", LOGIN_TOKEN),
) if not val]
if _missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(_missing)}")

router = APIRouter(prefix="/webhook")


@router.post("/formafzar/contact", status_code=status.HTTP_200_OK)
async def formafzar_contact_webhook(payload: FormafzarContactWebhook):
    client = HesabfaClient(
        api_key=API_KEY,
        user_id=USER_ID,
        password=PASSWORD,
        login_token=LOGIN_TOKEN,
    )

    contact = await get_or_create_contact(
        client,
        payload.contact.model_dump(),
    )

    return {
        "status": "success",
        "contact_code": contact["Code"],
    }

@router.post("/formafzar/invoice", status_code=status.HTTP_200_OK)
async def formafzar_invoice_webhook(payload: FormafzarInvoiceWebhook):
    client = HesabfaClient(
        api_key=API_KEY,
        user_id=USER_ID,
        password=PASSWORD,
        login_token=LOGIN_TOKEN,
    )

    invoice = await create_invoice(
        client,
        formafzar_invoice=payload.invoice.model_dump(),
    )

    return {
        "status": "success",
        "invoice_code": invoice["Invoice"]["Code"],
    }

@router.get("/odoo/contacts", status_code=status.HTTP_200_OK)
async def get_odoo_contacts():
    from services.odoo_client import OdooClient

    ODOO_URL = os.getenv("ODOO_URL")
    ODOO_DB = os.getenv("ODOO_DB")
    ODOO_API_KEY = os.getenv("ODOO_API_KEY")

    if not all([ODOO_URL, ODOO_DB, ODOO_API_KEY]):
        raise RuntimeError("Missing required Odoo environment variables.")

    odoo_client = OdooClient(
        url=ODOO_URL,
        db=ODOO_DB,
        api_key=ODOO_API_KEY,
    )

    contacts = odoo_client.search_read(
        model="res.partner",
        domain=[["is_company", "=", False]],
        fields=["name", "phone", "email"],
        limit=100,
    )

    return {
        "status": "success",
        "contacts": contacts,
    }