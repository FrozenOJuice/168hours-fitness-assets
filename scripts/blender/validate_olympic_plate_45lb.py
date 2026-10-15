"""Current A14 validation entry point.

Default: generic origins plus unchanged-geometry/world/render regressions for
all current equipment. -- --origins runs just the origin audit and accepts
--manifest <repository-relative path>. Original0.x full validators are frozen
in docs/audits/origin_baseline; do not overwrite their approval reports.
"""
from pathlib import Path
import sys,runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_asset_origins import main
if __name__=='__main__':
    main()
    if '--origins' not in sys.argv:
        runpy.run_path(str(Path(__file__).with_name('validate_origin_migration.py')),run_name='__main__')

    if '--origins' not in sys.argv:
        runpy.run_path(str(Path(__file__).with_name('validate_origin_compatibility.py')),run_name='__main__')
