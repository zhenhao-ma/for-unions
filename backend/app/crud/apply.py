from app.crud.base import CRUDBase
from app import schemas

class CRUDApply(CRUDBase[schemas.Apply.DB]): ...
apply = CRUDApply(schemas.Apply.DB, collection_name="apply")
