import hashlib, hmac, json, os, secrets, time
from functools import wraps
from pathlib import Path
from flask import Flask, jsonify, request, g
from flask_cors import CORS

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.environ.get(
    "VNDELAY_SECRET_KEY", "DEV-ONLY-change-this-secret"
)


# --- THÊM ROUTE TRANG CHỦ ĐỂ KHẮC PHỤC LỖI 404 ---
@app.get("/")
def index():
  return jsonify(
      status="ok",
      service="VN DELAY API",
      message="Server đang hoạt động bình thường trên Render!",
      endpoints=[
          "/api/health",
          "/api/login",
          "/api/version",
          "/api/broadcast",
      ],
  )


def read_json(name, fallback):
  try:
    with (BASE / name).open("r", encoding="utf-8") as f:
      return json.load(f)
  except (OSError, ValueError):
    return fallback


def write_json(name, data):
  target = BASE / name
  tmp = target.with_suffix(target.suffix + ".tmp")
  with tmp.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
  os.replace(tmp, target)


def password_hash(password, salt=None):
  salt = salt or secrets.token_hex(16)
  digest = hashlib.pbkdf2_hmac(
      "sha256", password.encode(), salt.encode(), 310000
  ).hex()
  return f"pbkdf2_sha256$310000${salt}${digest}"


def verify_password(password, encoded):
  try:
    scheme, rounds, salt, expected = encoded.split("$", 3)
    if scheme != "pbkdf2_sha256":
      return False
    got = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), int(rounds)
    ).hex()
    return hmac.compare_digest(got, expected)
  except (ValueError, TypeError):
    return False


# In-memory sessions are deliberately simple for this scaffold; restart invalidates tokens.
SESSIONS = {}


def bearer_admin(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    token = (
        request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    )
    session = SESSIONS.get(token)
    if not session or session.get("role") != "admin":
      return jsonify(error="Yêu cầu quyền admin."), 403
    g.session = session
    return fn(*args, **kwargs)

  return wrapper


@app.get("/api/health")
def health():
  return jsonify(status="ok", service="VN DELAY API")


@app.post("/api/login")
def login():
  body = request.get_json(silent=True) or {}
  username, password = body.get("username", ""), body.get("password", "")
  if (
      not isinstance(username, str)
      or not isinstance(password, str)
      or not username
      or not password
  ):
    return jsonify(error="Vui lòng nhập username và password."), 400
  users = read_json("whitelist.json", [])
  for user in users:
    if user.get("username") == username and verify_password(
        password, user.get("password_hash", "")
    ):
      token = secrets.token_urlsafe(32)
      SESSIONS[token] = {
          "username": username,
          "role": user.get("role", "user"),
          "created": time.time(),
      }
      return jsonify(status="ok", token=token, role=SESSIONS[token]["role"])
  return jsonify(
      error="Tài khoản không có trong whitelist hoặc mật khẩu không đúng."
  ), 401


@app.get("/api/version")
def version():
  data = read_json("version.json", {})
  return jsonify(
      latest_version=data.get("latest_version", "1.0.0"),
      download_url=data.get("download_url", ""),
      checksum=data.get("checksum", ""),
      release_notes=data.get("release_notes", ""),
  )


@app.post("/api/version/update")
@bearer_admin
def update_version():
  body = request.get_json(silent=True) or {}
  version = body.get("version", "")
  url = body.get("download_url", "")
  if not version or not isinstance(url, str) or (url and not url.startswith("https://")):
    return jsonify(error="Version bắt buộc; URL phải là HTTPS."), 400
  data = {
      "latest_version": str(version),
      "download_url": url,
      "checksum": str(body.get("checksum", "")),
      "release_notes": str(body.get("release_notes", "")),
  }
  write_json("version.json", data)
  return jsonify(status="ok", version=version)


@app.get("/api/broadcast")
def get_broadcast():
  return jsonify(
      read_json("broadcast.json", {"id": 0, "message": "", "timestamp": 0})
  )


@app.post("/api/broadcast")
@bearer_admin
def post_broadcast():
  body = request.get_json(silent=True) or {}
  message = body.get("message", "")
  if not isinstance(message, str) or not message.strip():
    return jsonify(error="Thông báo không được để trống."), 400
  current = read_json("broadcast.json", {"id": 0})
  data = {
      "id": int(current.get("id", 0)) + 1,
      "message": message.strip()[:1000],
      "timestamp": int(time.time()),
  }
  write_json("broadcast.json", data)
  return jsonify(status="ok", broadcast=data)


@app.get("/api/game/<game_id>/status")
def game_status(game_id):
  games = read_json("games.json", {})
  if game_id not in games:
    return jsonify(error="Game không tồn tại."), 404
  return jsonify(
      released=bool(games[game_id].get("released", False)),
      module_name=games[game_id].get("module_name", game_id + "_module"),
  )


@app.post("/api/game/<game_id>/release")
@bearer_admin
def set_release(game_id):
  games = read_json("games.json", {})
  if game_id not in games:
    return jsonify(error="Game không tồn tại."), 404
  body = request.get_json(silent=True) or {}
  released = body.get("released")
  if not isinstance(released, bool):
    return jsonify(error="released phải là true/false."), 400
  games[game_id]["released"] = released
  write_json("games.json", games)
  return jsonify(status="ok", game=game_id, released=released)


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
