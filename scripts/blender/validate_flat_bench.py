"""Validate the current bench origin contract and authorized visual revision.

Default: this bench's origin report plus saved geometry, palette, bracket/cap
fit and linked support checks. -- --origins selects only the origin audit.
Historical A14 proofs stay pinned to their retained revisions; they are checked
separately by validate_origin_migration.py without redefining shared standards.
"""
from pathlib import Path
import sys,runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_asset_origins import main
if __name__=='__main__':
    # A bench revision owns its evidence; preserve completed library audit snapshots.
    if '--' not in sys.argv:sys.argv.append('--')
    if '--manifest' not in sys.argv:
        from build_flat_bench import ASSET,REPO
        sys.argv.extend(['--manifest',str((ASSET/'asset.json').relative_to(REPO))])
    main()
    if '--origins' not in sys.argv:
        runpy.run_path(str(Path(__file__).with_name('validate_flat_bench_visual.py')),run_name='__main__')
