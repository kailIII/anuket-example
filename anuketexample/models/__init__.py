# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# SQLAlchemy models imports
from anuket.models.auth import AuthUser, AuthGroup
from anuket.models.migration import Migration

# Root factory (ACLS)
from anuket.models.rootfactory import RootFactory
