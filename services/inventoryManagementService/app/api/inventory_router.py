from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
#from app.schemas.models import EmployeeCreate,EmployeeLogin
from app.respository import inventory_repository as InvoRepo
from database.databaseconnection import SessionLocal
from app.schemas.models import InventoryBase, InventoryUpdate
from sqlalchemy.orm import Session

router = APIRouter()
auth_url = "http://192.168.0.135:5000/authentication"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/")
def getAllCategories( db:Session = Depends(get_db)):
    stocks = InvoRepo.get_full_Inventory(db)
    return stocks


@router.post("/stock")
async def makeNewStock(newEquipment:InventoryBase, db:Session = Depends(get_db)):
    Stocks = InvoRepo.get_specific_Inventory(db=db,name_of_equipment=newEquipment.name_of_equipment)
    if Stocks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Equipmaent already exists in the database")
    try:
        return InvoRepo.create_new_equipment(db=db,new_equipment=newEquipment)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

@router.put("/stock/{inventory_id}")
async def updateExistingStock(inventory_id: int, updated_inventory : InventoryUpdate ,db: Session = Depends(get_db)):
    Equipment = InvoRepo.get_specific_Inventory_by_id(inventory_id=inventory_id,db=db)
    if not Equipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Equipment not exist in the database")
    
    try:
        return InvoRepo.update_equipment(db=db, updated_equipment=updated_inventory, equipment_id=inventory_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

@router.patch("/stock/{inventory_id}")
async def updateExistingStock(inventory_id: int, updated_inventory : InventoryUpdate ,db: Session = Depends(get_db)):
    Equipment = InvoRepo.get_specific_Inventory_by_id(inventory_id=inventory_id,db=db)
    if not Equipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Equipment not exist in the database")
    
    try:
        return InvoRepo.update_equipment(db=db, updated_equipment=updated_inventory, equipment_id=inventory_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

@router.delete("/stock/{inventory_id}")
async def deleteExistingStock(inventory_id: int, db: Session = Depends(get_db)):
    Equipment = InvoRepo.get_specific_Inventory_by_id(inventory_id=inventory_id,db=db)
    if not Equipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Equipment not exist in the database")
    
    try:
        return InvoRepo.delete_equipment(db=db, equipment_id=inventory_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")

# async def makeNewStock(newEquipment:InventoryBase, db:Session = Depends(get_db)):
#     Stocks = InvoRepo.get_specific_Inventory(db=db,name_of_equipment=newEquipment.name_of_equipment)
#     if Stocks:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Equipmaent already exists in the database")
#     try:
#         return InvoRepo.create_new_equipment(db=db,new_equipment=newEquipment)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong !!")
