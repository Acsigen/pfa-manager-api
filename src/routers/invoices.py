from fastapi import APIRouter, Depends
from ..models.invoice import Invoice, InvoiceItem, list_user_invoices, list_client_invoices, show_invoice, delete_invoice_item, get_invoice_available_items, get_invoice_items
from ..models.activity_report import ActivityReport
from .auth import get_current_user
from typing import Annotated

router: APIRouter = APIRouter(tags=["invoices"])

user_dependency = Annotated[dict, Depends(dependency=get_current_user)]

# TODO: implement list invoice items
@router.post(path="/api/v1/invoices")
async def add_invoice_handler(user: user_dependency, invoice: Invoice):
    added_invoice: Invoice = invoice.add(user_id=user.get("user_id"))
    if type(added_invoice) is Invoice:
        return added_invoice


@router.post(path="/api/v1/invoices/{invoice_id}/items")
async def add_invoice_items_handler(invoice_item: InvoiceItem, invoice_id: int):
    invoice_item.invoice_id = invoice_id
    added_item: InvoiceItem = invoice_item.add()
    if type(added_item) is InvoiceItem:
        return added_item

@router.delete(path="/api/v1/invoices/{invoice_id}/items/{item_id}")
async def delete_invoice_items_handler(item_id: int):
    if delete_invoice_item(item_id=item_id):
        return "Item deleted"

@router.post(path="/api/v1/invoices/{invoice_id}/available_items")
async def get_invoice_available_items_handler(user: user_dependency, invoice: Invoice):
    available_items: list[ActivityReport] = get_invoice_available_items(client_id=invoice.client_id,invoice_id=invoice.id,user_id=user.get("user_id"))
    return available_items

@router.post(path="/api/v1/invoices/{invoice_id}/invoiced_items")
async def get_invoice_items_handler(user: user_dependency, invoice: Invoice):
    invoice_items: list[InvoiceItem] = get_invoice_items(client_id=invoice.client_id,invoice_id=invoice.id,user_id=user.get("user_id"))
    return invoice_items


@router.put(path="/api/v1/invoices/{invoice_id}")
async def update_invoice_handler(user: user_dependency, invoice_id: int, invoice: Invoice):
    updated_invoice: Invoice = invoice.update(user_id=user.get("user_id"), invoice_id=invoice_id)
    if type(updated_invoice) is Invoice:
        return updated_invoice


@router.get(path="/api/v1/invoices/{invoice_id}")
async def show_invoice_handler(user: user_dependency, invoice_id: int):
    invoice: Invoice = show_invoice(user_id=user.get("user_id"), invoice_id=invoice_id)
    if type(invoice) is Invoice:
        return invoice


@router.get(path="/api/v1/invoices")
async def list_user_invoices_handler(user: user_dependency):
    invoice_list: list = list_user_invoices(user_id=user.get("user_id"))
    if type(invoice_list) is list:
        return invoice_list

@router.get(path="/api/v1/invoices/")
async def list_client_invoices_handler(user: user_dependency, client_id: int):
    invoice_list: list = list_client_invoices(user_id=user.get("user_id"), client_id=client_id)
    if type(invoice_list) is list:
        return invoice_list
