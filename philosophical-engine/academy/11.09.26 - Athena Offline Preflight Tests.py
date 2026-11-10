#!/usr/bin/env python3
"""Disposable fixture tests for Athena P0-B2 preflight. Never contact Ollama."""
import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

TARGET=Path(__file__).with_name('11.09.26 - Athena Offline Preflight v0.1.py')
spec=importlib.util.spec_from_file_location('athena_offline_p0b2',TARGET)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def dig(b):return hashlib.sha256(b).hexdigest()


class OfflineFixture(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'models'
        self.blobs=self.root/'blobs'
        self.blobs.mkdir(parents=True)
        self.mpath=self.root/'manifests/registry.ollama.ai/library/qwen3.5/4b'
        self.mpath.parent.mkdir(parents=True)
        self.runner=Path(self.tmp.name)/'historical.py'
        content=b'SYSTEM=("Synthetic Athena classroom prompt. " "No real permissions.")\n'
        self.runner.write_bytes(content)
        self.config=b'{"modelfile":"synthetic only"}'
        self.cdig=dig(self.config)
        (self.blobs/('sha256-'+self.cdig)).write_bytes(self.config)
        self.layers=[]
        # Same cardinality as actual reported model manifest, tiny fake payloads.
        for i in range(733):
            raw=f'synthetic-{i}'.encode()
            h=dig(raw)
            (self.blobs/('sha256-'+h)).write_bytes(raw)
            self.layers.append({'digest':'sha256:'+h,'size':len(raw),'mediaType':'application/octet-stream'})
        self.m={'schemaVersion':2,'config':{'digest':'sha256:'+self.cdig,'size':len(self.config)},'layers':self.layers}
        self.write_manifest()
        self.save=(mod.EXPECTED_MANIFEST,mod.EXPECTED_CONFIG,mod.EXPECTED_RUNNER_BLOB,mod.HISTORICAL_PROMPT_SHA256)
        mod.EXPECTED_MANIFEST=dig(self.mpath.read_bytes())
        mod.EXPECTED_CONFIG=self.cdig
        mod.EXPECTED_RUNNER_BLOB=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        mod.HISTORICAL_PROMPT_SHA256=dig(b'Synthetic Athena classroom prompt. No real permissions.')
        self.addCleanup(self.restore)

    def restore(self):
        (mod.EXPECTED_MANIFEST,mod.EXPECTED_CONFIG,mod.EXPECTED_RUNNER_BLOB,mod.HISTORICAL_PROMPT_SHA256)=self.save

    def write_manifest(self):
        self.mpath.write_text(json.dumps(self.m,sort_keys=True),encoding='utf-8')

    def check_bad(self, expected):
        with self.assertRaisesRegex((ValueError, OSError), expected):
            mod.inspect(self.root,self.runner)

    def test_positive_has_no_execution_claim(self):
        x=mod.inspect(self.root,self.runner)
        self.assertEqual(x['layer_count_by_presence_and_size'],733)
        self.assertTrue(x['historical_runner']['matches_reported_nov4_system_prompt_hash'])
        self.assertEqual(x['current_athena_configuration'],'UNKNOWN')
        self.assertFalse(x['pilot_execution_authorized'])
        self.assertEqual(x['pilot_model_calls'],0)
        self.assertEqual(x['official_p1_baseline'],'BLOCKED')
        self.assertFalse(x['weights_content_all_hashed'])

    def test_manifest_pin_refusal(self):
        self.m['schemaVersion']=3
        self.write_manifest()
        self.check_bad('MANIFEST_SHA256_MISMATCH')

    def test_config_hash_refusal(self):
        (self.blobs/('sha256-'+self.cdig)).write_bytes(b'!'*len(self.config))
        self.check_bad('CONFIG_CONTENT_MISMATCH')

    def test_missing_layer(self):
        h=self.layers[27]['digest'][7:]
        (self.blobs/('sha256-'+h)).unlink()
        self.assertRaises(FileNotFoundError,mod.inspect,self.root,self.runner)

    def test_layer_wrong_size(self):
        h=self.layers[27]['digest'][7:]
        (self.blobs/('sha256-'+h)).write_bytes(b'X')
        self.check_bad('MISSING_SYMLINK_OR_SIZE_MISMATCH')

    def test_symlink_layer(self):
        h=self.layers[27]['digest'][7:]
        target=self.blobs/('sha256-'+h)
        target.unlink()
        target.symlink_to(self.blobs/('sha256-'+self.cdig))
        self.check_bad('MISSING_SYMLINK_OR_SIZE_MISMATCH')

    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE_KEY'):
            mod.parse_json(b'{"x":1,"x":2}')

    def test_nan_not_allowed(self):
        with self.assertRaisesRegex(ValueError,'BAD_CONSTANT'):
            mod.parse_json(b'{"x":NaN}')

    def test_model_root_symlink(self):
        alt=Path(self.tmp.name)/'alternate'
        alt.symlink_to(self.root, target_is_directory=True)
        self.assertRaisesRegex(ValueError,'MODEL_ROOT_MISSING_OR_SYMLINK',mod.inspect,alt,self.runner)

    def test_runner_blob_changed(self):
        self.runner.write_text('SYSTEM="forged"\n')
        self.check_bad('HISTORICAL_RUNNER_BLOB_MISMATCH')

    def test_prompt_mismatch_does_not_prove_live_state(self):
        mod.HISTORICAL_PROMPT_SHA256='0'*64
        x=mod.inspect(self.root,self.runner)
        self.assertFalse(x['historical_runner']['matches_reported_nov4_system_prompt_hash'])
        self.assertEqual(x['official_p1_baseline'],'BLOCKED')

    def test_nonliteral_prompt_rejected(self):
        content=b'SYSTEM=some_runtime_function()\n'
        self.runner.write_bytes(content)
        mod.EXPECTED_RUNNER_BLOB=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        self.check_bad('malformed node or string')

    def test_bad_descriptor(self):
        self.assertRaisesRegex(ValueError,'BAD_DIGEST',mod.valid_descriptor,{'digest':'sha256:../etc','size':0})

    def test_bad_size_bool(self):
        self.assertRaisesRegex(ValueError,'BAD_SIZE',mod.valid_descriptor,{'digest':'sha256:'+'a'*64,'size':True})


if __name__=='__main__':unittest.main(verbosity=2)
