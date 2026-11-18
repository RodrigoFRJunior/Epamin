
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

    property string estado: "INVOCANDO"
    property color luz: "#83EFFF"
    property color azul: "#35BCEB"
    property color profundo: "#176EBA"

    Shortcut {
        sequence: "Escape"
        onActivated: Qt.quit()
    }

    // INVOCACAO DOS ELEMENTOS
    SequentialAnimation {
        id: invocacao

        ParallelAnimation {
            NumberAnimation {
                target: circuloExterno
                property: "opacity"
                from: 0
                to: 1
                duration: 1100
            }
            NumberAnimation {
                target: circuloExterno
                property: "scale"
                from: 0.72
                to: 1
                duration: 1400
                easing.type: Easing.OutCubic
            }
        }

        PauseAnimation { duration: 180 }

        ParallelAnimation {
            NumberAnimation {
                target: circuloMedio
                property: "opacity"
                from: 0
                to: 1
                duration: 900
            }
            NumberAnimation {
                target: circuloMedio
                property: "scale"
                from: 0.65
                to: 1
                duration: 1100
                easing.type: Easing.OutBack
            }
        }

        PauseAnimation { duration: 180 }

        ParallelAnimation {
            NumberAnimation {
                target: circuloInterno
                property: "opacity"
                from: 0
                to: 1
                duration: 850
            }
            NumberAnimation {
                target: circuloInterno
                property: "scale"
                from: 0.55
                to: 1
                duration: 1000
                easing.type: Easing.OutBack
            }
        }

        PauseAnimation { duration: 250 }

        ParallelAnimation {
            NumberAnimation {
                target: particulas
                property: "opacity"
                from: 0
                to: 1
                duration: 1000
            }
            NumberAnimation {
                target: nucleo
                property: "opacity"
                from: 0
                to: 1
                duration: 1200
            }
            NumberAnimation {
                target: nucleo
                property: "scale"
                from: 0.1
                to: 1
                duration: 1400
                easing.type: Easing.OutElastic
            }
        }

        ScriptAction {
            script: janela.estado = "AGUARDANDO"
        }
    }

    Component.onCompleted: invocacao.start()

    Item {
        id: cena
        anchors.fill: parent

        // COMPOSICAO CENTRAL
        Item {
            id: circuloPrincipal

            width: 690
            height: 690
            anchors.centerIn: parent

            // CIRCULO EXTERNO: GRANDE SELO ARCANO
            Item {
                id: circuloExterno

                width: 680
                height: 680
                anchors.centerIn: parent

                opacity: 0
                scale: 0.72

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        function circle(r, color, line) {
                            ctx.beginPath()
                            ctx.arc(cx, cy, r, 0, Math.PI * 2)
                            ctx.strokeStyle = color
                            ctx.lineWidth = line
                            ctx.stroke()
                        }

                        circle(330, "#347FBD", 1.2)
                        circle(318, "#83EFFF", 1.5)
                        circle(310, "#286DA9", 1)
                        circle(298, "#5BCDF1", 1.4)

                        // DIVISORES RADIAIS
                        for (var i = 0; i < 144; i++) {
                            var a = i * Math.PI / 72
                            var major = i % 6 === 0
                            var r1 = major ? 298 : 306
                            var r2 = major ? 326 : 313

                            ctx.beginPath()
                            ctx.moveTo(
                                cx + Math.cos(a) * r1,
                                cy + Math.sin(a) * r1
                            )
                            ctx.lineTo(
                                cx + Math.cos(a) * r2,
                                cy + Math.sin(a) * r2
                            )

                            ctx.strokeStyle = major
                                ? "#9AF5FF" : "#347BAF"
                            ctx.lineWidth = major ? 2 : 0.8
                            ctx.stroke()
                        }

                        // PEQUENOS LOSANGOS
                        for (var j = 0; j < 24; j++) {
                            var angle = j * Math.PI / 12
                            var x = cx + Math.cos(angle) * 280
                            var y = cy + Math.sin(angle) * 280

                            ctx.save()
                            ctx.translate(x, y)
                            ctx.rotate(angle)

                            ctx.beginPath()
                            ctx.moveTo(0, -7)
                            ctx.lineTo(4, 0)
                            ctx.lineTo(0, 7)
                            ctx.lineTo(-4, 0)
                            ctx.closePath()

                            ctx.strokeStyle = "#9AF5FF"
                            ctx.lineWidth = 1.2
                            ctx.stroke()

                            ctx.restore()
                        }

                        // ARCO SUPERIOR E INFERIOR
                        for (var k = 0; k < 4; k++) {
                            var start = k * Math.PI / 2 + 0.18

                            ctx.beginPath()
                            ctx.arc(
                                cx, cy, 337,
                                start, start + 0.38
                            )
                            ctx.strokeStyle = "#83EFFF"
                            ctx.lineWidth = 2.5
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 90000
                    loops: Animation.Infinite
                }
            }

            // CIRCULO MEDIO: RUNAS E INSCRICOES
            Item {
                id: circuloMedio

                width: 535
                height: 535
                anchors.centerIn: parent

                opacity: 0
                scale: 0.65

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        function circle(r, color, line) {
                            ctx.beginPath()
                            ctx.arc(cx, cy, r, 0, Math.PI * 2)
                            ctx.strokeStyle = color
                            ctx.lineWidth = line
                            ctx.stroke()
                        }

                        circle(255, "#4DBCEB", 1.5)
                        circle(245, "#83EFFF", 0.8)
                        circle(232, "#286DA9", 1.2)

                        // INSCRICOES ARCANAS FICTICIAS
                        for (var i = 0; i < 48; i++) {
                            var a = i * Math.PI / 24
                            var x = cx + Math.cos(a) * 238
                            var y = cy + Math.sin(a) * 238

                            ctx.save()
                            ctx.translate(x, y)
                            ctx.rotate(a + Math.PI / 2)

                            ctx.strokeStyle = i % 3 === 0
                                ? "#A7F7FF" : "#4B9ECF"
                            ctx.lineWidth = 1.5

                            ctx.beginPath()
                            ctx.moveTo(-4, -7)
                            ctx.lineTo(0, -2)
                            ctx.lineTo(4, -7)
                            ctx.moveTo(0, -2)
                            ctx.lineTo(0, 7)
                            ctx.moveTo(-4, 4)
                            ctx.lineTo(4, 4)
                            ctx.stroke()

                            ctx.restore()
                        }

                        // GEOMETRIA INTERNA
                        for (var j = 0; j < 12; j++) {
                            var angle = j * Math.PI / 6

                            var x1 = cx + Math.cos(angle) * 185
                            var y1 = cy + Math.sin(angle) * 185
                            var x2 = cx + Math.cos(angle) * 230
                            var y2 = cy + Math.sin(angle) * 230

                            ctx.beginPath()
                            ctx.moveTo(x1, y1)
                            ctx.lineTo(x2, y2)

                            ctx.strokeStyle = "#57C8EF"
                            ctx.lineWidth = 1
                            ctx.stroke()

                            // PONTOS DE CONEXAO
                            ctx.beginPath()
                            ctx.arc(x1, y1, 3, 0, Math.PI * 2)
                            ctx.fillStyle = "#B5FAFF"
                            ctx.fill()
                        }

                        // ARCOS SEGMENTADOS
                        for (var k = 0; k < 8; k++) {
                            var start = k * Math.PI / 4

                            ctx.beginPath()
                            ctx.arc(
                                cx, cy, 215,
                                start, start + 0.32
                            )
                            ctx.strokeStyle = "#A0F4FF"
                            ctx.lineWidth = 3
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 360
                    to: 0
                    duration: 62000
                    loops: Animation.Infinite
                }
            }

            // CIRCULO INTERNO: GEOMETRIA SAGRADA
            Item {
                id: circuloInterno

                width: 380
                height: 380
                anchors.centerIn: parent

                opacity: 0
                scale: 0.55

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        function polygon(sides, radius, offset) {
                            ctx.beginPath()

                            for (var i = 0; i <= sides; i++) {
                                var a = i * Math.PI * 2 / sides + offset
                                var x = cx + Math.cos(a) * radius
                                var y = cy + Math.sin(a) * radius

                                if (i === 0)
                                    ctx.moveTo(x, y)
                                else
                                    ctx.lineTo(x, y)
                            }

                            ctx.closePath()
                            ctx.stroke()
                        }

                        // CIRCULOS DE CONTENCAO
                        ctx.strokeStyle = "#83EFFF"
                        ctx.lineWidth = 1.5

                        ctx.beginPath()
                        ctx.arc(cx, cy, 178, 0, Math.PI * 2)
                        ctx.stroke()

                        ctx.beginPath()
                        ctx.arc(cx, cy, 164, 0, Math.PI * 2)
                        ctx.stroke()

                        // HEXAGONOS E ESTRELAS
                        ctx.strokeStyle = "#5BD7F7"
                        ctx.lineWidth = 1.3

                        polygon(6, 150, Math.PI / 6)
                        polygon(6, 150, 0)
                        polygon(12, 130, Math.PI / 12)

                        // ESTRELA CENTRAL
                        ctx.strokeStyle = "#B5FAFF"
                        ctx.lineWidth = 1.5

                        ctx.beginPath()

                        for (var j = 0; j <= 12; j++) {
                            var r = j % 2 === 0 ? 105 : 48
                            var angle = j * Math.PI / 6 - Math.PI / 2
                            var x = cx + Math.cos(angle) * r
                            var y = cy + Math.sin(angle) * r

                            if (j === 0)
                                ctx.moveTo(x, y)
                            else
                                ctx.lineTo(x, y)
                        }

                        ctx.closePath()
                        ctx.stroke()

                        // RAIOS INTERNOS
                        for (var k = 0; k < 24; k++) {
                            var a = k * Math.PI / 12

                            ctx.beginPath()
                            ctx.moveTo(
                                cx + Math.cos(a) * 110,
                                cy + Math.sin(a) * 110
                            )
                            ctx.lineTo(
                                cx + Math.cos(a) * 155,
                                cy + Math.sin(a) * 155
                            )

                            ctx.strokeStyle = "#398FC5"
                            ctx.lineWidth = 0.8
                            ctx.stroke()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 38000
                    loops: Animation.Infinite
                }
            }

            // PEQUENOS GLIFOS ORBITAIS
            Item {
                id: particulas
                anchors.fill: parent
                opacity: 0

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 45000
                    loops: Animation.Infinite
                }

                Repeater {
                    model: 48

                    Item {
                        property real angulo: index * 7.5
                        property real distancia: 270 + (index % 3) * 12

                        x: circuloPrincipal.width / 2 +
                           Math.cos(angulo * Math.PI / 180) * distancia - 7

                        y: circuloPrincipal.height / 2 +
                           Math.sin(angulo * Math.PI / 180) * distancia - 7

                        width: 14
                        height: 14

                        Rectangle {
                            anchors.centerIn: parent
                            width: index % 4 === 0 ? 5 : 2.5
                            height: width
                            radius: width / 2
                            color: "#B9F9FF"

                            SequentialAnimation on opacity {
                                loops: Animation.Infinite

                                NumberAnimation {
                                    to: 0.95
                                    duration: 600 + index * 35
                                }

                                NumberAnimation {
                                    to: 0.18
                                    duration: 600 + index * 35
                                }
                            }
                        }
                    }
                }
            }

            // NUCLEO DE ENERGIA
            Item {
                id: nucleo

                width: 180
                height: 180
                anchors.centerIn: parent

                opacity: 0

                // HALO EXTERNO
                Rectangle {
                    anchors.centerIn: parent
                    width: 180
                    height: 180
                    radius: width / 2
                    color: "#247FC4"
                    opacity: 0.07
                    border.color: "#75E9FF"
                    border.width: 1
                }

                // ANEL DE ENERGIA
                Rectangle {
                    anchors.centerIn: parent
                    width: 135
                    height: 135
                    radius: width / 2
                    color: "transparent"
                    border.color: "#5BDFFF"
                    border.width: 2
                    opacity: 0.75
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 108
                    height: 108
                    radius: width / 2
                    color: "#0D5A9C"
                    opacity: 0.25
                    border.color: "#A5F8FF"
                    border.width: 1
                }

                // ENERGIA CENTRAL
                Rectangle {
                    anchors.centerIn: parent
                    width: 68
                    height: 68
                    radius: width / 2

                    gradient: Gradient {
                        GradientStop {
                            position: 0
                            color: "#F0FFFF"
                        }
                        GradientStop {
                            position: 0.25
                            color: "#9BF4FF"
                        }
                        GradientStop {
                            position: 0.65
                            color: "#39C9F2"
                        }
                        GradientStop {
                            position: 1
                            color: "#0873B6"
                        }
                    }

                    opacity: 0.92
                }

                SequentialAnimation on scale {
                    loops: Animation.Infinite

                    NumberAnimation {
                        to: 1.07
                        duration: 1900
                        easing.type: Easing.InOutSine
                    }

                    NumberAnimation {
                        to: 0.96
                        duration: 1900
                        easing.type: Easing.InOutSine
                    }
                }
            }
        }

        // IDENTIDADE DISCRETA
        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 30
            spacing: 6

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "E P A M I N"
                color: "#B8F8FF"
                font.pixelSize: 21
                font.letterSpacing: 8
                font.weight: Font.Light
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "SISTEMA ARCANO"
                color: "#5DB9E1"
                font.pixelSize: 9
                font.letterSpacing: 5
            }
        }

        // ESTADO DO SISTEMA
        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 34
            spacing: 8

            Text {
                anchors.horizontalCenter: parent.horizontalCenter

                text: estado === "INVOCANDO"
                      ? "DESPERTANDO"
                      : "AGUARDANDO"

                color: "#B5F8FF"
                font.pixelSize: 12
                font.letterSpacing: 5
            }

            Rectangle {
                anchors.horizontalCenter: parent.horizontalCenter
                width: 100
                height: 1
                color: "#5BDFFF"
                opacity: 0.65
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "EPAMIN"
                color: "#4A91BD"
                font.pixelSize: 9
                font.letterSpacing: 4
            }
        }
    }
}
