import Qt3D.Core 2.12
import Qt3D.Extras 2.13
import QtQuick 2.0

Entity {
    id: titleText
    components: [ Transform { translation: Qt.vector3d(0.0, 10.0, 30.0) } ]

    Text2DEntity {
        color: "white"
        text: "MY TITLE"
    }
}