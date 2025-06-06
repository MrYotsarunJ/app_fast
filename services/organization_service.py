from sqlalchemy.orm import Session
from database import Organization

async def list_organization(db:Session, params):
     out = db.query(Organization)
     out =out.filter(Organization.sub_domain != None)

     q = params.get("q", None)
     if q and q.strip() != "":
        q = q.replace(" ", "")
        q = q.lower()
        out = out.filter(Organization.org_name.like(f"%{q}%"))

     out_list = []
     for pg in out:
        my_dict = pg.__dict__
        out_list.append(my_dict)

     return out_list