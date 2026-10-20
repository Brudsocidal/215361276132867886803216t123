import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: card
    property string title: "Game"
    property string subtitle: ""
    property color accent: "#f4d35e"
    property bool comingSoon: false
    signal play()
    radius: 18; color: "#20283b"; border.color: hovered ? accent : "#3b4664"; border.width: hovered ? 2 : 1
    property bool hovered: false
    Behavior on border.color { ColorAnimation { duration: 160 } }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 18; spacing: 12
        Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 130; radius: 12; color: "#151b2b"; border.color: "#3b4664"
            Label { anchors.centerIn: parent; text: card.title.split(" ")[0]; color: card.accent; font.pixelSize: 34; font.bold: true }
        }
        Label { text: card.title; color: "white"; font.pixelSize: 19; font.bold: true; wrapMode: Text.WordWrap }
        Label { text: card.subtitle; color: "#aab5d0"; Layout.fillWidth: true; wrapMode: Text.WordWrap }
        Item { Layout.fillHeight: true }
        Button { Layout.fillWidth: true; text: card.comingSoon ? "Sắp ra mắt" : "Chơi"; enabled: !card.comingSoon; onClicked: card.play() }
    }
    MouseArea { anchors.fill: parent; hoverEnabled: true; onEntered: card.hovered = true; onExited: card.hovered = false; z: -1 }
}
