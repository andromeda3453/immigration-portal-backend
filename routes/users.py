from fastapi import APIRouter, HTTPException, Depends, Query
from database import supabase
# from auth import verify_password
from schemas import LoginRequest, UserDetails, EditUserDetailsRequest
from typing import Dict
from uuid import UUID
from auth import create_access_token, verify_token, get_current_user

router = APIRouter()


# @router.post("/login")
# async def login(credentials: LoginRequest):

#     response = supabase.table('users').select(
#         'id, password').eq("username", credentials.username).execute()

#     print(response)

#     if len(response.data) == 0:
#         raise HTTPException(status_code=401, detail="Account doesn't exist")
#     elif credentials.password != response.data[0]["password"]:
#         raise HTTPException(status_code=401, detail="Incorrect password")
#     else:
#         user_data = supabase.table('users').select(
#             "username,full_name,primary_email,alternative_email,contact_number,alternative_contact,nationality,passport_number,passport_expiry,passport_type,application_reference,service_package,category").eq("id", response.data[0]["id"]).execute().data[0]
#         user_progress = supabase.table('user_progress').select(
#             "*").eq("user_id", response.data[0]["id"]).execute().data[0]

#         print(user_data)
#         print(user_progress)

#         if not user_progress:
#             user_progress = {}

#         return {
#             "user_details": user_data,
#             "progress": user_progress
#         }
#         # return {"user_id": str(response["id"])}


@router.post("/login")
async def login(credentials: LoginRequest):
    response = supabase.table('users').select('id, password').eq(
        "username", credentials.username).execute()

    if len(response.data) == 0:
        raise HTTPException(status_code=401, detail="Account doesn't exist")
    elif credentials.password != response.data[0]["password"]:
        raise HTTPException(status_code=401, detail="Incorrect password")

    user_id = response.data[0]["id"]
    access_token = create_access_token(data={"sub": user_id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/me")
async def get_user_data(user_id: str = Depends(verify_token)):
    user_response = supabase.table('users').select(
        "username,full_name,primary_email,alternative_email,contact_number,alternative_contact,nationality,passport_number,passport_expiry,passport_type,application_reference,service_package,category"
    ).eq("id", user_id).execute()

    if len(user_response.data) == 0:
        raise HTTPException(status_code=404, detail="User not found")

    progress_response = supabase.table('user_progress').select(
        "*").eq("user_id", user_id).execute()
    user_data = user_response.data[0]
    user_progress = progress_response.data[0] if progress_response.data else {}

    return {
        "user_details": user_data,
        "progress": user_progress
    }


@router.put("/user/edit")
def edit_user_details(
    details: EditUserDetailsRequest,
    user: dict = Depends(get_current_user)
):
    updates = {k: v for k, v in details.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update.")

    response = supabase.table("users").update(
        updates).eq("id", user["user_id"]).execute()

    print(response)

    # if response.error:
    #     raise HTTPException(status_code=500, detail="Failed to update user details.")

    return {"message": "Updated successfully."}


@router.get("/health")
def health_check():
    return {"status": "ok"}
