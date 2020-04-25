import argparse

from info_collector import SystemInfoCollector

parser = argparse.ArgumentParser()

parser.add_argument(
    '--mode',
    '-m',
    default='show',
    choices=['show', 'test'],
    help='Launch mode. Option "show" prints OS data, "test" performs tests',
)
parser.add_argument(
    '--params',
    '-p',
    default=['all'],
    choices=[
        'all',
        'net_interfaces',
        'default_route',
        'cpu_state',
        'process_state',
        'process_list',
        'cron_status',
        'port_state',
        'package_ver',
        'files_list',
        'workdir',
        'kernel_ver',
        'os_ver',
    ],
    nargs='+',
    help='Params to show or test',
)
parser.add_argument('--pid', help='PID. Necessary if process_state or all params selected')
parser.add_argument('--port', default='8000', help='Port to show state of or test')
parser.add_argument(
    '--package',
    help='Package name to show version of. Necessary if package_ver or all params selected',
)
parser.add_argument(
    '--path', help='Path to show files from. Necessary if files_list or all params selected'
)

args = parser.parse_args()

if 'all' in args.params and not (args.pid and args.package and args.path):
    parser.error('Parameter "all" requires --pid, --package and --path')

elif 'process_state' in args.params and not args.pid:
    parser.error('Parameter "process_state" requires --pid')

elif 'package_ver' in args.params and not args.package:
    parser.error('Parameter "package_ver" requires --package')

elif 'files_list' in args.params and not args.path:
    parser.error('Parameter "files_list" requires --path')

data = SystemInfoCollector().get_data(
    params=args.params, pid=args.pid, package=args.package, path=args.path, port=args.port
)

if 'interfaces' in data:
    print('Interfaces')
    for interface in data['interfaces']:
        print(f'{interface}: {data[interface]}')
    print()

if 'default_route' in data:
    print(f'Default route: {data["default_route"]}\n')

if 'processor' in data:
    print('Processor stats:')
    for stat in data['processor']:
        print(f'{stat}: {data["processor"][stat]}')
    print()

if 'process_info' in data:
    print('Process stats:')
    for stat in data['process_info']:
        print(f'{stat}: {data["process_info"][stat]}')
    print()

if 'process_list' in data:
    print('Process list:')
    for process in data['process_list']:
        print(process)
    print()

if 'cron_running' in data:
    print(f'Cron running: {data["cron_running"]}\n')

if 'ports_in_use' in data:
    print('Ports:')
    for port in data['ports_in_use']:
        print(f'Port {port} in use: {data["ports_in_use"][port]}')
    print()

if 'package_versions' in data:
    print('Package versions:')
    for package in data['package_versions']:
        print(f'Package {package} version: {data["package_versions"][package]}')
    print()

if 'files' in data:
    print('Files:')
    for file in data['files']:
        print(file)
    print()

if 'current_directory' in data:
    print(f'Current directory: {data["current_directory"]}\n')

if 'kernel_version' in data:
    print(f'Kernel: {data["kernel_version"]}')

if 'os_version' in data:
    print(f'OS version: {data["os_version"]}')
