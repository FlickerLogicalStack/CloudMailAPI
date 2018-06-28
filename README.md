
# MailCloudAPI
Unofficial cloud.mail.ru's python API

### All existing methods in Cloud Mail API

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

##### *marked those that are implemented*
