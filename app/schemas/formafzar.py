from pydantic import BaseModel
from typing import List, Optional


class FormafzarItem(BaseModel):
    title: str
    qty: float
    price: float
    discount: Optional[float] = 0


class FormafzarContact(BaseModel):
    name: str
    mobile: str
    email: Optional[str]
    address: Optional[str]


class FormafzarInvoice(BaseModel):
    date: str
    due_date: Optional[str]
    notes: Optional[str]
    items: List[FormafzarItem]


class FormafzarContactWebhook(BaseModel):
    contact: FormafzarContact

class FormafzarInvoiceWebhook(BaseModel):
    invoice: FormafzarInvoice
