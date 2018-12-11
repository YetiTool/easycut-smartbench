from asmcnc.comms import serial_connection


class FakeScreenManager():

    def get_screen(self, screen):
        return FakeScreen()


class FakeText():
    text = ""


class FakeDeveloperWidget():
     buffer_log_mode = ""


class FakeScreen():
    grbl_serial_char_capacity = FakeText()
    grbl_serial_line_capacity = FakeText()
    developer_widget = FakeDeveloperWidget()


def test_status_message_validation():
    # 13:09:46.077 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>
    # 13:09:46.178 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ|WCO:-166.126,-213.609,-21.822>
    # 13:09:46.277 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ|Ov:100,100,100>

    s = serial_connection.SerialConnection(None, FakeScreenManager())
    messages = []
    messages.append("<Idl_|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Corrupt status
    messages.append("<Idle|MPos:0.0a0,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Corrupt position
    messages.append("<Idle|MPos:0.000,0.000,0.000a|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Corrupt position
    messages.append("<Idle|MPos:0.0000.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Missing comma
    messages.append("<Idle|MPos:0.000,0.000 0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Comma to space

    messages.append("<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>")  # Good

    errorCnt = 0
    for message in messages:
        s.process_grbl_push(message)


if __name__ == '__main__':
    test_status_message_validation()
