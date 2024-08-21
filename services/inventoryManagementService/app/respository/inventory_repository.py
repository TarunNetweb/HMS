from sqlalchemy.orm import Session
from database.models import Inventory
from app.schemas.models import InventoryBase, InventoryUpdate
from datetime import datetime
import pytz
from fastapi import HTTPException, status

def get_full_Inventory(db: Session):
    inventory = db.query(Inventory).filter().all()
    return inventory

def get_specific_Inventory(name_of_equipment:str,db: Session):
    inventory = db.query(Inventory).filter(Inventory.name_of_equipment == name_of_equipment).first()
    return inventory

def get_specific_Inventory_by_id(inventory_id:int,db: Session):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    return inventory


def create_new_equipment(db: Session, new_equipment :  InventoryBase):
    inventory_new = Inventory(
        name_of_equipment =  new_equipment.name_of_equipment,
    category_of_equipment = new_equipment.category_of_equipment,
    stock_of_equipment =  new_equipment.stock_of_equipment,
    unit_price = new_equipment.unit_price,
    date_of_purchase = new_equipment.date_of_purchase
    )
    inventory_new.setTotalPrice()
    db.add(inventory_new)
    db.commit()
    db.refresh(inventory_new)
    inventory = db.query(Inventory).filter().all()
    return {"msg":"Equipment Addition Successful" , "new_inventory" : inventory}


def update_equipment(db: Session, updated_equipment :  InventoryUpdate,  equipment_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == equipment_id).first()
    
    if updated_equipment.stock_of_equipment and updated_equipment.unit_price:
        inventory.stock_of_equipment = updated_equipment.stock_of_equipment
        inventory.unit_price = updated_equipment.unit_price
        inventory.total_value = updated_equipment.stock_of_equipment * updated_equipment.unit_price
    
    if not updated_equipment.unit_price:
        inventory.unit_price = inventory.unit_price    
        inventory.stock_of_equipment = updated_equipment.stock_of_equipment
        inventory.total_value = updated_equipment.stock_of_equipment * inventory.unit_price 
    if not updated_equipment.stock_of_equipment:
        inventory.stock_of_equipment = inventory.stock_of_equipment
        inventory.unit_price = updated_equipment.unit_price
        inventory.total_value = inventory.stock_of_equipment * updated_equipment.unit_price 

    db.commit()
    inventory = db.query(Inventory).filter().all()
    return {"msg":"Equipment Updation Successful" , "new_inventory" : inventory}


def delete_equipment(db: Session, equipment_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == equipment_id).first()
    db.delete(inventory)
    db.commit()
    inventory = db.query(Inventory).filter().all()
    return {"msg":"Equipment deletion Successful" , "new_inventory" : inventory}