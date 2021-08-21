# cloud.mail.ru API
## About docs
All api calls are performed using the field `api` an instance of the class `CloudMail`.\
`CloudMail` instance will be named as `cm` in the all examples below.\
I will define two terms:
- *PyAPI*: python side interface of communication with official cloud.mail.ru API.
- *CloudAPI*: official cloud.mail.ru API, which my library uses.

## About Authentication and Identification
All user identification in CloudAPI's requests performing by passing cookies in requests\
Also you need to pass token(csrf) in requests to CloudAPI, except `tokens/csrf` method - it get csrf token based only on your valid cookies

Authentication steps:
- If two-factor disabled:
  - POST requets to `https://auth.mail.ru/cgi-bin/auth` with query that contain these fields:
    - `Login`
    - `Password`
  - Now you must have valid cookies
- If two-factor enabled:
  - POST requets to `https://auth.mail.ru/cgi-bin/auth` with query that contain these fields:
    - `Login`
    - `Password`
  - In previous response you will get redirect on `https://auth.mail.ru/cgi-bin/secstep`
  - Now you need to send POST request on `https://auth.mail.ru/cgi-bin/secstep` with thsese form fields:
    - `csrf`: it can be parsed from previous GET response (`https://auth.mail.ru/cgi-bin/secstep`)
    - `Login`
    - `AuthCode`: code that generate for you special app or sended to you by SMS
    - `Permament` (1 or 0): is server remember your device for next auths for passing this step
  - Now you must have valid cookies

## Methods
Usually api methods belong to a group of methods (file, folder, user)\
I'm going to describe about them also in the groups.
### About method calling
All CloudAPI calls are performed using the field `api` in instance of the class `CloudMail`\
`CloudMail` instance will be named as `cm` in the all examples below\
You can call CloudAPI directly by calling `api` field like:
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
All kwargs after `fullpath` will be passed directly on `requests`'s request method (get/post/put)
- `data` for pass dict as *application/x-www-form-urlencoded*
- `json` for pass dict as *application/json*
- `params` for pass dict as query

### Methods
#### About 'conflict'
In some methods (like file.add, folder.rename, etc), which may cause a conflict of names you can add a field `conflict`\
- `conflict` == `rename`: Server will rename file/folder as if you created the file/folder with the existing in the current directory name in Windows.
- `conflict` != `rename`: Server will raise exception `File(folder) already exist` or something like that.

*Default behavior is rename on conflict and you just need to pass `False` to change this*

#### File Group
#### *cloud.mail.ru/api/v2/file* 
- Method: `GET`
- Description: get information about file
- Response example:
```
{'body': {'hash': '9EE56D6C62B33379584F219648A908C37554C2FF',
          'home': '/Path/To/File/FileName.zip',
          'kind': 'file',
          'mtime': 1528621600,
          'name': 'FileName.zip',
          'size': 812828829,
          'type': 'file',
          'virus_scan': 'pass'},
 'email': 'email@mail.ru',
 'status': 200,
 'time': 1530370640869}
```
- PyAPI: `>>> cm.api.file(cloud_path: str)`
  - `cloud_path`: path to file in the cloud env
- CloudAPI: `GET https://cloud.mail.ru/api/v2/file`
  - Query:
    - `home`: **as `cloud_path` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/add* 
