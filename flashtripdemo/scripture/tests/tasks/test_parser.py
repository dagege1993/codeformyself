# coding: utf8

from tasks.gmail import do_request, is_order_message, parse_order_message

message_id = '15dbb8fb581d722d'
email = 'sww4718168@gmail.com'
token = {
    "_id":
    "59dc3de83faf68f6b31e1430",
    "access_token":
    "ya29.Gl3gBE_CqkDOcOnjs7U6qGOyONm-k04LxitbQGsk9ID93xvh2D9ovmb9On6zHzIuIDYNl1msvP01_AH9Fk5qj6tol1Aj48JzrOTPY1SAMSJqsqlpNJSR8SbV7BjYmoU",
    "expires_in":
    3547,
    "id_token":
    "eyJhbGciOiJSUzI1NiIsImtpZCI6ImMzODM1NWU3MjA5ZTlmOTkwOWJlODUxOTIyODhkMDg1OTY1NGEyOTUifQ.eyJhenAiOiI1NDMxNDU4MTE4NTktZWJobDAzb2Y1N3JjaG5vbG1kcHVwaHFpbnFmMW1hdm4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1NDMxNDU4MTE4NTktZWJobDAzb2Y1N3JjaG5vbG1kcHVwaHFpbnFmMW1hdm4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDMzMjg0NTk1MzE5ODgxMTMwMDIiLCJlbWFpbCI6InN3dzQ3MTgxNjhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJpRGZRY0lOX1dIdkNiZEZWVm5hUUFBIiwiaXNzIjoiYWNjb3VudHMuZ29vZ2xlLmNvbSIsImlhdCI6MTUwNzYxODU4MSwiZXhwIjoxNTA3NjIyMTgxfQ.LUQZZqlPqSrwpb0tu3matFumtm6YY-qDbd6mudlb7ZHn7_2bwUxl1mKfaXHKxkeGxEIIfqdMoa_drtJSZxm7IB2AMXhM49S1UCWbJqy3-xYrUyT9gCzk_MT6zEKt4Plbr325I4VV2gLCNCr3gDwf5YwjLzDtsUvA6Iree7LcqeTVqdp65lX8jK-q3pxiOuxUm3hU9qF2uNubPaUoZzvNlflRbuAjgIbZjU4KHlQlYSGqitZA4A1gnyeegUIyRXV2YBifbXx6fH2LtN54Kr8_0epBn5IIm1akcKczF4zpYlnXgISQ2_TOrbIBaSE0x4q84Kqx_3xKmdtV8azj2HT3sQ",
    "token_type":
    "Bearer",
    "updated_at":
    "2017-10-10T13:51:52.841Z",
    "email":
    "sww4718168@gmail.com",
    "id":
    "103328459531988113002",
    "first_name":
    "炜",
    "last_name":
    "宋",
    "username":
    None,
    "picture":
    "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
    "link":
    "https://plus.google.com/103328459531988113002",
    "locale":
    "zh-CN",
    "city":
    None,
    "country":
    None,
    "gender":
    None
}

async_result = do_request.delay(f'users/{email}/messages/{message_id}', token)

result = async_result

print(result.get().keys())

print(is_order_message.delay(result.result).get() is not False)

print(parse_order_message.delay(result.result, email, token['id']).get())
