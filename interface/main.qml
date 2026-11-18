import QtQuick
import QtQuick.Window

Window {
    id: janela

    visible: true
    visibility: Window.FullScreen

    width: Screen.width
    height: Screen.height

    color: "transparent"

    flags: Qt.FramelessWindowHint |
           Qt.WindowStaysOnTopHint

    title: "EPAMIN"

    // Paleta visual
    property color azul: "#168FCB"
    property color ciano: "#54DFFF"
    property color branco: "#DDF8FF"

    // Fundo transparente
    Rectangle {
        anchors.fill: parent
        color: "transparent"
    }

    // Núcleo central
    Item {
        id: nucleo

        width: 360
        height: 360

        anchors.centerIn: parent

        // Anel externo
        Rectangle {
            width: 340
            height: 340

            anchors.centerIn: parent

            radius: width / 2
            color: "transparent"

            border.color: azul
            border.width: 2

            opacity: 0.65

            RotationAnimation on rotation {
                from: 0
                to: 360
                duration: 30000
                loops: Animation.Infinite
            }
        }

        // Segundo anel
        Rectangle {
            width: 290
            height: 290

            anchors.centerIn: parent

            radius: width / 2
            color: "transparent"

            border.color: ciano
            border.width: 1

            opacity: 0.8

            RotationAnimation on rotation {
                from: 360
                to: 0
                duration: 18000
                loops: Animation.Infinite
            }
        }

        // Anel interno
        Rectangle {
            width: 220
            height: 220

            anchors.centerIn: parent

            radius: width / 2
            color: "transparent"

            border.color: azul
            border.width: 2

            opacity: 0.8

            RotationAnimation on rotation {
                from: 0
                to: 360
                duration: 12000
                loops: Animation.Infinite
            }
        }

        // Núcleo luminoso
        Rectangle {
            id: centro

            width: 130
            height: 130

            anchors.centerIn: parent

            radius: width / 2

            color: "#102B40"

            border.color: ciano
            border.width: 2

            opacity: 0.95

            SequentialAnimation on scale {
                loops: Animation.Infinite

                NumberAnimation {
                    to: 1.08
                    duration: 1400
                    easing.type: Easing.InOutSine
                }

                NumberAnimation {
                    to: 1.0
                    duration: 1400
                    easing.type: Easing.InOutSine
                }
            }

            Column {
                anchors.centerIn: parent
                spacing: 5

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "◈"
                    color: ciano
                    font.pixelSize: 32
                }

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "EPAMIN"
                    color: branco
                    font.pixelSize: 17
                    font.bold: true
                    font.letterSpacing: 3
                }

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "SYSTEM ONLINE"
                    color: ciano
                    font.pixelSize: 8
                    font.letterSpacing: 2
                }
            }
        }
    }

    // Indicadores superiores
    Text {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 30

        text: "EPAMIN // SYSTEM INTERFACE"
        color: ciano

        font.pixelSize: 12
        font.letterSpacing: 3
    }

    Text {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 30

        text: "LOCAL SYSTEM • ACTIVE"
        color: ciano

        font.pixelSize: 11
        font.letterSpacing: 2
    }

    // Informações inferiores
    Column {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter

        anchors.bottomMargin: 45
        spacing: 8

        Text {
            anchors.horizontalCenter: parent.horizontalCenter

            text: "AGUARDANDO INTERAÇÃO"
            color: branco

            font.pixelSize: 13
            font.letterSpacing: 4
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter

            text: "VOICE INTERFACE // STANDBY"
            color: ciano

            font.pixelSize: 9
            font.letterSpacing: 3
        }
    }

    // Atalho para fechar o protótipo
    Item {
        focus: true

        Keys.onEscapePressed: {
            Qt.quit()
        }
    }
}
