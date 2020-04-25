def test_interfaces_up(collected_data):
    for key, value in collected_data['interfaces'].items():
        assert 'UP' in value


def test_default_route_present(collected_data):
    assert collected_data['default_route']


def test_processor_load_by_system(collected_data):
    assert float(collected_data['processor']['sys'].replace(',', '.')) < 75


def test_process_memory_consumption(collected_data):
    assert float(collected_data['process_info']['%mem']) < 30


def test_running_processes_list(collected_data):
    assert len(collected_data['process_list']) < 1000


def test_cron_running(collected_data):
    assert collected_data['cron_running']


def test_port_is_free(collected_data):
    for key, value in collected_data['ports_in_use'].items():
        assert not value


def test_package_not_alpha(collected_data):
    for key, value in collected_data['package_versions'].items():
        assert 'alpha' not in value.casefold()


def test_files_present(collected_data):
    assert collected_data['files']


def test_directory_not_root(collected_data):
    assert collected_data['current_directory'] != '/'


def test_kernel_not_outdated(collected_data):
    assert float(collected_data['kernel_version'].rsplit('.', 1)[0]) > 5.1


def test_os_version_reported(collected_data):
    assert collected_data['os_version']
