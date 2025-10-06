from marshmallow import pre_load
from ...extensions import ma
from ...models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_fk = True
        load_instance = False
        ordered = True
    
    @pre_load
    def process_input(self, data, **kwargs):
        """Convert Postman-style fields to database fields"""
        # Handle 'name' -> 'full_name'
        if 'name' in data and 'full_name' not in data:
            data['full_name'] = data.pop('name')
        
        # Handle 'salary' (dollars) -> 'salary_cents'
        if 'salary' in data and 'salary_cents' not in data:
            # Assuming salary is in dollars, convert to cents
            data['salary_cents'] = int(data.pop('salary') * 100)
        
        return data

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
