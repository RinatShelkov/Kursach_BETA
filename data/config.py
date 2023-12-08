from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = ROOT_PATH.joinpath("src")

OPERATIONS_XLS = ROOT_PATH.joinpath("data").joinpath("operations.xls")
USER_SETTINGS_JSON = ROOT_PATH.joinpath("data").joinpath("user_settings.json")

LOG_PATH = ROOT_PATH.joinpath("log")
LOG_VIEWS_PATH = ROOT_PATH.joinpath("log").joinpath("views.log")
LOG_UTILS_PATH = ROOT_PATH.joinpath("log").joinpath("utils.log")
LOG_VIEWS_PATH = ROOT_PATH.joinpath("log").joinpath("services.log")


TEST_TRANSACTION_PATH_CSV = ROOT_PATH.joinpath("data").joinpath("test_transactions.csv")
TEST_TRANSACTION_PATH_XLSX = ROOT_PATH.joinpath("data").joinpath("test_transactions_excel.xlsx")
TEST_UTILS_JSONDecodeError = ROOT_PATH.joinpath("data").joinpath("test_get_list_dict_json.json")
TEST_UTILS_FileNotFoundError = ROOT_PATH.joinpath("data").joinpath("test_get_list_dict_invalid")
TEST_READING_JSON= ROOT_PATH.joinpath("data").joinpath("test_get_list_dict.json")
TEST_USER_SETTINGS_JSON = ROOT_PATH.joinpath("data").joinpath("test_user_settings.json")
TEST_OPERATIONS_XLS = ROOT_PATH.joinpath("data").joinpath("test_operations.xls")