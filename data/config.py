from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = ROOT_PATH.joinpath("src")
LOG_PATH = ROOT_PATH.joinpath("log")
OPERATIONS_XLS = ROOT_PATH.joinpath("data").joinpath("operations.xls")
TEST_UTILS_JSONDecodeError = ROOT_PATH.joinpath("data").joinpath("test_get_list_dict_json.json")
TEST_UTILS_FileNotFoundError = ROOT_PATH.joinpath("data").joinpath("test_get_list_dict_invalid")
LOG_VIEWS_PATH = ROOT_PATH.joinpath("log").joinpath("views.log")
LOG_UTILS_PATH = ROOT_PATH.joinpath("log").joinpath("utils.log")
OPER = ROOT_PATH.joinpath("data").joinpath("Oper.xls")
USER_SETTINGS_JSON = ROOT_PATH.joinpath("data").joinpath("user_settings.json")

print(OPERATIONS_XLS)
