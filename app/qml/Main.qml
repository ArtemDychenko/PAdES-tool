import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 500
    height: 600
    title: "PDF Sign & Verify"
    Material.theme: Material.Light
    Material.accent: Material.Teal

    signal selectPdf()
    signal selectPublicKey()
    signal signPdf()
    signal verifyPdf()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 16

        Label {
            text: "PDF Signature Manager"
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        ComboBox {
            id: usbComboBox
            Layout.fillWidth: true
            model: ["Select USB device", "USB Device 1", "USB Device 2"]
            currentIndex: 0
        }

        Button {
            text: "Select PDF File"
            Layout.fillWidth: true
            onClicked: selectPdf()
        }

        Label {
            id: selectedPdfLabel
            text: "No PDF file selected"
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }

        Button {
            text: "Select Verification Key"
            Layout.fillWidth: true
            onClicked: selectPublicKey()
        }

        Label {
            id: selectedKeyLabel
            text: "No key selected"
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            // SIGN PDF BUTTON WITH TOOLTIP
            Item {
                Layout.fillWidth: true
                Layout.preferredWidth: 1  // Makes both buttons take equal width
                height: signButton.implicitHeight

                Button {
                    id: signButton
                    text: "Sign PDF"
                    anchors.fill: parent
                    enabled: usbComboBox.currentIndex > 0 &&
                            selectedPdfLabel.text !== "No PDF file selected"
                    Material.background: Material.Teal
                    Material.foreground: "white"
                    onClicked: signPdf()
                }

                ToolTip.visible: !signButton.enabled && signTipArea.containsMouse
                ToolTip.text: usbComboBox.currentIndex === 0
                            ? "Select a USB device to enable signing"
                            : "Select a PDF file to enable signing"

                MouseArea {
                    id: signTipArea
                    anchors.fill: parent
                    hoverEnabled: true
                }
            }

            // VERIFY SIGNATURE BUTTON WITH TOOLTIP
            Item {
                Layout.fillWidth: true
                Layout.preferredWidth: 1
                height: verifyButton.implicitHeight

                Button {
                    id: verifyButton
                    text: "Verify Signature"
                    anchors.fill: parent
                    enabled: selectedPdfLabel.text !== "No PDF file selected" &&
                            selectedKeyLabel.text !== "No key selected"
                    Material.background: Material.Blue
                    Material.foreground: "white"
                    onClicked: verifyPdf()
                }

                ToolTip.visible: !verifyButton.enabled && verifyTipArea.containsMouse
                ToolTip.text: selectedPdfLabel.text === "No PDF file selected"
                            ? "Select a PDF file to enable verification"
                            : "Select a public key to enable verification"

                MouseArea {
                    id: verifyTipArea
                    anchors.fill: parent
                    hoverEnabled: true
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 120
            color: "#f5f5f5"
            radius: 8
            border.color: "#cccccc"
            border.width: 1

            ScrollView {
                anchors.fill: parent
                TextArea {
                    id: outputLog
                    text: "Status messages will appear here..."
                    wrapMode: Text.Wrap
                    readOnly: true
                    background: null
                }
            }
        }
    }

    // These functions are called from Python
    function setPdfFile(path) {
        selectedPdfLabel.text = path
    }

    function setKeyFile(path) {
        selectedKeyLabel.text = path
    }

    function append_log(message) {
        outputLog.text += "\n" + message
    }
}
