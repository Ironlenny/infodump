import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
//import infodump.gui.controller 1.0

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("InfoDump")

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
//            MenuItem {
//                text: qsTr("&Open")
//                onTriggered: console.log("Open action triggered");
//            }
            MenuItem {
                objectName: 'exit'
                text: qsTr("Exit")
//                onTriggered: messageRequired;
            }
        }
        Menu {
	  title: qsTr('Edit')
	  MenuItem { action: copyAction }
	  MenuItem { action: cutAction }
	  MenuItem { action: pastAction }
	}
    }

    ColumnLayout {
        id: layout
        anchors.fill: parent
        spacing: 2

        TextArea {
            objectName: "noteArea"
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        Row {
            //anchors.bottom
            //anchors.fill: parent
            spacing: 6
            TextField {
                objectName: "tagField"
                Layout.fillWidth: true
                text: "Tags..."

            }
            Button {
                objectName: "contextButton"
                text: "Save"
                onClicked: parent.clicked()
            }
        }
    }
}


