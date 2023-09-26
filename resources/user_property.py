
from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PropertyModel
import uuid
from globalfun import validation_regular_user_management
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from schema import RoleRegularUserCreate
from models import RoleUserModel,RoleModel
from werkzeug.security import generate_password_hash

uId=str(uuid.uuid4())

property_user_router = APIRouter(
    prefix='/v1/mak/property/user',
    tags=['Property User']

)


@property_user_router.get('/all', status_code=status.HTTP_200_OK)
async def all_property_for_user( db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_regular_user_management(username, db,mak['jti'])
    if valid==True:
        # data=db.query(RoleUserModel).options(load_only(*['name','username',"uid",'id','email','mobile_number','role_id','super_admin','active',"logs","create_at"])).all()
        data=db.query(PropertyModel).filter(PropertyModel.active==True).all()
        result = [{ "name": item.name,"uid":item.uid,'id':item.id,'address':item.address,'active':item.active,"logs":item.logs,"create_at":item.create_at} for item in data]
        
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'data': result}
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")

@property_user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def register_regular_user(request: RoleRegularUserCreate, db: Session = Depends(get_db)):
    valid=True
    if valid==True:
        create_at=datetime.now()
        is_exixt_id=  db.query(RoleUserModel).filter(RoleUserModel.username ==request.username).first()
        is_exixt_role=  db.query(RoleModel).filter(RoleModel.uid =="123456789").first()
        

        if is_exixt_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Id Already exist")
        if is_exixt_role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role is not found")
    
        
        log={
            "message":"Regular User Created",
            "create_at":str(create_at),
            "admin":str(request.username)
        }

        new_user = RoleUserModel(uid=uId,username=request.username,password=generate_password_hash(request.password),super_admin= False,role_id="123456789",active=True,logs=log,create_at= create_at)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'message': "Registrar Succesfully"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
   