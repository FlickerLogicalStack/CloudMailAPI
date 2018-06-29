# cloud.mail.ru API

All api calls are performed using the field `api` an instance of the class `CloudMail` \
`CloudMail` instance will be named as `cm` in the all examples below \
You can call api directly by calling `api` field like:
```
>>> cm.api(
        "dispatcher",
        "get",
        params={"token": cm.api.csrf_token}
    )
>>> cm.api(
    "file/copy",
    "post",
    data={
        "home": "/TestDir1",
        "folder": "/TestDir2",
        "token": cm.api.csrf_token
    })
```
or
```
>>> cm.api(
        "https://cloud.mail.ru/api/v2/dispatcher",
        "get",
        fullpath=True,
        params={
            "token": cm.api.csrf_token
        }
    )
>>> cm.api(
        "https://cloud.mail.ru/api/v2/file/copy",
        "post",
        fullpath=True,
        data={
            "home": "/TestDir1",
            "folder": "/TestDir2",
            "token": cm.api.csrf_token
        }
    )
```
## Groups
### File Group
#### *file*
Method: GET \
How to call: `>>> cm.api.file(cloud_path: str)` \
Params:
- `cloud_path`: path to file in cloud env

Query for direct api calling:
- `home`: cloud_path
- `token`: api.csrf_token

#### *https://clocloXXX-upload.cloud.mail.ru/upload/*
Method: PUT \
How to call: `>>> cm.api.file._upload_file(local_path: str)` \
Params:
- `local_path`: path in local env

Details:
- *No direct call from cm.api(...)* 
- *`XXX` is uploading server id, can be obtained from `api.dispatcher`*

#### *file/add*
Method: POST \
How to call: `>>> cm.api.file.add(local_path: str, cloud_path: str)` \
Params:
- `cloud_path`: path to file in cloud env
- `local_path`: path in local env

Raw api form data:
- `home`: cloud_path
- `hash`: must obtain by calling `>>> cm.api.file._upload_file(file_path: str)`
- `size`: must obtain by calling `>>> cm.api.file._upload_file(file_path: str)`
- `token`: api.csrf_token
- `conflict`: "rename"

Details:
- *field `conflict` can be ignored, but if there is a conflict of names, the server will raise an error*

#### *api.file.remove*
Method: POST \
How to call: `>>> cm.api.file.remove(cloud_path: str)` \
Params:
- `cloud_path`: path to file in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `token`: api.csrf_token

#### *api.file.move*
Method: POST \
How to call: `>>> cm.api.file.move(cloud_path: str, to_folder_path: str)` \
Params:
- `cloud_path`: path to file in cloud env
- `to_folder_path`: new file path in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `folder`: to_folder_path
- `token`: api.csrf_token

#### *api.file.rename*
Method: POST \
How to call: `>>> cm.api.file.rename(cloud_path: str, new_name: str)` \
Params:
- `cloud_path`: path to file in cloud env
- `new_name`: new file name in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `name`: new_name
- `token`: api.csrf_token
- `conflict`: "rename"

Details:
- *field `conflict` can be ignored, but if there is a conflict of names, the server will raise an error*

#### *api.file.publish*
Method: POST \
How to call: `>>> cm.api.file.publish(cloud_path: str)` \
Params:
- `cloud_path`: path to file in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `token`: api.csrf_token

#### *api.file.unpublish*
Method: POST \
How to call: `>>> cm.api.file.unpublish(web_link: str)` \
Params:
- `web_link`: weblink of already published file, can be obtain in `api.file.publish` response or in `api.file` lookup

Form data field(s) for direct api calling:
- `weblink`: weblink that you want to terminate
- `token`: api.csrf_token

#### *api.file.copy*
Method: POST \
How to call: `>>> cm.api.file.copy(cloud_path: str, to_folder_path: str)` \
Params:
- `cloud_path`: path to file in cloud env
- `to_folder_path`: file path of a copy in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `folder`: to_folder_path
- `token`: api.csrf_token
- `conflict`: "rename"
Details:
- *field `conflict` can be ignored, but if there is a conflict of names, the server will raise an error*

#### *api.file.history*
Method: POST \
How to call: `>>> cm.api.file.history(cloud_path: str)` \
Params:
- `cloud_path`: path to file in cloud env

Form data field(s) for direct api calling:
- `home`: cloud_path
- `token`: api.csrf_token
