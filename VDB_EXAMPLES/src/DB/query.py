from . import database
from . import models

def add_progress_queue(cve, commit, crawlType, vendor, product):
    t = models.progress_queue(cve, commit, crawlType, vendor, product)
    database.db_session.add(t)

def get_progress_queue():
    queue = []   
    for progress_queue in database.db_session.query(models.progress_queue).all():
        queue.append({'cve': progress_queue.cve,\
        'commit': progress_queue.commit,\
        'crawlType': progress_queue.crawlType,\
        'vendor':progress_queue.vendor,\
        'product':progress_queue.product\
        })
    return queue

def clear_progress_queue():
    #t = models.progress_queue(cve, commit, crawlType, vendor, product)
    #database.db_session.delete(t)
    print(database.db_session.query(models.progress_queue).delete())


def del_progress_queue(cve, crawlType):
    t = models.progress_queue(cve, commit, crawlType, vendor, product)
    database.db_session.delete(t)


def get_urls_from_cve(cve):
    urls = []
    for query in database.db_session.query(models.cve_url).\
    filter(models.cve_url.cve==cve).all():
        urls.append(query.url)
    return urls


def show_cve_cpe():
    queries = database.db_session.query(models.cve_cpe)
    entries = [dict(vendor = q.vendor, product = q.product, version = q.version, cve = q.cve) for q in queries]
    print(entries)


def show_cve_url():
    queries = database.db_session.query(models.cve_url)
    entries = [dict(cve = q.cve, name = q.name, refsource = q.refsource, tags = q.tags) for q in queries]
    print(entries)


# add entry to cve_cpe
def update_cve_cpe(vendor, product, version, cve):
    item = database.db_session.query(models.cve_cpe).filter_by(vendor=vendor, product=product, cve=cve).first()

    if item == None:
        t = models.cve_cpe(vendor, product, version, cve)
        database.db_session.add(t)    
    else:
        item.version = version
    

# add entry to cve_url
def update_cve_url(cve, url, name, refsource, tags):
    item = database.db_session.query(models.cve_url).filter_by(cve=cve, url=url).first()

    if item == None:
        t = models.cve_url(cve, url, name, refsource, tags)
        database.db_session.add(t)
    else:
        item.name       = name
        item.refsource  = refsource
        item.tags       = tags


# add entry to cve_data
def update_cve_data(cve, cvssV2, cvssV3, cwe):
    item = database.db_session.query(models.cve_data).filter_by(cve=cve).first()

    if item == None:
        t = models.cve_data(cve, cvssV2, cvssV3, cwe)
        database.db_session.add(t)
    else:
        item.cvssV2     = cvssV2
        item.cvssV3     = cvssV3
        item.cwe        = cwe


def add_cve_cpe(vendor, product, version, cve):
    t = models.cve_cpe(vendor, product, version, cve)
    database.db_session.add(t)    


# add entry to cve_url
def add_cve_url(cve, url, name, refsource, tags):
    t = models.cve_url(cve, url, name, refsource, tags)
    database.db_session.add(t)


# add entry to cve_data
def add_cve_data(cve, cvssV2, cvssV3, cwe):
    t = models.cve_data(cve, cvssV2, cvssV3, cwe)
    database.db_session.add(t)


# get cve with vendor product information
def get_cves_from_vp(vendor, product):
    cves = []
    for cve_cpe in database.db_session.query(models.cve_cpe).filter_by(vendor=vendor, product=product).all():
        cves.append(cve_cpe.cve)
    return cves


def get_url_from_cve(cve):
    urls =[]
    for cve_url in database.db_session.query(models.cve_url).filter_by(cve = cve).all():
        urls.append(cve_url.url)
    return urls


def get_all_urls():
    urls = []
    for row in database.db_session.query(models.cve_url).all():
        urls.append([row.cve, row.url])
    return urls


def get_urls_from_vp(vendor, product):
    urls = []
    for row in database.db_session.query(models.cve_cpe.vendor, models.cve_cpe.product, \
    models.cve_cpe.cve, models.cve_url.url).filter_by(vendor=vendor, product=product)\
    .join(models.cve_url, models.cve_cpe.cve == models.cve_url.cve).all():
        urls.append([row.cve,row.url])
    return urls


def get_urls_from_vendor(vendor):
    urls = []
    for row in database.db_session.query(models.cve_cpe.vendor, models.cve_cpe.product, models.cve_cpe.cve, models.cve_url.url).filter_by(vendor=vendor).join(models.cve_url, models.cve_cpe.cve == models.cve_url.cve).all():
        urls.append([row.cve, row.url])
    return urls


def session_commit():
    database.db_session.commit()


def get_versions_from_vpc(vendor, product, cve):
    versionInfo = ''
    try:
        versionInfo = database.db_session.query(models.cve_cpe).filter_by(vendor=vendor, product=product, cve=cve).one().version
    except :
        pass
    return versionInfo

def get_data_from_cve(cve):
    data = []
    try :
        row = database.db_session.query(models.cve_data).filter_by(cve=cve).one()
        data.append(row.cvssV2)
        cwes = row.cwe.split(':')
        data.append(cwes[0])
    except:
        print("[-] Query Error", cve)
        data = ['0', 'CWE-999']
    return data


def drop_all_table():
    database.drop_tables()

def mozilla_query():
    data = []
    try :
        for row in database.db_session.query(models.cve_url).filter(models.cve_url.url.like("%bugzilla.mozilla.org/show_bug.cgi?id=%")).all():
            data.append([row.cve, row.url])
    except Exception as e:
        print(e)
        print("[-] Mozilla_Query Error")
        data = []
    return data
