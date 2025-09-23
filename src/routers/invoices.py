from fastapi import APIRouter
from ..models.invoice import Invoice, delete_invoice, list_invoices, show_invoice

router: APIRouter = APIRouter()

@router.post(path="/api/v1/invoices")
async def add_invoice_handler(invoice: Invoice):
    added_invoice: Invoice = invoice.add()
    if type(added_invoice) is Invoice:
        return added_invoice

@router.put(path="/api/v1/invoices/{invoice_id}")
async def update_invoice_handler(invoice_id: int, invoice: Invoice):
    updated_invoice: Invoice = invoice.update(invoice_id=invoice_id)
    if type(updated_invoice) is Invoice:
        return updated_invoice

@router.get(path="/api/v1/invoices/{invoice_id}")
async def show_invoice_handler(invoice_id: int):
    invoice: Invoice = show_invoice(invoice_id=invoice_id)
    if type(invoice) is Invoice:
        return invoice

@router.get(path="/api/v1/invoices")
async def list_invoices_handler():
    invoice_list: list = list_invoices()
    if type(invoice_list) is list:
        return invoice_list

@router.delete(path="/api/v1/invoices/{invoice_id}")
async def delete_invoice_handler(invoice_id: int):
    if delete_invoice(invoice_id=invoice_id):
        return "Invoice deleted"