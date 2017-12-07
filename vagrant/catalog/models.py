from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Spirit(Base):
    __tablename__ = 'spirit'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'id': self.id,
        'picture' : self.picture,
        'description' : self.description
        }

class Recipe(Base):
    __tablename__ = 'recipe'
    name = Column(String(120), nullable=False)
    id = Column(Integer, primary_key=True)
    picture = Column(String(8))
    description = Column(String(250))
    ingredients = Column(String)
    instructions = Column(String)
    spirit_id = Column(Integer, ForeignKey('spirit.id'))
    spirit = relationship(Spirit)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'id': self.id,
        'picture' : self.picture,
        'description' : self.description,
        'ingredients' : self.ingredients,
        'instructions' : self.instructions
        }


engine = create_engine('sqlite:///drinkcatalog.db')
 

Base.metadata.create_all(engine)