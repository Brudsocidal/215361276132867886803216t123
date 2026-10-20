import json, sys
from app import password_hash
if len(sys.argv) != 4 or sys.argv[3] not in ("user", "admin"):
    print('Usage: python create_user.py USERNAME "PASSWORD" user|admin')
    raise SystemExit(2)
print(json.dumps({"username": sys.argv[1], "password_hash": password_hash(sys.argv[2]), "role": sys.argv[3]}, ensure_ascii=False, indent=2))
