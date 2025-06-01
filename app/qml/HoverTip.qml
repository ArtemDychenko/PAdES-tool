// HoverTip.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    property alias text: tooltipText.text
    signal hovered()

    Rectangle {
        id: tipBox
        visible: false
        color: "#333"
        radius: 4
        opacity: 0.9
        anchors.bottom: parent.top
        anchors.left: parent.left
        width: tooltipText.paintedWidth + 16
        height: tooltipText.paintedHeight + 10
        z: 999

        Text {
            id: tooltipText
            text: ""
            color: "white"
            font.pixelSize: 12
            anchors.centerIn: parent
        }
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: tipBox.visible = true
        onExited: tipBox.visible = false
    }
}