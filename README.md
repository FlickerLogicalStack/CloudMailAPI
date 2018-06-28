
# MailCloudAPI
Unofficial cloud.mail.ru's python API

## All existing methods in Cloud Mail API

| Implemented? | Method |          Path         |    Additional Info    |
|:------------:|:------:|:---------------------:|:---------------------:|
|              | (POST) | batch                 |                       |
|              | (POST) | clone                 |                       |
|              | (POST) | stock/save            |                       |
|              | (GET)  | dispatcher            |                       |
|              | (POST) | docs/token            |                       |
|              | (GET)  | file                  |                       |
|       X      | (POST) | file/add              |                       |
|       X      | (POST) | file/move             |                       |
|       X      | (POST) | file/remove           |                       |
|       X      | (POST) | file/rename           |                       |
|              | (POST) | file/copy             |                       |
|              | (POST) | file/publish          |                       |
|              | (POST) | file/unpublish        |                       |
|              | (GET)  | file/history          |                       |
|              | (GET)  | folder                |                       |
|       X      | (POST) | folder/add            |                       |
|       X      | (POST) | folder/move           |`Alias for file/move`  |
|       X      | (POST) | folder/remove         |`Alias for file/remove`|
|       X      | (POST) | folder/rename         |`Alias for file/rename`|
|              | (GET)  | folder/find           |                       |
|              | (GET)  | folder/invites        |                       |
|              | (GET)  | folder/shared/links   |                       |
|              | (GET)  | folder/invites/info   |                       |
|              | (POST) | folder/invites/reject |                       |
|              | (POST) | folder/mount          |                       |
|              | (GET)  | folder/shared/incomi  |                       |
|              | (GET)  | folder/shared/info    |                       |
|              | (POST) | folder/share          |                       |
|              | (GET)  | folder/tree           |                       |
|              | (POST) | folder/unmount        |                       |
|              | (POST) | folder/unshare        |                       |
|              | (POST) | folder/viruscan       |                       |
|              | (GET)  | mail/ab/contacts      |                       |
|              | (POST) | mail/ab/contacts/add  |                       |
|              | (GET)  | status                |                       |
|              | (POST) | tokens/csrf           |                       |
|              | (POST) | tokens/download       |                       |
|              | (GET)  | weblinks              |                       |
|              | (GET)  | weblinks/subscribe    |                       |
|              | (GET)  | user                  |                       |
|              | (POST) | user/agree-la         |                       |
|              | (POST) | user/edit             |                       |
|              | (POST) | user/unfreeze         |                       |
|              | (POST) | user/promo/active     |                       |
|              | (POST) | user/promo/ignore     |                       |
|              | (POST) | user/promo/invite     |                       |
|              | (POST) | user/promo/join       |                       |
|              | (GET)  | user/space            |                       |
|              | (POST) | zip                   |                       |
|              | (GET)  | mail/ab/contacts      |                       |
|              | (POST) | mail/ab/contacts/add  |                       |
|              | (GET)  | billing/rates         |                       |
|              | (POST) | billing/change        |                       |
|              | (POST) | billing/prolong       |                       |
|              | (POST) | billing/cancel        |                       |
|              | (POST) | billing/history       |                       |
|              | (GET)  | trashbin              |                       |
|              | (POST) | trashbin/restore      |                       |
|              | (POST) | trashbin/empty        |                       |
|              | (GET)  | domain/folders        |                       |
|              | (POST) | promo/validate        |                       |
|              | (POST) | notify/applink        |                       |

## Examples of usage
I decided implement the structure of the original API so for the `file/add` request you must call the method `MailCloud_instance.api.file.add(...)`.
All realized methods are described in the table above.
#### Basic usage
```
>>> import mail_cloud_api
>>> mc = mail_cloud_api.MailCloud("email@email.com", "password")
>>> mc.auth() # This method can ask AuthCode by input() if df auth enabled, run in inputable env
True
>>> mc.print(mc.api.file.add("/Some/Local/Dir/file.txt", "/Some/Cloud/Dir/file_qwe.txt"))
{'email': 'email@email.com', 'body': '/Some/Cloud/Dir/file_qwe.txt', 'time': 1530208363765, 'status': 200}
```
#### Cookies saving/loading
For identification mail.ru use cookies.
It would be a shame if every session you would have to authenticate again, so I implemented methods to load/save cookies to a json file.
```
>>> import mail_cloud_api
>>> mc_temp = mail_cloud_api.MailCloud("email@email.com", "password")
>>> mc_temp.auth()
True
>>> mc.save_cookies_to_file("/Some/Local/Dir/cookies.json")
<RequestsCookieJar[<Cookie GarageID=7d1958e70...>]
>>> del mc_temp
>>> mc = mail_cloud_api.MailCloud("email@email.com", "password")
>>> mc.load_cookies_from_file("/Some/Local/Dir/cookies.json")
<RequestsCookieJar[<Cookie GarageID=7d1958e70...>]
>>> mc.print(mc.api.file.add("/Some/Local/Dir/file.txt", "/Some/Cloud/Dir/file_qwe.txt"))
{'email': 'email@email.com', 'body': '/Some/Cloud/Dir/file_qwe.txt', 'time': 1530208363765, 'status': 200}
```

Also there is a method `def update_cookies_from_dict(self, dict_={}, **kwargs) -> RequestsCookieJar` that has a same effect as `load_cookies_from_file`