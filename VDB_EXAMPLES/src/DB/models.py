from sqlalchemy import Column, String, PrimaryKeyConstraint

from . import database

# progress_queue Table
class progress_queue(database.Base):
    __tablename__ = 'progress_queue'
    __table_args__= (PrimaryKeyConstraint('cve', 'commit', 'crawlType', 'vendor', 'product'), )
    cve         = Column(String(25))
    commit      = Column(String(60))
    crawlType   = Column(String(255))
    vendor   = Column(String(255))
    product   = Column(String(255))

    def __init__(self, cve, commit, crawlType, vendor, product):
        self.cve        = cve
        self.commit     = commit
        self.crawlType  = crawlType
        self.vendor     = vendor
        self.product    = product

    def __repr__(self):
        return "<progress_queue('%s', '%s', '%s', '%s', '%s'>" % (self.cve, self.commit, self.crawlType, self.vendor, self.product)

# cve_cpe Table
class cve_cpe(database.Base):
    __tablename__ = 'cve_cpe'
    __table_args__= (PrimaryKeyConstraint('vendor', 'product', 'cve'), )
    vendor = Column(String(255))
    product = Column(String(255))
    version = Column(String)
    cve = Column(String(25))

    def __init__(self, vendor, product, version, cve):
        self.vendor = vendor
        self.product = product
        self.version = version
        self.cve = cve

    def __repr__(self):
        return "<cve_cpe('%s', '%s', '%s'>" %(self.vendor, self.product, self.cve)

# cve_url Table
class cve_url(database.Base):
    __tablename__ = 'cve_url'
    __table_args__ = (PrimaryKeyConstraint('cve', 'url'), )
    cve = Column(String(25))
    url = Column(String(500))
    name = Column(String(500))
    refsource = Column(String(255))
    tags = Column(String(255))

    def __init__(self, cve, url, name, refsource, tags):
        self.cve = cve
        self.url = url
        self.name = name
        self.refsource = refsource
        self.tags = tags

    def __repr__(self):
        return "<cve_url('%s', '%s', '%s', '%s', '%s'>" %(self.cve, self.url, self.name, self.refsource, self.tags)


# cve_data Table
class cve_data(database.Base):
    __tablename__ = 'cve_data'
    __table_args__ = (PrimaryKeyConstraint('cve'), )
    cve = Column(String(25))
    cvssV2 = Column(String(10))
    cvssV3 = Column(String(10))
    cwe = Column(String(300))
    def __init__(self, cve, cvssV2, cvssV3, cwe):
        self.cve = cve
        self.cvssV2 = cvssV2
        self.cvssV3 = cvssV3
        self.cwe = cwe

    def __repr__(self):
        return "<cve_data('%s', '%s', '%s', '%s'>" %(self.cve, self.cvssV2, self.cvssV3, self.cwe)