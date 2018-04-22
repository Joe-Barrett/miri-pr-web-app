from peewee import *
from main import db


class BaseModel(Model):
    id = PrimaryKeyField()
    title = CharField(null=True)

    class Meta:
        database = db

		
class Users(BaseModel):
	name = CharField()
	pw = CharField()

class Contribution(BaseModel):
    map_location = CharField(null=True)
    shown_location = CharField(null=True)
    contributor = CharField(null=True)
    description = TextField(null=True)


class Image(BaseModel):
    file = BlobField()
    mimetype = CharField()
    contribution = ForeignKeyField(Contribution, backref='images', on_delete='CASCADE')
	

COUNTRIES = [
    'Albania',
    'Andorra',
    'Armenia',
    'Austria',
    'Azerbaijan',
    'Belarus',
    'Belgium',
    'Bosnia and Herzegovina',
    'Bulgaria',
    'Croatia',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Estonia',
    'Finland',
    'France',
    'Georgia',
    'Germany',
    'Greece',
    'Hungary',
    'Iceland',
    'Ireland',
    'Italy',
    'Kazakhstan',
    'Kosovo',
    'Latvia',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macedonia (FYROM)',
    'Malta',
    'Moldova',
    'Monaco',
    'Montenegro',
    'Netherlands',
    'Norway',
    'Poland',
    'Portugal',
    'Romania',
    'Russia',
    'San Marino',
    'Serbia',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sweden',
    'Switzerland',
    'Turkey',
    'Ukraine',
    'United Kingdom (UK)',
    'Vatican City (Holy See)',
		'USA',
		'Various Locations'
]
