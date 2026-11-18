
import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: janela

    visible: true
    visibility: Window.FullScreen
    color: "transparent"

    flags: Qt.FramelessWindowHint |
           Qt.WindowStaysOnTopHint |
           Qt.Tool

    title: "Epamin"

    Shortcut {
        sequence: "Escape"
        onActivated: Qt.quit()
    }

    property color azul: "#39CFFF"
    property color ciano: "#9AF5FF"
    property color azulEscuro: "#087CA8"

    Item {
        id: interface
        anchors.fill: parent

        // Centro da composição
        Item {
            id: sistemaCentral

            width: 620
            height: 620
            anchors.centerIn: parent

            // CAMADA 1 - ANEL EXTERNO
            Item {
                id: anelExterno
                width: 610
                height: 610
                anchors.centerIn: parent

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)
                        ctx.lineWidth = 1.5
                        ctx.strokeStyle = "#398DCB"

                        ctx.beginPath()
                        ctx.arc(cx, cy, 295, 0, Math.PI * 2)
                        ctx.stroke()

                        ctx.beginPath()
                        ctx.arc(cx, cy, 285, 0, Math.PI * 2)
                        ctx.stroke()

                        // Marcações externas
                        for (var i = 0; i < 120; i++) {
                            var angulo = i * Math.PI / 60
                            var raio1 = i % 5 === 0 ? 270 : 278
                            var raio2 = 290

                            ctx.beginPath()
                            ctx.moveTo(
                                cx + Math.cos(angulo) * raio1,
                                cy + Math.sin(angulo) * raio1
                            )
                            ctx.lineTo(
                                cx + Math.cos(angulo) * raio2,
                                cy + Math.sin(angulo) * raio2
                            )

                            ctx.strokeStyle =
                                i % 5 === 0 ? "#65DFFF" : "#286A9A"

                            ctx.lineWidth = i % 5 === 0 ? 2 : 1
                            ctx.stroke()
                        }

                        // Segmentos luminosos
                        for (var j = 0; j < 8; j++) {
                            var inicio = j * Math.PI / 4
                            ctx.beginPath()
                            ctx.arc(cx, cy, 302,
                                    inicio, inicio + 0.22)
                            ctx.strokeStyle = "#54DFFF"
                            ctx.lineWidth = 3
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 55000
                    loops: Animation.Infinite
                }
            }

            // CAMADA 2 - ANEL INTERMEDIÁRIO
            Item {
                id: anelIntermediario

                width: 470
                height: 470
                anchors.centerIn: parent

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        ctx.strokeStyle = "#45CFFF"
                        ctx.lineWidth = 2

                        ctx.beginPath()
                        ctx.arc(cx, cy, 220, 0, Math.PI * 2)
                        ctx.stroke()

                        ctx.beginPath()
                        ctx.arc(cx, cy, 205, 0, Math.PI * 2)
                        ctx.stroke()

                        // Arcos segmentados
                        for (var i = 0; i < 12; i++) {
                            var inicio = i * Math.PI / 6

                            ctx.beginPath()
                            ctx.arc(
                                cx, cy, 212,
                                inicio, inicio + 0.20
                            )

                            ctx.strokeStyle = "#91F4FF"
                            ctx.lineWidth = 3
                            ctx.stroke()
                        }

                        // Pequenas marcações internas
                        for (var j = 0; j < 72; j++) {
                            var angulo = j * Math.PI / 36

                            ctx.beginPath()
                            ctx.moveTo(
                                cx + Math.cos(angulo) * 190,
                                cy + Math.sin(angulo) * 190
                            )
                            ctx.lineTo(
                                cx + Math.cos(angulo) * 199,
                                cy + Math.sin(angulo) * 199
                            )

                            ctx.strokeStyle = "#328CB8"
                            ctx.lineWidth = 1
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 360
                    to: 0
                    duration: 32000
                    loops: Animation.Infinite
                }
            }

            // CAMADA 3 - ANEL INTERNO
            Item {
                id: anelInterno

                width: 340
                height: 340
                anchors.centerIn: parent

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        ctx.strokeStyle = "#8CEEFF"
                        ctx.lineWidth = 2

                        ctx.beginPath()
                        ctx.arc(cx, cy, 155, 0, Math.PI * 2)
                        ctx.stroke()

                        ctx.beginPath()
                        ctx.arc(cx, cy, 140, 0, Math.PI * 2)
                        ctx.stroke()

                        // Elementos geométricos
                        for (var i = 0; i < 24; i++) {
                            var angulo = i * Math.PI / 12
                            var x1 = cx + Math.cos(angulo) * 125
                            var y1 = cy + Math.sin(angulo) * 125
                            var x2 = cx + Math.cos(angulo) * 155
                            var y2 = cy + Math.sin(angulo) * 155

                            ctx.beginPath()
                            ctx.moveTo(x1, y1)
                            ctx.lineTo(x2, y2)

                            ctx.strokeStyle = "#49CFFF"
                            ctx.lineWidth = 1.5
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 18000
                    loops: Animation.Infinite
                }
            }

            // PARTÍCULAS ORBITAIS
            Repeater {
                model: 36

                Rectangle {
                    property real angulo: index * 10
                    property real distancia: 245 + (index % 4) * 9

                    width: index % 3 === 0 ? 4 : 2
                    height: width
                    radius: width / 2

                    color: index % 2 === 0 ? "#B8F8FF" : "#35CFFF"

                    x: sistemaCentral.width / 2 +
                       Math.cos(angulo * Math.PI / 180) * distancia -
                       width / 2

                    y: sistemaCentral.height / 2 +
                       Math.sin(angulo * Math.PI / 180) * distancia -
                       height / 2

                    SequentialAnimation on opacity {
                        loops: Animation.Infinite

                        NumberAnimation {
                            to: 0.95
                            duration: 700 + index * 40
                        }

                        NumberAnimation {
                            to: 0.15
                            duration: 700 + index * 40
                        }
                    }
                }
            }

            // NÚCLEO CENTRAL
            Item {
                id: nucleo
                width: 150
                height: 150
                anchors.centerIn: parent

                // Halo externo
                Rectangle {
                    anchors.centerIn: parent
                    width: 150
                    height: 150
                    radius: width / 2
                    color: "#123B78"
                    opacity: 0.15
                }

                // Camada luminosa
                Rectangle {
                    anchors.centerIn: parent
                    width: 120
                    height: 120
                    radius: width / 2
                    color: "#087BB5"
                    opacity: 0.24
                    border.color: "#5BEAFF"
                    border.width: 2
                }

                // Núcleo interno
                Rectangle {
                    anchors.centerIn: parent
                    width: 82
                    height: 82
                    radius: width / 2

                    gradient: Gradient {
                        GradientStop {
                            position: 0.0
                            color: "#B7FAFF"
                        }
                        GradientStop {
                            position: 0.35
                            color: "#36CFFF"
                        }
                        GradientStop {
                            position: 1.0
                            color: "#075A9D"
                        }
                    }

                    border.color: "#D5FFFF"
                    border.width: 2

                    Rectangle {
                        anchors.centerIn: parent
                        width: 32
                        height: 32
                        radius: width / 2
                        color: "#FFFFFF"
                        opacity: 0.8
                    }
                }

                SequentialAnimation on scale {
                    loops: Animation.Infinite

                    NumberAnimation {
                        to: 1.09
                        duration: 1700
                        easing.type: Easing.InOutSine
                    }

                    NumberAnimation {
                        to: 0.96
                        duration: 1700
                        easing.type: Easing.InOutSine
                    }
                }
            }
        }

        // IDENTIFICAÇÃO SUPERIOR
        Column {
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 32
            spacing: 5

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "E P A M I N"
                color: "#B8F5FF"
                font.pixelSize: 24
                font.bold: true
                font.letterSpacing: 7
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "AUTONOMOUS SYSTEM"
                color: "#398DBB"
                font.pixelSize: 9
                font.letterSpacing: 4
            }
        }

        // PAINEL ESQUERDO
        Column {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            anchors.leftMargin: 55
            spacing: 9

            Text {
                text: "SYSTEM STATUS"
                color: "#75DFFF"
                font.pixelSize: 11
                font.bold: true
            }

            Text {
                text: "CORE ONLINE"
                color: "#B8F5FF"
                font.pixelSize: 10
            }

            Text {
                text: "VOICE MODULE: READY"
                color: "#4B9FCE"
                font.pixelSize: 9
            }

            Text {
                text: "NEURAL LINK: STANDBY"
                color: "#4B9FCE"
                font.pixelSize: 9
            }
        }

        // PAINEL DIREITO
        Column {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: 55
            spacing: 9

            Text {
                text: "SYSTEM MONITOR"
                color: "#75DFFF"
                font.pixelSize: 11
                font.bold: true
            }

            Text {
                text: "PROCESSING: IDLE"
                color: "#B8F5FF"
                font.pixelSize: 10
            }

            Text {
                text: "INTERFACE: ACTIVE"
                color: "#4B9FCE"
                font.pixelSize: 9
            }

            Text {
                text: "SECURITY: ENABLED"
                color: "#4B9FCE"
                font.pixelSize: 9
            }
        }

        // TEXTO INFERIOR
        Column {
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 35
            spacing: 7

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "AGUARDANDO INSTRUÇÕES"
                color: "#A6F2FF"
                font.pixelSize: 12
                font.letterSpacing: 3
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "E P A M I N   //   VERSION 0.2"
                color: "#397FA9"
                font.pixelSize: 9
                font.letterSpacing: 2
            }
        }
    }
}
