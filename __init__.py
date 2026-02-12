import shutil
import os
import glob
from pathlib import Path
from libs.helpers import print_message, print_choices, ERROR
from utils import set_env_variable


# Module global settings
__module_disabled_methods__ = []
__module_name__ = 'KubeConfigHelper'
__module_author__ = 'JoePeach88'
__module_version__ = '1.0.0'
__module_link__ = 'https://github.com/JoePeach88/kube-helper-kubeconfig'
__methods_static_aliases__ = {
    'ls': ['ll', 'list'],
    'store': ['save'],
    'rm': ['remove', 'delete', 'drop']
}


class kubeconfigHelper:
    """
    kubeconfigHelper - module to work with kubeconfigs.
    """
    def __init__(self, settings: dict):
        self.settings = settings

    def store(self, kubeconfig: str, dest: str = None):
        """
        Method stores kubeconfig to specified location `dest` or to default kubeconfigs location from config file.
        Usage:
            1. Without specified location (to default kubeconfigs location):
                kubeconfig store --kubeconfig /path/to/kubeconfig
            2. With specified location
                kubeconfig store --kubeconfig /path/to/kubeconfig --dest /path/to/save/kubeconfig
        """
        try:
            dest_path = Path(self.settings.get('kubeconfigs_location', ''))
            if not dest_path:
                dest_path = Path.home() / '.kube'
            dest_path = Path(dest) if dest else dest_path
            dest_path = Path(dest_path / Path(kubeconfig).name)
            shutil.copy2(kubeconfig, dest_path)
            print_message(f"kubeconfig '{kubeconfig}' copied to '{dest_path}' successfully.")
        except FileNotFoundError:
            print_message(f"The source file '{kubeconfig}' was not found.", ERROR)
        except PermissionError:
            print_message(f"Permission denied. Cannot copy file to '{dest_path}'.", ERROR)
        except Exception as e:
            print_message(f"An unexpected error occurred: {e}", ERROR)

    def ls(self, pretty: bool = True, location: str = 'default,env,kubeconfigs_location'):
        """
        Method displays all available kubeconfigs from all known kubeconfigs locations.
        Usage:
            kubeconfig ls
        """
        kubeconfig_list = []
        locations = location.split(',')
        if 'env' in locations:
            # Check KUBECONFIG environment variable
            kubeconfig_env = os.getenv('KUBECONFIG')
            if kubeconfig_env:
                print_message("Found kubeconfigs in env variable KUBECONFIG.")
                separator = ';' if os.name == 'nt' else ':'
                paths = kubeconfig_env.split(separator)

                for path_str in paths:
                    path = Path(path_str.strip()).expanduser().resolve()
                    if path.exists() and path.is_file() and str(path) not in kubeconfig_list:
                        kubeconfig_list.append(str(path))
        
        if 'default' in locations:
            # Check default location
            default_config = Path.home() / '.kube' / 'config'
            if default_config.exists() and default_config.is_file():
                print_message(f"Found kubeconfigs in default location: '{str(default_config)}'.")
                if str(default_config) not in kubeconfig_list:
                    kubeconfig_list.append(str(default_config))

        if 'kubeconfigs_location' in locations:
            # Check settings location
            if self.settings:
                kubeconfigs_location = self.settings.get('kubeconfigs_location')
                kubeconfigs = glob.glob(os.path.join(Path(kubeconfigs_location), "*.yaml"))
                if kubeconfigs:
                    print_message(f"Found kubeconfigs in settings kubeconfigs location: '{str(kubeconfigs_location)}'.")
                    for kubeconfig in kubeconfigs:
                        if kubeconfig not in kubeconfig_list:
                            kubeconfig_list.append(kubeconfig)

        return f'Available kubeconfigs ({len(kubeconfig_list)}):\n' + '\n'.join(kubeconfig_list) if pretty else kubeconfig_list

    def use(self, kubeconfig: str = None):
        """
        Method sets kubeconfig which will be used in future in kubectl, it sets selected kubeconfig to env variable.
        Usage:
            1. With prompt to select available kubeconfigs.
                kubeconfig use
            2. With specified kubeconfig.
                kubeconfig use --kubeconfig /path/to/kubeconfig
        """
        if not kubeconfig:
            kubeconfig_list = self.ls(pretty=False)
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        if kubeconfig:
            separator = ';' if os.name == 'nt' else ':'
            current_kubeconfig = os.environ.get('KUBECONFIG', '').split(separator)
            if kubeconfig not in current_kubeconfig:
                current_kubeconfig.append(kubeconfig)
            kubeconfig = current_kubeconfig
            set_env_variable('KUBECONFIG', separator.join(kubeconfig))
            print_message(f"KUBECONFIG variable successfully set to '{separator.join(kubeconfig)}'")

    def rm(self, kubeconfig: str = None):
        """
        Method removes kubeconfig from env variable KUBECONFIG.
        Usage:
            kubeconfig rm --kubeconfig /path/to/kubeconfig
        """
        if not kubeconfig:
            kubeconfig_list = self.ls(pretty=False, location='env')
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        if kubeconfig:
            separator = ';' if os.name == 'nt' else ':'
            current_kubeconfig = os.environ.get('KUBECONFIG', '').split(separator)
            if kubeconfig in current_kubeconfig:
                current_kubeconfig.remove(kubeconfig)
            kubeconfig = current_kubeconfig
            set_env_variable('KUBECONFIG', separator.join(kubeconfig))
            print_message(f"KUBECONFIG variable successfully set to '{separator.join(kubeconfig)}'")
