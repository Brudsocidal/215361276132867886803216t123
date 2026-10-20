import os
import requests
from PySide6.QtCore import QObject, Signal, Slot, Property
from modules import gta_module, valorant_module, roblox_module

DEFAULT_API = os.environ.get("VNDELAY_API_URL", "http://127.0.0.1:5000").rstrip("/")

class Backend(QObject):
    userChanged = Signal()
    statusChanged = Signal()
    messageChanged = Signal()
    gameChanged = Signal()
    adminChanged = Signal()

    def __init__(self):
        super().__init__()
        self._username = ""
        self._role = "user"
        self._token = ""
        self._status = "Chưa đăng nhập"
        self._message = ""
        self._game = "gta"
        self._api = DEFAULT_API

    @Property(str, notify=userChanged)
    def username(self): return self._username

    @Property(str, notify=statusChanged)
    def status(self): return self._status

    @Property(str, notify=messageChanged)
    def message(self): return self._message

    @Property(str, notify=gameChanged)
    def currentGame(self): return self._game

    @Property(bool, notify=adminChanged)
    def isAdmin(self): return self._role == "admin"

    def _request(self, method, path, **kwargs):
        try:
            r = requests.request(method, self._api + path, timeout=(8, 45), **kwargs)
            data = r.json() if r.content else {}
            if not r.ok:
                return False, data.get("error", "Yêu cầu không thành công.")
            return True, data
        except requests.Timeout:
            return False, "Máy chủ phản hồi chậm hoặc đang khởi động. Hãy thử lại."
        except (requests.RequestException, ValueError):
            return False, "Không thể kết nối máy chủ. Hãy kiểm tra mạng và địa chỉ API."

    @Slot(str, str)
    def login(self, username, password):
        self._status = "Đang kết nối máy chủ..."
        self.statusChanged.emit()
        ok, data = self._request("POST", "/api/login", json={"username": username, "password": password})
        if not ok:
            self._message = data if isinstance(data, str) else data.get("error", "Đăng nhập thất bại.")
            self.messageChanged.emit(); return
        self._username = username
        self._role = data.get("role", "user")
        self._token = data.get("token", "")
        self._status = "Đã đăng nhập"
        self.userChanged.emit(); self.statusChanged.emit(); self.adminChanged.emit()
        self._message = "Đăng nhập thành công."
        self.messageChanged.emit()

    @Slot()
    def logout(self):
        self._username, self._role, self._token = "", "user", ""
        self.userChanged.emit(); self.adminChanged.emit()
        self._message = "Đã đăng xuất."; self.messageChanged.emit()

    @Slot(str)
    def openGame(self, game_id):
        ok, data = self._request("GET", f"/api/game/{game_id}/status")
        if not ok:
            self._message = data if isinstance(data, str) else "Không kiểm tra được trạng thái game."
            self.messageChanged.emit(); return
        if not data.get("released", False):
            self._message = "Tính năng đang phát triển, sắp ra mắt."
            self.messageChanged.emit(); return
        self._game = game_id
        self.gameChanged.emit()
        self._message = "Module đã mở. Hook tối ưu hiện để trống theo yêu cầu."
        self.messageChanged.emit()

    @Slot()
    def runOptimization(self):
        {"gta": gta_module, "valorant": valorant_module, "roblox": roblox_module}.get(self._game, gta_module).run_optimization()
        self._message = "Hook run_optimization() đã được gọi; hiện chưa có logic."
        self.messageChanged.emit()

    @Slot()
    def stopOptimization(self):
        {"gta": gta_module, "valorant": valorant_module, "roblox": roblox_module}.get(self._game, gta_module).stop_optimization()
        self._message = "Hook stop_optimization() đã được gọi; hiện chưa có logic."
        self.messageChanged.emit()

    @Slot()
    def exitModule(self):
        self._game = ""
        self.gameChanged.emit()

    @Slot(str)
    def sendBroadcast(self, message):
        ok, data = self._request("POST", "/api/broadcast", json={"message": message},
                                 headers={"Authorization": "Bearer " + self._token})
        self._message = "Đã gửi thông báo." if ok else (data if isinstance(data, str) else "Không gửi được thông báo.")
        self.messageChanged.emit()

    @Slot(str, bool)
    def setGameReleased(self, game_id, released):
        ok, data = self._request("POST", f"/api/game/{game_id}/release", json={"released": released},
                                 headers={"Authorization": "Bearer " + self._token})
        self._message = "Đã cập nhật trạng thái game." if ok else (data if isinstance(data, str) else "Không cập nhật được.")
        self.messageChanged.emit()

    @Slot(str, str, str, str)
    def updateVersion(self, version, download_url, checksum, notes):
        body = {"version": version, "download_url": download_url, "checksum": checksum, "release_notes": notes}
        ok, data = self._request("POST", "/api/version/update", json=body,
                                 headers={"Authorization": "Bearer " + self._token})
        self._message = "Đã cập nhật metadata phiên bản." if ok else (data if isinstance(data, str) else "Không cập nhật được.")
        self.messageChanged.emit()
