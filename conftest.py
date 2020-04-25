import pytest

from info_collector import SystemInfoCollector


def pytest_addoption(parser):
    parser.add_argument('--pid', required=True, help='PID to show info about')
    parser.add_argument('--port', default='8000', help='Port to show state of or test')
    parser.add_argument('--package', required=True, help='Package name to show version of.')
    parser.add_argument(
        '--path',
        required=True,
        help='Path to show files from. Necessary if files_list or all params selected',
    )


@pytest.fixture(scope='session')
def collected_data(request):
    return SystemInfoCollector().get_data(
        pid=request.config.getoption('--pid'),
        package=request.config.getoption('--package'),
        path=request.config.getoption('--path'),
        port=request.config.getoption('--port'),
    )
