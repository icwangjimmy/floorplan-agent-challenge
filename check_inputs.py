"""Read-only standard-library check; no API calls or network."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
path = root / "input/kenney-140-input-v1.zip"
expected = "c8f1488d2d2486234d2e8ab8af992ad4402df3c95cfa4f197cc907170b7a2c82"
assert path.is_file(), "Missing furniture ZIP"
assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, "ZIP hash mismatch"
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None, "Damaged ZIP"
    names = z.namelist()
    assert sum(n.endswith('.glb') for n in names) == 140
    assert sum(n.endswith('.png') for n in names) == 140
    assert len(json.loads(z.read('catalog.json'))['assets']) == 140
print("PASS: asset hash, 140 GLBs, 140 thumbnails, 140 catalogue entries")
plans = [p for p in (root / 'input').glob('floorplan.*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg')]
if len(plans) != 1:
    print("ACTION: add exactly one floorplan.png (or JPG/JPEG; update TASK and prompt paths)")
    raise SystemExit(2)
p = plans[0]
magic = p.read_bytes()[:8]
assert (p.suffix.lower() == '.png' and magic == b'\x89PNG\r\n\x1a\n') or (p.suffix.lower() in ('.jpg','.jpeg') and magic[:3] == b'\xff\xd8\xff'), "Image extension/signature mismatch"
task = (root / 'TASK.md').read_text(encoding='utf-8-sig')
assert f'input/{p.name}' in task, "Update the image path in TASK.md and the prompt"
print("PASS: floorplan present with matching signature and task path; view it before running")
