from app import ma
from app.models import Blacklist

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True

blacklist_schema = BlacklistSchema()
blacklists_schema = BlacklistSchema(many=True)