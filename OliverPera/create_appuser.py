# from chainlit.client.cloud import chainlit_client
# from chainlit.types import AppUser

# async def create_new_user():
#     app_users = [AppUser(username="admin",role="admin"), 
#                  AppUser(username="Olli",role="admin"),
#                  AppUser(username="Robin",role="admin"),
#                  AppUser(username="Timon",role="admin"),
#                  AppUser(username="Hellstern",role="admin")]
    
#     for user in app_users:
#         persisted_app_user = await chainlit_client.create_app_user(user)
        
#         if persisted_app_user:
#             print(f"App user created: {persisted_app_user.username}")
#         else:
#             print("Failed to create app user.")

    
