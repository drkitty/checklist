from base64 import b16encode, b16decode
from hashlib import pbkdf2_hmac, sha256
from os import urandom

from sqlalchemy import Boolean, Column, String, Text

from .core import Base
import settings.python as settings


class Item(Base):
    __tablename__ = 'item'

    id = Column(String(32), primary_key=True)
    done = Column(Boolean)
    description = Column(Text)


class User(Base):
    __tablename__ = 'user'

    name = Column(String(128), primary_key=True)
    pw_hash = Column(String(64))
    pw_salt = Column(String(64))

    def set_password(self, password):
        self.pw_salt = b16encode(urandom(32)).decode('ascii')
        self.pw_hash = self.hash(password)

    def test_password(self, password):
        return self.hash(password) == self.pw_hash

    def hash(self, password):
        #text = password.encode('utf-8') + b16decode(self.pw_salt)
        return b16encode(pbkdf2_hmac(
            hash_name='sha256', password=password.encode('utf-8'),
            salt=b16decode(self.pw_salt),
            iterations=settings.hash_rounds)).decode('ascii')
