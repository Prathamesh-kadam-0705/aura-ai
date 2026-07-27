from app.database.models.contact import Contact
from app.database.connection import SessionLocal


class ContactModule:


    def create(self, request):

        db = SessionLocal()

        contact = Contact(
            name=request.entities.get("name"),
            phone=request.entities.get("phone"),
            email=request.entities.get("email")
        )

        db.add(contact)
        db.commit()
        db.refresh(contact)

        db.close()


        return {
            "success": True,
            "message": "Contact saved successfully.",
            "data": {
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone,
                "email": contact.email
            }
        }



    def search(self, request):

        db = SessionLocal()

        name = request.entities.get("name")


        contact = (
            db.query(Contact)
            .filter(Contact.name.ilike(f"%{name}%"))
            .first()
        )


        db.close()


        if not contact:
            return {
                "success": False,
                "message": "Contact not found."
            }


        return {
            "success": True,
            "data":{
                "id":contact.id,
                "name":contact.name,
                "phone":contact.phone,
                "email":contact.email
            }
        }



    def list(self, request):

        db = SessionLocal()

        contacts = db.query(Contact).all()

        db.close()


        return {
            "success":True,
            "data":[
                {
                    "id":c.id,
                    "name":c.name,
                    "phone":c.phone,
                    "email":c.email
                }
                for c in contacts
            ]
        }



    def delete(self, request):

        db = SessionLocal()

        name = request.entities.get("name")


        contact = (
            db.query(Contact)
            .filter(Contact.name==name)
            .first()
        )


        if not contact:
            db.close()

            return {
                "success":False,
                "message":"Contact not found."
            }


        db.delete(contact)
        db.commit()

        db.close()


        return {
            "success":True,
            "message":"Contact deleted successfully."
        }



    def update(self, request):

        db = SessionLocal()


        name = request.entities.get("name")


        contact = (
            db.query(Contact)
            .filter(Contact.name==name)
            .first()
        )


        if not contact:
            db.close()

            return {
                "success":False,
                "message":"Contact not found."
            }


        if request.entities.get("phone"):
            contact.phone = request.entities.get("phone")


        if request.entities.get("email"):
            contact.email = request.entities.get("email")


        db.commit()
        db.refresh(contact)

        db.close()


        return {
            "success":True,
            "message":"Contact updated successfully.",
            "data":{
                "id":contact.id,
                "name":contact.name,
                "phone":contact.phone,
                "email":contact.email
            }
        }