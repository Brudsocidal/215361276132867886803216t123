import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

ApplicationWindow {
    id: win
    width: 1080; height: 720; minimumWidth: 900; minimumHeight: 620
    visible: true
    title: "VN DELAY"
    color: "#10131f"
    property bool loggedIn: backend.username.length > 0
    property bool showAdmin: false
    property bool moduleMode: backend.currentGame.length > 0

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#182239" }
            GradientStop { position: 0.55; color: "#10131f" }
            GradientStop { position: 1.0; color: "#29151f" }
        }
    }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 24; spacing: 18
        RowLayout {
            Layout.fillWidth: true
            ColumnLayout {
                spacing: 0
                Label { text: "VN DELAY"; color: "#fff2d0"; font.pixelSize: 30; font.bold: true }
                Label { text: "DELAY DAME FREE  •  CLIENT"; color: "#9ca8c8"; font.pixelSize: 12 }
            }
            Item { Layout.fillWidth: true }
            Flag3D { Layout.preferredWidth: 96; Layout.preferredHeight: 60 }
            Label { visible: loggedIn; text: backend.username; color: "#f7d66d"; font.bold: true }
            Button { visible: loggedIn; text: "Đăng xuất"; onClicked: { backend.logout(); backend.exitModule(); showAdmin = false } }
        }
        Rectangle { Layout.fillWidth: true; height: 1; color: "#38415c" }

        StackView {
            id: stack
            Layout.fillWidth: true; Layout.fillHeight: true
            initialItem: loginPage
            replaceEnter: Transition { NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 180 } }
            replaceExit: Transition { NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 120 } }
        }

        Rectangle {
            Layout.fillWidth: true; Layout.preferredHeight: 42; radius: 10
            color: "#20283b"; border.color: "#3d4968"
            Label { anchors.fill: parent; anchors.margins: 10; verticalAlignment: Text.AlignVCenter; text: backend.message || backend.status; color: "#d5def5"; elide: Text.ElideRight }
        }
    }

    Component {
        id: loginPage
        Item {
            ColumnLayout {
                anchors.centerIn: parent; width: Math.min(parent.width * 0.72, 440); spacing: 16
                Label { text: "Chào mừng trở lại"; color: "white"; font.pixelSize: 28; font.bold: true }
                Label { text: "Đăng nhập bằng tài khoản trong whitelist."; color: "#aab5d0"; wrapMode: Text.WordWrap }
                TextField { id: username; Layout.fillWidth: true; placeholderText: "Username"; selectByMouse: true }
                TextField { id: password; Layout.fillWidth: true; placeholderText: "Password"; echoMode: TextInput.Password; selectByMouse: true; onAccepted: loginButton.clicked() }
                NeonButton { id: loginButton; Layout.fillWidth: true; text: "ĐĂNG NHẬP"; onClicked: { backend.login(username.text, password.text); loginTimer.start() } }
                Timer { id: loginTimer; interval: 350; onTriggered: if (backend.username.length > 0) stack.replace(gamePage) }
                Label { text: "Máy chủ có thể cần 30–60 giây để khởi động lần đầu."; color: "#7e8aa8"; wrapMode: Text.WordWrap }
            }
        }
    }
    Component {
        id: gamePage
        Item {
            ColumnLayout {
                anchors.fill: parent; spacing: 16
                RowLayout {
                    Layout.fillWidth: true
                    Label { text: "Thư viện game"; color: "white"; font.pixelSize: 25; font.bold: true }
                    Item { Layout.fillWidth: true }
                    Button { visible: backend.isAdmin; text: "Admin Panel"; onClicked: stack.push(adminPage) }
                }
                GridLayout {
                    Layout.fillWidth: true; Layout.fillHeight: true
                    columns: width > 700 ? 3 : 1; rowSpacing: 14; columnSpacing: 14
                    GameCard { Layout.fillWidth: true; Layout.fillHeight: true; title: "GTA V / FiveM"; subtitle: "Available • Module khung"; accent: "#f4d35e"; onPlay: { backend.openGame("gta"); moduleTimer.start() } }
                    GameCard { Layout.fillWidth: true; Layout.fillHeight: true; title: "VALORANT"; subtitle: "Coming Soon"; accent: "#ff667a"; comingSoon: true }
                    GameCard { Layout.fillWidth: true; Layout.fillHeight: true; title: "ROBLOX"; subtitle: "Coming Soon"; accent: "#69c9ff"; comingSoon: true }
                }
                Timer { id: moduleTimer; interval: 300; onTriggered: if (backend.currentGame.length > 0) stack.push(modulePage) }
            }
        }
    }
    Component {
        id: modulePage
        Item {
            ColumnLayout {
                anchors.centerIn: parent; width: Math.min(parent.width * 0.8, 560); spacing: 18
                Label { text: backend.currentGame === "gta" ? "GTA V / FiveM" : backend.currentGame.toUpperCase(); color: "white"; font.pixelSize: 28; font.bold: true }
                Label { text: "Module view trong cùng cửa sổ launcher. Logic tối ưu chưa được cài."; color: "#aab5d0"; wrapMode: Text.WordWrap }
                RowLayout {
                    Layout.fillWidth: true
                    NeonButton { text: "Chạy hook"; onClicked: backend.runOptimization() }
                    Button { text: "Dừng hook"; onClicked: backend.stopOptimization() }
                    Button { text: "Exit"; onClicked: { backend.stopOptimization(); backend.exitModule(); stack.pop() } }
                }
            }
        }
    }
    Component {
        id: adminPage
        Flickable {
            contentWidth: width; contentHeight: adminColumn.implicitHeight
            ColumnLayout {
                id: adminColumn; width: parent.width; spacing: 14
                Label { text: "Admin Panel"; color: "white"; font.pixelSize: 26; font.bold: true }
                Label { text: "Broadcast toàn server"; color: "#f4d35e"; font.pixelSize: 16 }
                TextField { id: broadcastText; Layout.fillWidth: true; placeholderText: "Nội dung thông báo" }
                Button { text: "Gửi thông báo"; onClicked: backend.sendBroadcast(broadcastText.text) }
                Label { text: "Trạng thái game"; color: "#f4d35e"; font.pixelSize: 16 }
                RowLayout {
                    Button { text: "GTA Available"; onClicked: backend.setGameReleased("gta", true) }
                    Button { text: "GTA Coming Soon"; onClicked: backend.setGameReleased("gta", false) }
                    Button { text: "Valorant Available"; onClicked: backend.setGameReleased("valorant", true) }
                    Button { text: "Roblox Available"; onClicked: backend.setGameReleased("roblox", true) }
                }
                Label { text: "Cập nhật metadata (chỉ URL GitHub Releases; không upload EXE lên Render)"; color: "#f4d35e"; wrapMode: Text.WordWrap }
                TextField { id: ver; Layout.fillWidth: true; placeholderText: "Version, ví dụ 1.1.0" }
                TextField { id: url; Layout.fillWidth: true; placeholderText: "URL GitHub Release asset" }
                TextField { id: sha; Layout.fillWidth: true; placeholderText: "SHA256 (tùy chọn)" }
                TextField { id: notes; Layout.fillWidth: true; placeholderText: "Release notes" }
                Button { text: "Cập nhật version.json"; onClicked: backend.updateVersion(ver.text, url.text, sha.text, notes.text) }
                Button { text: "Quay lại"; onClicked: stack.pop() }
            }
        }
    }
}
