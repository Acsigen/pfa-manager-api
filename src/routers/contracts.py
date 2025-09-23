from fastapi import APIRouter
from ..models.contract import Contract, show_contract, list_contracts, delete_contract

router: APIRouter = APIRouter()

@router.post(path="/api/v1/clients/{client_id}/contracts")
async def add_contract_handler(client_id:int, contract: Contract):
    added_contract: Contract = contract.add(client_id=client_id)
    if type(added_contract) is Contract:
        return added_contract

@router.put(path="/api/v1/clients/{client_id}/contracts/{contract_id}")
async def update_contract_handler(contract_id: int, client_id: int, contract: Contract):
    updated_contract = contract.update(contract_id=contract_id,client_id=client_id)
    if type(updated_contract) is Contract:
        return updated_contract

@router.get(path="/api/v1/clients/{client_id}/contracts/{contract_id}")
async def show_contract_handler(contract_id: int, client_id: int):
    contract: Contract = show_contract(contract_id=contract_id, client_id=client_id)
    if type(contract) is Contract:
        return contract

@router.get(path="/api/v1/clients/{client_id}/contracts")
async def list_contracts_handler(client_id: int):
    contract_list = list_contracts(client_id)
    if type(contract_list) is list:
        return contract_list

@router.delete("/api/v1/clients/{client_id}/contracts/{contract_id}")
async def delete_contract_handler(contract_id: int, client_id: int):
    if delete_contract(contract_id=contract_id, client_id=client_id) is True:
        return "Contract deleted"