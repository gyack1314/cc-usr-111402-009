"""UTC整秒时间和冻结分区的已有读取。"""
from datetime import datetime,timezone
import tzdata
import os,importlib.resources
from zoneinfo import ZoneInfo,reset_tzpath

def packaged_zone(name):
    path=importlib.resources.files('tzdata').joinpath('zoneinfo')
    reset_tzpath([str(path)])
    return ZoneInfo.no_cache(name)

def utc_text(instant):
    if type(instant) is not int:raise ValueError('绝对时刻不是整数秒')
    return datetime.fromtimestamp(instant,timezone.utc).isoformat()

def partition_catalog(partitions,storage):
    last=None;ids=set()
    for p in sorted(partitions,key=lambda r:r['start']):
        if p['id'] in ids or p['start']>=p['end']:raise ValueError('分区非法')
        if last is not None and p['start']<last:raise ValueError('UTC分区重叠')
        ids.add(p['id']);last=p['end']
    return storage.write({'tzdb_version':tzdata.__version__,'partitions':partitions})

def inspect(data,storage,root):
    head=partition_catalog(data['partitions'],storage);zone=packaged_zone('Europe/Berlin')
    return {'catalog':head,'tzdb_version':tzdata.__version__,'zone':zone.key,'rows':[{'row_id':r['row_id'],'utc':utc_text(r['instant'])} for r in data['rows']]}
