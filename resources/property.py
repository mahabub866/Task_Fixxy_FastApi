from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PropertyModel
import uuid
from schema import PropertyModelCreate,PropertyStatusUpdate,PropertyUpdate
from globalfun import flatten_list_of_dicts,validation_property_management
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session




property_router = APIRouter(
    prefix='/v1/mak/property',
    tags=['Property']

)


@property_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_property(request: PropertyModelCreate, db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_property_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
      
        log={
            "message":"New Property Created",
            "create_at":str(create_at),
            "admin":str(username)
        }
        uId=str(uuid.uuid4())
        new_property = PropertyModel(uid=uId,name=request.name,address=request.address,active=request.active,logs=log,create_at= create_at)
        db.add(new_property)
        db.commit()
        db.refresh(new_property)
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'message': "Property Create Succesfully"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
            

@property_router.get('/all', status_code=status.HTTP_200_OK)
async def all_property( db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_property_management(username, db,mak['jti'])
    if valid==True:
        # data=db.query(RoleUserModel).options(load_only(*['name','username',"uid",'id','email','mobile_number','role_id','super_admin','active',"logs","create_at"])).all()
        data=db.query(PropertyModel).all()
        result = [{ "name": item.name,"uid":item.uid,'id':item.id,'address':item.address,'active':item.active,"logs":item.logs,"create_at":item.create_at} for item in data]
        
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'data': result}
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")


@property_router.put('/update/status', status_code=status.HTTP_201_CREATED)
async def status_update( request:PropertyStatusUpdate,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_property_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        property=db.query(PropertyModel).filter(PropertyModel.uid==request.uid).first()
        
        if property:
        
            new_logs={}
            if request.active==True:
                new_logs={
                    "admin": str(username),
                    "message": "property is actived",
                    "create_at": str(create_at)
                }
            else:
                    new_logs={
                    "admin": str(username),
                    "message": "property is deactived",
                    "create_at": str(create_at)
                }

            logs = []
            logs.append(property.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            
            db.query(PropertyModel).filter(PropertyModel.uid==request.uid).update({'active': request.active,'logs':logs_data})
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"Property Status is Update" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                

@property_router.put('/update', status_code=status.HTTP_201_CREATED)
async def update_property( request:PropertyUpdate,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_property_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        property=db.query(PropertyModel).filter(PropertyModel.uid==request.uid).first()
        

        if property:
           
            new_logs={
                "admin": str(username),
                "message": "property updated",
                "create_at": str(create_at)
            }
            logs = []
            logs.append(property.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            db.query(PropertyModel).filter(PropertyModel.uid==request.uid).update({'active': request.active,"name":request.name,'address':request.address,'logs':logs_data})
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"Property is Update" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                
                
@property_router.delete('/delete/{delete_id}', status_code=status.HTTP_201_CREATED)
async def delete_property(delete_id:str,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_property_management(username, db,mak['jti'])
    if valid==True:
        property=db.query(PropertyModel).filter(PropertyModel.uid==delete_id).first()
        if property:
            
            db.query(PropertyModel).filter(PropertyModel.uid==delete_id).delete()
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"property is Deleted" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                



        