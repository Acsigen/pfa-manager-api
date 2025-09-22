from fastapi import APIRouter
from models.contract import Contract, delete_contract as delete_contract, list_contracts as list_contracts, show_contract as show_contract

router = APIRouter()

@router.post("/api/v1/clients/{client_id}/contracts")
async def add_contract_handler(contract: Contract):
    added_contract = contract.add()
    if type(added_contract) == Contract:
        return added_contract

@router.put("/api/v1/clients/{client_id}/contracts/{contract_id}")
async def update_contract_handler(contract_id: int, contract: Contract):
    updated_contract = contract.update(contract_id)
    if type(updated_contract) == Contract:
        return updated_contract

@router.get("/api/v1/clients/{client_id}/contracts/{contract_id}")
async def show_contract_handler(contract_id: int):
    contract = show_contract(contract_id)
    if type(contract) == Contract:
        return contract

@router.get("/api/v1/clients/{client_id}/contracts")
async def list_contracts_handler():
    contract_list = list_contracts()
    if type(contract_list) == list:
        return contract_list

@router.delete("/api/v1/clients/{client_id}/contracts/{contract_id}")
async def delete_contract_handler(contract_id: int):
    if delete_contract(contract_id=contract_id) == True:
        return "Contract deleted"