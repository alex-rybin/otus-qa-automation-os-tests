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

for data_field in data:
    if isinstance(data[data_field], dict):
        print(f'{data_field}:')
        for key, value in data[data_field].items():
            print(f'{key}: {value}')
        print()

    elif isinstance(data[data_field], list):
        print(f'{data_field}:')
        for value in data[data_field]:
            print(value)
        print()

    else:
        print(f'{data_field}: {data[data_field]}\n')
