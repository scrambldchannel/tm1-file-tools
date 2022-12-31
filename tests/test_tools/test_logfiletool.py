from tm1filetools.tools import TM1LogFileTool


def test_find_logs(log_folder):

    ft = TM1LogFileTool(log_folder)

    ft._find_logs()

    assert any(log.stem == "tm1s" for log in ft._log_files)
    assert all(log.stem != "dog" for log in ft._log_files)


def test_get_process_error_logs(log_folder):

    ft = TM1LogFileTool(log_folder)

    logs = ft.get_process_error_logs()

    assert any(log.stem == "tm1processerror_23984572903485_myprocee_ss" for log in logs)
    # assert all(log.stem != "}shark" for log in logs)


def test_get_logs(log_folder):

    ft = TM1LogFileTool(log_folder)

    logs = ft.get_logs()

    assert any(log.stem == "tm1s" for log in logs)
    assert all(log.stem != "}shark" for log in logs)
