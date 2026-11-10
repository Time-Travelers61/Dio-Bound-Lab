#!/usr/bin/env python3
"""PE-ACADEMY-001 P0-B2: offline historical-source and Ollama disk inventory.

Does not use sockets, subprocess, model services, or write model/system files.
A success proves selected bytes/size checks, NOT a currently running Athena,
independent examiner, authority to start Ollama, or admission to P1.
"""
import argparse
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

EXPECTED_MANIFEST = '3b6225ff07117608fdd54a729806671494c57980272eab2b7e7dd2b972423c1c'
EXPECTED_CONFIG = '2dacb491745bc7b2a481550d5b44d5737b0bde4ab1bd8f8d360d33e76a65fd3b'
EXPECTED_RUNNER_BLOB = '071edd94fb40e49f82d4b20fe79df611437b4b3e'
HISTORICAL_PROMPT_SHA256 = 'a9d5d87f065277580f965c8d9c5683b0ffd03eb5aa105a074196dceb1c61a9aa'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_regular(path, max_bytes):
    p = Path(path)
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > max_bytes:
        raise ValueError('NOT_REGULAR_OR_OVERSIZE: ' + p.name)
    # Avoid leaf symlinks. Parent identity/access is NOT continuously attested.
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(p, flags)
    try:
        fs = os.fstat(fd)
        if not stat.S_ISREG(fs.st_mode) or fs.st_size != st.st_size:
            raise ValueError('FILE_CHANGED_DURING_READ: ' + p.name)
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            data = handle.read(max_bytes + 1)
        if len(data) != st.st_size:
            raise ValueError('FILE_CHANGED_DURING_READ: ' + p.name)
        return data
    finally:
        os.close(fd)


def parse_json(data):
    def pairs_no_duplicate(pairs):
        d = {}
        for key, val in pairs:
            if key in d:
                raise ValueError('DUPLICATE_KEY')
            d[key] = val
        return d
    return json.loads(data, object_pairs_hook=pairs_no_duplicate,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('BAD_CONSTANT')))


def valid_descriptor(desc):
    if not isinstance(desc, dict):
        raise ValueError('INVALID_DESCRIPTOR')
    digest = desc.get('digest')
    size = desc.get('size')
    if not isinstance(digest, str) or len(digest) != 71 or not digest.startswith('sha256:'):
        raise ValueError('BAD_DIGEST')
    hx = digest[7:]
    if not all(ch in '0123456789abcdef' for ch in hx):
        raise ValueError('BAD_DIGEST')
    if type(size) is not int or size < 0:
        raise ValueError('BAD_SIZE')
    return hx, size


def check_blob(blobs, descriptor, verify_content=False):
    hx, expected_size = valid_descriptor(descriptor)
    path = blobs / ('sha256-' + hx)
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size != expected_size:
        raise ValueError('MISSING_SYMLINK_OR_SIZE_MISMATCH: '+hx[:16])
    if verify_content:
        data = read_regular(path, 32 * 1024 * 1024)
        if sha256(data) != hx:
            raise ValueError('CONFIG_CONTENT_MISMATCH')
    return expected_size


def historical_system_prompt(runner_path):
    src = read_regular(runner_path, 200_000)
    blob = hashlib.sha1(b'blob ' + str(len(src)).encode() + b'\0' + src).hexdigest()
    if blob != EXPECTED_RUNNER_BLOB:
        raise ValueError('HISTORICAL_RUNNER_BLOB_MISMATCH')
    tree = ast.parse(src.decode('utf-8'))
    matches = [n.value for n in tree.body if isinstance(n, ast.Assign)
               and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
               and n.targets[0].id == 'SYSTEM']
    if len(matches) != 1:
        raise ValueError('HISTORICAL_SYSTEM_UNAVAILABLE')
    value = ast.literal_eval(matches[0])
    if not isinstance(value, str):
        raise ValueError('HISTORICAL_SYSTEM_NOT_LITERAL')
    return {'runner_git_blob_sha1': blob, 'system_prompt_sha256':sha256(value.encode('utf-8')),
            'matches_reported_nov4_system_prompt_hash':
                sha256(value.encode('utf-8')) == HISTORICAL_PROMPT_SHA256}


def inspect(models_root, runner_path):
    root = Path(models_root).expanduser()
    if not root.is_dir() or root.is_symlink():
        raise ValueError('MODEL_ROOT_MISSING_OR_SYMLINK')
    manifest_path = root / 'manifests/registry.ollama.ai/library/qwen3.5/4b'
    raw = read_regular(manifest_path, 2 * 1024 * 1024)
    if sha256(raw) != EXPECTED_MANIFEST:
        raise ValueError('MANIFEST_SHA256_MISMATCH')
    manifest = parse_json(raw)
    config = manifest.get('config')
    layers = manifest.get('layers')
    if not isinstance(layers,list) or len(layers) != 733:
        raise ValueError('UNEXPECTED_LAYER_COUNT')
    blobs = root / 'blobs'
    if not blobs.is_dir() or blobs.is_symlink():
        raise ValueError('BLOB_ROOT_MISSING_OR_SYMLINK')
    config_digest, _ = valid_descriptor(config)
    if config_digest != EXPECTED_CONFIG:
        raise ValueError('CONFIG_DESCRIPTOR_MISMATCH')
    check_blob(blobs, config, verify_content=True)
    seen = {config_digest}
    total = 0
    for item in layers:
        dig, size = valid_descriptor(item)
        seen.add(dig)
        total += check_blob(blobs, item, verify_content=False)
    runner = historical_system_prompt(runner_path)
    return {
        'schema':'PE_ATHENA_OFFLINE_P0B2_V01',
        'status':'LOCAL_DISK_SOURCE_CHECK_ONLY',
        'manifest_sha256':sha256(raw),
        'config_sha256_verified':EXPECTED_CONFIG,
        'layer_count_by_presence_and_size':len(layers),
        'unique_referenced_blobs_including_config':len(seen),
        'layer_bytes_by_declared_size':total,
        'weights_content_all_hashed':False,
        'historical_runner':runner,
        'current_ollama_catalog':'NOT_QUERIED',
        'current_athena_configuration':'UNKNOWN',
        'pilot_execution_authorized':False,
        'pilot_model_calls':0,
        'examiner_admitted':False,
        'official_p1_baseline':'BLOCKED',
        'limitations':['Parent-directory continuous custody not attested',
                       'Layer byte contents not fully rehashed',
                       'Historical source does not prove active model or prompt',
                       'No network, model, or other process examined']
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models-root', required=True,
                        help='Exact pre-authorized Ollama models root; e.g. ~/.ollama/models')
    parser.add_argument('--historical-runner', required=True,
                        help='Exact source-pinned November 4 runner file')
    args=parser.parse_args()
    try:
        result=inspect(args.models_root, args.historical_runner)
        rc=0
    except (ValueError,OSError,SyntaxError,UnicodeDecodeError,TypeError,KeyError,MemoryError) as exc:
        result={'schema':'PE_ATHENA_OFFLINE_P0B2_V01','status':'REFUSED',
                'error_class':type(exc).__name__,
                'current_athena_configuration':'UNKNOWN',
                'pilot_execution_authorized':False,'pilot_model_calls':0,
                'official_p1_baseline':'BLOCKED'}
        rc=2
    print(json.dumps(result,sort_keys=True,indent=2))
    return rc


if __name__=='__main__':
    raise SystemExit(main())
