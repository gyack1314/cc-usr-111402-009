"""资料与现有领域接口的核对。"""
import unittest,tempfile,json
from pathlib import Path
from lake.storage import Storage
from lake.temporal import inspect

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
        self.data=json.loads(Path('data/source.json').read_text(encoding='utf-8'))
    def test_existing_reader(self):
        self.assertTrue(inspect(self.data,self.store,self.root))

    def test_packaged_zone_and_partition_error(self):
        from lake.temporal import packaged_zone,utc_text,partition_catalog
        import tzdata
        self.assertEqual(packaged_zone('Europe/Berlin').key,'Europe/Berlin');self.assertEqual(tzdata.__version__,'2025.2')
        self.assertTrue(utc_text(0).startswith('1970-01-01T00:00:00'))
        with self.assertRaises(ValueError):partition_catalog([{'id':'a','start':0,'end':2},{'id':'b','start':1,'end':3}],self.store)