- Method: `POST`
- Description: add new file to cloud
- Response example:
```
{'body': '/Garbage/cookies.json',
 'email': 'email@mail.ru',
 'status': 200,
 'time': 1530371015566}
```
- PyAPI: `>>> cm.api.file.add(local_path: str, cloud_path: str, rename_on_conflict=True)`
  - `local_path`: path to file in the local env
  - `cloud_path`: path to file in the cloud env
  - `rename_on_conflict`: see [About conflict](#about-conflict) section
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/add`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `hash`: server file hash (SHA1 + salt), can be obtain by method `api.file._upload`
    - `size`: file size (Content-Lenght of PUT request while uploading file), can be obtain by method `api.file._upload`
    - `conflict`: see [About conflict](#about-conflict) section
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cld-uploaderXXX.cloud.mail.ru/upload-web*
*where XXX in url is uploading server, can be obtained by calling `/dispatcher`*
- Method: `PUT`
- Description: upload file to server
- CloudAPI Response example:
'1AA3F87D2F472FF076CB7E532B4543ACC706D0CB'
- PyAPI Response example:
('1AA3F87D2F472FF076CB7E532B4543ACC706D0CB', 662)
  - *where second element - size of the file*
- PyAPI: `>>> cm.api.file.add(local_path: str, cloud_path: str)`
  - `local_path`: path to file in the local env
- CloudAPI: `PUT cld-uploader12.cloud.mail.ru/upload-web`
  - multipart/form-data:
    - Just your file
  - api(...) call example:
    ```
    >>> response = mc.api(
        "https://cloclo21-upload.cloud.mail.ru/upload/",
        "put",
        fullpath=True,
        files={
            "file": (
                os.path.basename("Path/To/File/FileName.zip"),
                open("Path/To/File/FileName.zip", "rb"),
                "application/octet-stream"
            )
        }
    )
    >>> print(response.text, response.request.headers["Content-Length"])
    '4DE2BA407D546C7CFD34727B2FABC8CD41B4D2CD', '662'
    ```
#### *cloud.mail.ru/api/v2/file/remove* 
- Method: `POST`
- Description: remove a file from the cloud
- Response example:
```
{'body': '/Garbage/cookies.json',
 'email': 'email@mail.ru',
 'status': 200,
 'time': 1530448995599}
```
- PyAPI: `>>> cm.api.file.remove(cloud_path: str)`
  - `cloud_path`: path to file in the cloud env
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/remove`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/move* 
- Method: `POST`
- Description: move a file to another folder in the cloud
- Response example:
```
{'body': '/Garbage/TestDir/cookies.json',
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530449141906}
```
- PyAPI: `>>> cm.api.file.move(cloud_path: str, to_folder_path: str)`
  - `cloud_path`: path to file in the cloud env
  - `to_folder_path`: path to folder in while cloud will move file
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/move`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `folder`: **as `to_folder_path` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/rename* 
- Method: `POST`
- Description: rename the file
- Response example:
```
{'body': '/Garbage/TestDir/cookies_renamed.json',
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530449171906}
```
- PyAPI: `>>> cm.api.file.rename(cloud_path: str, new_name: str, rename_on_conflict=True)`
  - `cloud_path`: path to file in the cloud env
  - `new_name`: new file name
  - `rename_on_conflict`: see [About conflict](#about-conflict) section
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/rename`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `name`: **as `new_name` in PyAPI**
    - `conflict`: see [About conflict](#about-conflict) section
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/publish* 
- Method: `POST`
- Description: publish the file
  - Return weblink to a file
- Response example:
```
{'body': '6Piv/KCVSUz6BC',
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530450666068}
```
- PyAPI: `>>> cm.api.file.publish(cloud_path: str)`
  - `cloud_path`: path to file in the cloud env
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/publish`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/unpublish* 
- Method: `POST`
- Description: unpublish the file
- Response example:
```
{'body': '/garbage/qwe.json',
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530450815567}
```
- PyAPI: `>>> cm.api.file.unpublish(weblink: str)`
  - `weblink`: web link of the file
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/unpublish`
  - Urlencoded Form Data:
    - `weblink`: **as `weblink` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/copy* 
- Method: `POST`
- Description: copy file to another folder
- Response example:
```
{'body': '/Garbage/TestDir (1)/TestDir',
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530450984825}
```
- PyAPI: `>>> cm.api.file.rename(cloud_path: str, to_folder_path: str, rename_on_conflict=True)`
  - `cloud_path`: path to file in the cloud env
  - `to_folder_path`: copy's folder path
  - `rename_on_conflict`: see [About conflict](#about-conflict) section
- CloudAPI: `POST https://cloud.mail.ru/api/v2/file/copy`
  - Urlencoded Form Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `folder`: **as `to_folder_path` in PyAPI**
    - `conflict`: see [About conflict](#about-conflict) section
    - `token`: `csrf` token, see method `tokens/csrf`

#### *cloud.mail.ru/api/v2/file/history* 
- Method: `GET`
- Description: get history of the file
- Response example:
```
{'body': [{'name': 'ast.py',
           'path': '/Garbage/ast.py',
           'size': 12670,
           'time': 1530268079,
           'uid': 170724211}],
 'email': '9medved@mail.ru',
 'status': 200,
 'time': 1530451191051}
```
- PyAPI: `>>> cm.api.file.history(cloud_path: str)`
  - `cloud_path`: path to file in the cloud env
- CloudAPI: `GET https://cloud.mail.ru/api/v2/file/history`
  - Query Data:
    - `home`: **as `cloud_path` in PyAPI**
    - `token`: `csrf` token, see method `tokens/csrf`