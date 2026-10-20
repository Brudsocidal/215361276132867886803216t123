import QtQuick

Item {
    // Shader/mesh chưa được xác minh trên mọi GPU/Qt build.
    // Nếu có file GIF do người dùng cung cấp, dùng fallback này.
    Image {
        id: flag
        anchors.fill: parent
        source: "../../assets/flag_vn_wave.gif"
        fillMode: Image.PreserveAspectFit
        visible: status === Image.Ready
        cache: true
    }
    Rectangle {
        anchors.fill: parent; radius: 5; color: "#cf2738"; visible: parent.children.length > 0 && flag.status !== Image.Ready
        Image { id: star; anchors.centerIn: parent; width: parent.width * 0.35; height: width; source: "../../assets/flag_vn_texture.png"; fillMode: Image.PreserveAspectFit; visible: status === Image.Ready }
        Text { anchors.centerIn: parent; text: "★"; color: "#ffdf59"; font.pixelSize: Math.min(parent.width, parent.height) * 0.52; visible: star.status !== Image.Ready }
    }
    // id attached via separate property alias is avoided; shader requires a later GPU test.
    property bool shaderNeedsTest: true
}
