from fastapi import APIRouter
from ..models.contract import Contract, show_contract #, delete_contract, list_contracts

router: APIRouter = APIRouter()

@router.post(path="/api/v1/clients/{client_id}/contracts")
async def add_contract_handler(client_id:int, contract: Contract):
    added_contract: Contract = contract.add(client_id=client_id)
    if type(added_contract) is Contract:
        return added_contract

# @router.put("/api/v1/clients/{client_id}/contracts/{contract_id}")
# async def update_contract_handler(contract_id: int, contract: Contract):
#     updated_contract = contract.update(contract_id)
#     if type(updated_contract) == Contract:
#         return updated_contract

@router.get("/api/v1/clients/{client_id}/contracts/{contract_id}")
async def show_contract_handler(contract_id: int):
    contract = show_contract(contract_id=contract_id)
    if type(contract) is Contract:
        return contract

# @router.get("/api/v1/clients/{client_id}/contracts")
# async def list_contracts_handler():
#     contract_list = list_contracts()
#     if type(contract_list) == list:
#         return contract_list

# @router.delete("/api/v1/clients/{client_id}/contracts/{contract_id}")
# async def delete_contract_handler(contract_id: int):
#     if delete_contract(contract_id=contract_id) == True:
#         return "Contract deleted"