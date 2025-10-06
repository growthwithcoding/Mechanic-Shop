from ...extensions import ma
from ...models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_fk = True
        load_instance = False
        ordered = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
