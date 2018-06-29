
# CloudMailAPI
Unofficial cloud.mail.ru's python API

## All existing methods in cloud.mail.ru's API

| Implemented? | Method |         Path          |      Additional Info     |
|:------------:|:------:|:---------------------:|:------------------------:|
|              | (POST) | batch                 |                          |
|              | (POST) | clone                 |                          |
|              | (POST) | stock/save            |                          |
|       X      | (GET)  | dispatcher            |                          |
|              | (POST) | docs/token            |                          |
|       X      | (GET)  | file                  |                          |
|       X      | (POST) | file/add              |                          |
|       X      | (POST) | file/move             |                          |
|       X      | (POST) | file/remove           |                          |
|       X      | (POST) | file/rename           |                          |
|       X      | (POST) | file/copy             |                          |
|       X      | (POST) | file/publish          |                          |
|       X      | (POST) | file/unpublish        |                          |
|              | (GET)  | file/history          |                          |
|       X      | (GET)  | folder                |                          |
|       X      | (POST) | folder/add            |                          |
|       X      | (POST) | folder/move           |`Alias for file/move`     |
|       X      | (POST) | folder/remove         |`Alias for file/remove`   |
|       X      | (POST) | folder/rename         |`Alias for file/rename`   |
|       X      | (POST) | folder/copy           |`Alias for file/copy`     |
|       X      | (POST) | folder/publish        |`Alias for file/publish`  |
|       X      | (POST) | folder/unpublish      |`Alias for file/unpublish`|
|              | (GET)  | folder/find           |                          |
|              | (GET)  | folder/invites        |                          |
|              | (GET)  | folder/shared/links   |                          |
|              | (GET)  | folder/invites/info   |                          |
|              | (POST) | folder/invites/reject |                          |
|              | (POST) | folder/mount          |                          |
|              | (GET)  | folder/shared/incomi  |                          |
|              | (GET)  | folder/shared/info    |                          |
|              | (POST) | folder/share          |                          |
|              | (GET)  | folder/tree           |                          |
|              | (POST) | folder/unmount        |                          |
|              | (POST) | folder/unshare        |                          |
|              | (POST) | folder/viruscan       |                          |
|              | (GET)  | mail/ab/contacts      |                          |
|              | (POST) | mail/ab/contacts/add  |                          |
|              | (GET)  | status                |                          |
|       X      | (POST) | tokens/csrf           |                          |
|       X      | (POST) | tokens/download       |                          |
|              | (GET)  | weblinks              |                          |
|              | (GET)  | weblinks/subscribe    |                          |
|              | (GET)  | user                  |                          |
|              | (POST) | user/agree-la         |                          |
|              | (POST) | user/edit             |                          |
|              | (POST) | user/unfreeze         |                          |
|              | (POST) | user/promo/active     |                          |
|              | (POST) | user/promo/ignore     |                          |
|              | (POST) | user/promo/invite     |                          |
|              | (POST) | user/promo/join       |                          |
|       X      | (GET)  | user/space            |                          |
|       X      | (POST) | zip                   |                          |
|              | (GET)  | mail/ab/contacts      |                          |
|              | (POST) | mail/ab/contacts/add  |                          |
|              | (GET)  | billing/rates         |                          |
|              | (POST) | billing/change        |                          |
|              | (POST) | billing/prolong       |                          |
|              | (POST) | billing/cancel        |                          |
|              | (POST) | billing/history       |                          |
|       X      | (GET)  | trashbin              |                          |
|       X      | (POST) | trashbin/restore      |                          |
|       X      | (POST) | trashbin/empty        |                          |
|              | (GET)  | domain/folders        |                          |
|              | (POST) | promo/validate        |                          |
|              | (POST) | notify/applink        |                          |

## Examples of usage
I decided implement the structure of the original API so for the `file/add` request you must call the method `MailCloud_instance.api.file.add(...)`.
All realized methods are described in the table above.
#### Basic usage
```
>>> import cloud_mail_api
>>> cm = cloud_mail_api.CloudMail("email@email.com", "password")
>>> cm.auth() # This method can ask AuthCode by input() if df auth enabled, run in inputable env
True
>>> cm.print(cm.api.file.add("/Some/Local/Dir/file.txt", "/Some/Cloud/Dir/file_qwe.txt"))
{'email': 'email@email.com', 'body': '/Some/Cloud/Dir/file_qwe.txt', 'time': 1530208363765, 'status': 200}
```
#### Cookies saving/loading
For identification mail.ru use cookies.
It would be a shame if every session you would have to authenticate again, so I implemented methods to load/save cookies to a json file.
```
>>> import cloud_mail_api
>>> cm_temp = cloud_mail_api.CloudMail("email@email.com", "password")
>>> cm_temp.auth()
True
>>> cm.save_cookies_to_file("/Some/Local/Dir/cookies.json")
<RequestsCookieJar[<Cookie GarageID=7d1958e70...>]
>>> del cm_temp
>>> cm = cloud_mail_api.CloudMail("email@email.com", "password")
>>> cm.load_cookies_from_file("/Some/Local/Dir/cookies.json")
<RequestsCookieJar[<Cookie GarageID=7d1958e70...>]
>>> cm.print(cm.api.file.add("/Some/Local/Dir/file.txt", "/Some/Cloud/Dir/file_qwe.txt"))
{'email': 'email@email.com', 'body': '/Some/Cloud/Dir/file_qwe.txt', 'time': 1530208363765, 'status': 200}
```

Also there is a method `def update_cookies_from_dict(self, dict_={}, **kwargs) -> RequestsCookieJar` that has a same effect as `load_cookies_from_file`