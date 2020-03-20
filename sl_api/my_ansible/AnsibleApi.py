import json
import os
import shutil

from ansible.errors import AnsibleError, AnsibleConnectionFailure
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

from optparse import Values

from utils.settings import envs





class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        # super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}


    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result


    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result



class AnsibleApi(object):
    def __init__(self):
        env = os.environ.get("FLASK_ENV") or "default"
        config = envs.get(env)
        inventory_file=config.ansible_host_file
        self.options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                    'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                    'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
                    'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                    'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                    'inventory':inventory_file,
                    'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                    'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None, 'listtasks': None,
                    'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
        self.ops = Values(self.options)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=inventory_file)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host, command):

        play_source = dict(
                name="Ansible Play",
                hosts=host,
                gather_facts='no',
                tasks=[dict(action=dict(module='shell', args=command), register='shell_out')]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.ops,
                    passwords=self.passwords,
                    stdout_callback=self.results_callback,
                    # run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

        result_raw = {'success': {}, 'failed': {}, 'unreachable': {},}

        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result
        result_info = json.dumps(result_raw, indent=4)


        return result_info




