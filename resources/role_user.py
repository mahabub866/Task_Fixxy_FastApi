from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException,Response
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from database import get_db
from models import RoleUserModel,RoleModel,BlockModel
import uuid
from schema import RoleUserCreate,LoginModel,RoleUserStatusUpdate,RoleUserUpdate,AdminSelfUserChangePasswordSchema,AdminUserChangePasswordSchema
from globalfun import decode_token,flatten_list_of_dicts,validation_user_management
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session, load_only
from dotenv import load_dotenv
import os



load_dotenv()

username=os.getenv("name")
password=os.getenv("password")


role_user_router = APIRouter(
    prefix='/v1/mak/role-user',
    tags=['RoleUser']

)

@role_user_router.get('/create/super-user', status_code=status.HTTP_201_CREATED)
async def super_admin(db: Session = Depends(get_db)):
    create_at=datetime.now()
    is_exixt=  db.query(RoleUserModel).first()
    uId=str(uuid.uuid4())
    if is_exixt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Super Admin User is Already Created")
    log={
         "message":"Super User Created",
        "create_at":str(create_at),
        "admin":"11223344"
    }
    new_role = RoleUserModel(uid=uId,username=str(username),password=generate_password_hash(str(password)),super_admin= True,role_id="11223344",logs=log,create_at=create_at)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {'status_code': status.HTTP_201_CREATED, 'success': True, 'message': "1st User Create Succesfully"}


