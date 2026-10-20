import QtQuick
import QtQuick.Controls

Button {
    id: control
    property color glowColor: "#f4d35e"
    implicitHeight: 48
    contentItem: Text { text: control.text; color: "#111522"; font.bold: true; font.pixelSize: 14; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
    background: Rectangle {
        radius: 12
        color: control.down ? Qt.darker(control.glowColor, 1.15) : control.hovered ? Qt.lighter(control.glowColor, 1.08) : control.glowColor
        border.color: "#fff0b2"; border.width: 1
        Behavior on color { ColorAnimation { duration: 140 } }
    }
}
