
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

    // INVOCACAO PROGRESSIVA
    SequentialAnimation {
        id: invocacao

        ParallelAnimation {
            NumberAnimation {
                target: anelExterno
                property: "opacity"
                from: 0
                to: 1
                duration: 1200
            }

            NumberAnimation {
                target: anelExterno
                property: "scale"
                from: 0.75
                to: 1
                duration: 1500
                easing.type: Easing.OutCubic
            }
        }

        PauseAnimation { duration: 200 }

        ParallelAnimation {
            NumberAnimation {
                target: anelMedio
                property: "opacity"
                from: 0
                to: 1
                duration: 900
            }

            NumberAnimation {
                target: anelMedio
                property: "scale"
                from: 0.7
                to: 1
                duration: 1100
                easing.type: Easing.OutBack
            }
        }

        PauseAnimation { duration: 200 }

        ParallelAnimation {
            NumberAnimation {
                target: anelInterno
                property: "opacity"
                from: 0
                to: 1
                duration: 850
            }

            NumberAnimation {
                target: anelInterno
                property: "scale"
                from: 0.6
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
                from: 0.2
                to: 1
                duration: 1400
                easing.type: Easing.OutCubic
            }
        }
    }

    Component.onCompleted: invocacao.start()

    Item {
        id: cena
        anchors.fill: parent

        // FUNDO ESCURO TRANSLUCIDO
        Rectangle {
            anchors.fill: parent
            color: "#99030A16"

            Rectangle {
                anchors.fill: parent

                gradient: Gradient {
                    GradientStop {
                        position: 0
                        color: "#33020A18"
                    }

                    GradientStop {
                        position: 0.5
                        color: "#00030A16"
                    }

                    GradientStop {
                        position: 1
                        color: "#55020A18"
                    }
                }
            }
        }

        // SELO CENTRAL
        Item {
            id: sistema

            width: 680
            height: 680
            anchors.centerIn: parent

            // ANEL EXTERNO
            Item {
                id: anelExterno

                anchors.fill: parent
                opacity: 0
                scale: 0.75

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

                        circle(330, "#438CBF", 1)
                        circle(318, "#8CEEFF", 1.5)
                        circle(306, "#347BAE", 0.8)
                        circle(294, "#63CDEB", 1.2)

                        // MARCACOES GEOMETRICAS
                        for (var i = 0; i < 120; i++) {
                            var a = i * Math.PI / 60
                            var major = i % 5 === 0

                            var r1 = major ? 294 : 301
                            var r2 = major ? 326 : 310

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
                                ? "#A3F5FF" : "#347DAA"

                            ctx.lineWidth = major ? 1.7 : 0.7
                            ctx.stroke()
                        }

                        // ARCOS LUMINOSOS
                        for (var j = 0; j < 8; j++) {
                            var start = j * Math.PI / 4

                            ctx.beginPath()
                            ctx.arc(
                                cx, cy, 337,
                                start + 0.12,
                                start + 0.43
                            )

                            ctx.strokeStyle = "#9BF5FF"
                            ctx.lineWidth = 2.2
                            ctx.stroke()
                        }

                        // PEQUENOS PONTOS DE LUZ
                        for (var k = 0; k < 24; k++) {
                            var angle = k * Math.PI / 12
                            var x = cx + Math.cos(angle) * 282
                            var y = cy + Math.sin(angle) * 282

                            ctx.beginPath()
                            ctx.arc(x, y, 2, 0, Math.PI * 2)
                            ctx.fillStyle = "#B9F9FF"
                            ctx.fill()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 100000
                    loops: Animation.Infinite
                }
            }

            // ANEL INTERMEDIARIO
            Item {
                id: anelMedio

                width: 510
                height: 510
                anchors.centerIn: parent

                opacity: 0
                scale: 0.7

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

                        circle(248, "#4EBDE6", 1.3)
                        circle(235, "#8CEEFF", 1)
                        circle(221, "#367BAE", 1)

                        // GEOMETRIA RADIAL
                        for (var i = 0; i < 12; i++) {
                            var a = i * Math.PI / 6

                            var x1 = cx + Math.cos(a) * 170
                            var y1 = cy + Math.sin(a) * 170
                            var x2 = cx + Math.cos(a) * 245
                            var y2 = cy + Math.sin(a) * 245

                            ctx.beginPath()
                            ctx.moveTo(x1, y1)
                            ctx.lineTo(x2, y2)

                            ctx.strokeStyle = "#55BFE5"
                            ctx.lineWidth = 1
                            ctx.stroke()

                            ctx.beginPath()
                            ctx.arc(x1, y1, 3, 0, Math.PI * 2)
                            ctx.fillStyle = "#B7F9FF"
                            ctx.fill()
                        }

                        // ARCOS SEGMENTADOS
                        for (var j = 0; j < 12; j++) {
                            var start = j * Math.PI / 6

                            ctx.beginPath()
                            ctx.arc(
                                cx, cy, 205,
                                start + 0.08,
                                start + 0.32
                            )

                            ctx.strokeStyle = "#A3F4FF"
                            ctx.lineWidth = 2
                            ctx.stroke()
                        }

                        // PONTAS GEOMETRICAS
                        for (var k = 0; k < 12; k++) {
                            var angle = k * Math.PI / 6
                            var px = cx + Math.cos(angle) * 230
                            var py = cy + Math.sin(angle) * 230

                            ctx.save()
                            ctx.translate(px, py)
                            ctx.rotate(angle)

                            ctx.beginPath()
                            ctx.moveTo(0, -7)
                            ctx.lineTo(5, 0)
                            ctx.lineTo(0, 7)
                            ctx.lineTo(-5, 0)
                            ctx.closePath()

                            ctx.strokeStyle = "#A6F7FF"
                            ctx.lineWidth = 1.3
                            ctx.stroke()

                            ctx.restore()
                        }
                    }
                }

                RotationAnimation on rotation {
                    from: 360
                    to: 0
                    duration: 72000
                    loops: Animation.Infinite
                }
            }

            // ANEL INTERNO
            Item {
                id: anelInterno

                width: 370
                height: 370
                anchors.centerIn: parent

                opacity: 0
                scale: 0.6

                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        var cx = width / 2
                        var cy = height / 2

                        ctx.clearRect(0, 0, width, height)

                        function polygon(sides, radius, offset, color) {
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
                            ctx.strokeStyle = color
                            ctx.stroke()
                        }

                        ctx.lineWidth = 1.3

                        // FORMAS SOBREPOSTAS
                        polygon(6, 165, 0, "#6ADBF6")
                        polygon(6, 165, Math.PI / 6, "#A1F5FF")
                        polygon(12, 140, Math.PI / 12, "#4BAAD6")
                        polygon(8, 115, 0, "#80E7FA")

                        // ESTRELA CENTRAL
                        ctx.beginPath()

                        for (var j = 0; j <= 24; j++) {
                            var r = j % 2 === 0 ? 105 : 48
                            var a = j * Math.PI / 12 - Math.PI / 2

                            var x = cx + Math.cos(a) * r
                            var y = cy + Math.sin(a) * r

                            if (j === 0)
                                ctx.moveTo(x, y)
                            else
                                ctx.lineTo(x, y)
                        }

                        ctx.closePath()
                        ctx.strokeStyle = "#C0FBFF"
                        ctx.lineWidth = 1.6
                        ctx.stroke()

                        // RAIOS INTERNOS
                        for (var k = 0; k < 24; k++) {
                            var angle = k * Math.PI / 12

                            ctx.beginPath()
                            ctx.moveTo(
                                cx + Math.cos(angle) * 112,
                                cy + Math.sin(angle) * 112
                            )
                            ctx.lineTo(
                                cx + Math.cos(angle) * 155,
                                cy + Math.sin(angle) * 155
                            )

                            ctx.strokeStyle = "#418FBE"
                            ctx.lineWidth = 0.8
                            ctx.stroke()
                        }

                        // CIRCULO DE CONTENCAO
                        ctx.beginPath()
                        ctx.arc(cx, cy, 178, 0, Math.PI * 2)
                        ctx.strokeStyle = "#83EFFF"
                        ctx.lineWidth = 1.4
                        ctx.stroke()
                    }
                }

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 42000
                    loops: Animation.Infinite
                }
            }

            // PARTICULAS
            Item {
                id: particulas

                anchors.fill: parent
                opacity: 0

                RotationAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 50000
                    loops: Animation.Infinite
                }

                Repeater {
                    model: 38

                    Item {
                        property real angulo: index * 9.47
                        property real distancia: 245 + (index % 5) * 17

                        width: 14
                        height: 14

                        x: 340 +
                           Math.cos(angulo * Math.PI / 180) * distancia - 7

                        y: 340 +
                           Math.sin(angulo * Math.PI / 180) * distancia - 7

                        Rectangle {
                            anchors.centerIn: parent

                            width: index % 4 === 0 ? 4 : 2
                            height: width
                            radius: width / 2
                            color: "#C4FAFF"

                            SequentialAnimation on opacity {
                                loops: Animation.Infinite

                                NumberAnimation {
                                    to: 0.95
                                    duration: 700 + index * 35
                                }

                                NumberAnimation {
                                    to: 0.12
                                    duration: 700 + index * 35
                                }
                            }
                        }
                    }
                }
            }

            // NUCLEO ENERGETICO
            Item {
                id: nucleo

                width: 190
                height: 190
                anchors.centerIn: parent

                opacity: 0

                // AURA
                Canvas {
                    anchors.fill: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.clearRect(0, 0, width, height)

                        var grad = ctx.createRadialGradient(
                            95, 95, 2,
                            95, 95, 95
                        )

                        grad.addColorStop(0, "rgba(225,255,255,0.48)")
                        grad.addColorStop(0.25, "rgba(90,220,255,0.25)")
                        grad.addColorStop(0.6, "rgba(30,140,220,0.10)")
                        grad.addColorStop(1, "rgba(10,80,160,0)")

                        ctx.fillStyle = grad
                        ctx.fillRect(0, 0, width, height)
                    }
                }

                // ONDAS DE ENERGIA
                Repeater {
                    model: 3

                    Rectangle {
                        anchors.centerIn: parent

                        width: 45 + index * 24
                        height: width
                        radius: width / 2

                        color: "transparent"
                        border.color: "#A4F7FF"
                        border.width: 1.2
                        opacity: 0.4

                        SequentialAnimation on scale {
                            loops: Animation.Infinite

                            PauseAnimation {
                                duration: index * 450
                            }

                            NumberAnimation {
                                from: 0.6
                                to: 1.8
                                duration: 2300
                                easing.type: Easing.OutCubic
                            }
                        }

                        SequentialAnimation on opacity {
                            loops: Animation.Infinite

                            PauseAnimation {
                                duration: index * 450
                            }

                            NumberAnimation {
                                from: 0.65
                                to: 0
                                duration: 2300
                            }
                        }
                    }
                }

                // LUZ CENTRAL
                Canvas {
                    width: 100
                    height: 100
                    anchors.centerIn: parent

                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.clearRect(0, 0, width, height)

                        var grad = ctx.createRadialGradient(
                            50, 50, 1,
                            50, 50, 50
                        )

                        grad.addColorStop(0, "#FFFFFF")
                        grad.addColorStop(0.18, "#D9FFFF")
                        grad.addColorStop(0.42, "#82EFFF")
                        grad.addColorStop(0.72, "#32C5F0")
                        grad.addColorStop(1, "rgba(20,120,210,0)")

                        ctx.fillStyle = grad
                        ctx.fillRect(0, 0, width, height)
                    }
                }

                SequentialAnimation on scale {
                    loops: Animation.Infinite

                    NumberAnimation {
                        to: 1.07
                        duration: 2100
                        easing.type: Easing.InOutSine
                    }

                    NumberAnimation {
                        to: 0.94
                        duration: 2100
                        easing.type: Easing.InOutSine
                    }
                }
            }
        }
    }
}