@role_user_router.post('/login',status_code=status.HTTP_200_OK)
async def login(request:LoginModel,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    db_user=db.query(RoleUserModel).filter(RoleUserModel.username==request.username).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid User ID")

    db_role=db.query(RoleModel).filter(RoleModel.uid==db_user.role_id).first()
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Role Id")


    if db_user and check_password_hash(db_user.password,request.password):
        access_token=Authorize.create_access_token(subject=request.username)
        refresh_token=Authorize.create_refresh_token(subject=request.username)
       
       
        # print(db_user.token)
        data={}
        if db_user.token is None:
            payload=decode_token(access_token,db)
            # print(payload,'payloaddddd')
           
            db.query(RoleUserModel).filter(and_(RoleUserModel.username==request.username,RoleUserModel.username==db_user.username)).update({"token":access_token,"jti":payload['jti']})
            db.commit()
            token_value =db.query(RoleUserModel).filter(and_(RoleUserModel.token!=None,RoleUserModel.username==request.username)).first()
            role=db.query(RoleModel).filter(RoleModel.uid==token_value.role_id).first()
            data = {"access_token": token_value.token,"role":role.role,"username":db_user.username,"refresh_token":refresh_token}
            
        
        else:
            payloads=decode_token(db_user.token,db)
            # print(payloads,'payloads')
            if payloads is None:
                payload=decode_token(access_token,db)
                db.query(RoleUserModel).filter(RoleUserModel.username==request.username).update({"token":access_token,"jti":payload['jti']})
                db.commit()
                token_value =db.query(RoleUserModel).filter(and_(RoleUserModel.token!=None,RoleUserModel.username==request.username)).first()
                role=db.query(RoleModel).filter(RoleModel.uid==token_value.role_id).first()
                data = {"access_token": token_value.token,"role":role.role,"username":db_user.username,"refresh_token":refresh_token}
            else:
                block_token=BlockModel(block_id=str(uuid.uuid4()),token=db_user.token,username=payloads['sub'],jti=payloads['jti'],create_at=datetime.utcnow())
                db.add(block_token)
                db.commit()
                db.refresh(block_token)
           
           
            maks=db.query(RoleUserModel).filter(and_(RoleUserModel.token!=None,RoleUserModel.username==request.username)).first()
            if maks:
                payload=decode_token(access_token,db)
                db.query(RoleUserModel).filter(RoleUserModel.username==request.username).update({"token":access_token,"jti":payload['jti']})
                db.commit()
                token_value =db.query(RoleUserModel).filter(and_(RoleUserModel.token!=None,RoleUserModel.username==request.username)).first()
                role=db.query(RoleModel).filter(RoleModel.uid==token_value.role_id).first()
                data = {"access_token": token_value.token,"role":role.role,"username":db_user.username,"refresh_token":refresh_token}

        return jsonable_encoder(data)
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Password")
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Password")


@role_user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(request: RoleUserCreate, db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        is_exixt_id=  db.query(RoleUserModel).filter(RoleUserModel.username ==request.username).first()
        is_exixt_role=  db.query(RoleModel).filter(RoleModel.uid ==request.role).first()
        
        
        uId=str(uuid.uuid4())
        if is_exixt_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Id Already exist")
        if is_exixt_role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role is not found")
    
        
        log={
            "message":"New User Created",
            "create_at":str(create_at),
            "admin":str(username)
        }

        new_role = RoleUserModel(uid=uId,username=request.username,password=generate_password_hash(request.password),super_admin= False,role_id=request.role,active=request.active,logs=log,create_at= create_at)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'message': "User Create Succesfully"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
            

@role_user_router.get('/all', status_code=status.HTTP_200_OK)
async def all_user( db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        # data=db.query(RoleUserModel).options(load_only(*['name','username',"uid",'id','email','mobile_number','role_id','super_admin','active',"logs","create_at"])).all()
        data=db.query(RoleUserModel).all()
        result = [{ "username": item.username,"uid":item.uid,'id':item.id,'role_id':item.role_id,'super_admin':item.super_admin,'active':item.active,"logs":item.logs,"create_at":item.create_at} for item in data]
        
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'data': result}
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")


@role_user_router.put('/update/status', status_code=status.HTTP_201_CREATED)
async def update_status( request:RoleUserStatusUpdate,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        user=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()
        
        if user:
            if db.query(RoleUserModel).filter(and_(RoleUserModel.uid==request.uid,RoleUserModel.super_admin==True)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Super Admin is not editable")
            new_logs={}
            if request.active==True:
                new_logs={
                    "admin": str(username),
                    "message": "user is actived",
                    "create_at": str(create_at)
                }
            else:
                    new_logs={
                    "admin": str(username),
                    "message": "user is deactived",
                    "create_at": str(create_at)
                }

            logs = []
            logs.append(user.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            
            db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).update({'active': request.active,'logs':logs_data})
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"User Status is Update" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                

@role_user_router.put('/update', status_code=status.HTTP_201_CREATED)
async def update_user( request:RoleUserUpdate,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        user=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()
        
        

        if user:
            if db.query(RoleUserModel).filter(and_(RoleUserModel.uid==request.uid,RoleUserModel.super_admin==True)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Super Admin is not editable")
            role=db.query(RoleModel).filter(RoleModel.uid==request.role).first()
            print(role)
            if role is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role is not found")
            new_logs={
                "admin": str(username),
                "message": "user updated",
                "create_at": str(create_at)
            }
            logs = []
            logs.append(user.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).update({'active': request.active,'role_id':request.role,'logs':logs_data})
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"User Status is Update" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                
                
@role_user_router.put('/self/chnage-password', status_code=status.HTTP_201_CREATED)
async def self_pass_change( request:AdminSelfUserChangePasswordSchema,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        user=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()
        
        if user:
            
            new_logs={
                "admin": str(username),
                "message": "password changed",
                "create_at": str(create_at)
            }
            logs = []
            logs.append(user.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            old_password=check_password_hash(user.password,request.old_password)
            if  (user is not None) and (user.active) :

                check=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()

                if check is None:
                    raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="id does not match")

                if old_password ==False:
                    raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password Does Not Match")


                db.query(RoleUserModel).filter(RoleUserModel.uid == request.uid).update({'password': generate_password_hash(request.new_password) ,"logs":logs_data})
                db.commit()
                return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"Password Update Succesfully" }
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
    
                
@role_user_router.put('/user/chnage-password', status_code=status.HTTP_201_CREATED)
async def user_pass_change( request:AdminUserChangePasswordSchema,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        create_at=datetime.now()
        user=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()
        
        if user:
            if db.query(RoleUserModel).filter(and_(RoleUserModel.uid==request.uid,RoleUserModel.super_admin==True)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Super Admin is not editable")
            new_logs={
                "admin": str(username),
                "message": "user password changed",
                "create_at": str(create_at)
            }
            logs = []
            logs.append(user.logs)
            logs.append(new_logs)
            logs_data=flatten_list_of_dicts(logs)
            
            if  (user is not None) and (user.active) :

                check=db.query(RoleUserModel).filter(RoleUserModel.uid==request.uid).first()

                if check is None:
                    raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="id Does Not Match")
                
                db.query(RoleUserModel).filter(RoleUserModel.uid == request.uid).update({'password': generate_password_hash(request.new_password) ,"logs":logs_data})
                db.commit()
                return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"Password Update Succesfully" }
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                

@role_user_router.delete('/delete/{delete_id}', status_code=status.HTTP_201_CREATED)
async def delete_user(delete_id:str,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        user=db.query(RoleUserModel).filter(RoleUserModel.uid==delete_id).first()
        if user:
            if db.query(RoleUserModel).filter(and_(RoleUserModel.uid==delete_id,RoleUserModel.super_admin==True)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Super Admin is not Deletable")
            
            db.query(RoleUserModel).filter(RoleUserModel.uid==delete_id).delete()
            db.commit()
            return {'status_code': status.HTTP_201_CREATED, 'success': True,"message":"User is Deleted" }
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")
                

@role_user_router.get('/user-helper', status_code=status.HTTP_200_OK)
async def helper_user( db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    mak=Authorize.get_raw_jwt()
    Authorize.jwt_required()
    username=Authorize.get_jwt_subject()
    valid=validation_user_management(username, db,mak['jti'])
    if valid==True:
        data=db.query(RoleUserModel).options(load_only(*['username',"uid"])).all()
        result = [{"uid": item.uid, "username": item.username} for item in data]
        
        return {'status_code': status.HTTP_201_CREATED, 'success': True, 'data': result}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Something happened")



        