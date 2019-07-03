# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The task plugin.
"""

from cli.exceptions import CLIException
from cli.mesos import get_containers
from cli.plugins import PluginBase
from cli.util import Table

from cli.mesos import ContainerIO


PLUGIN_NAME = "agent-container"
PLUGIN_CLASS = "AgentContainer"

VERSION = "Mesos CLI Agent Container Plugin"

SHORT_HELP = "Interacts with the containers running in a Mesos agent"


class AgentContainer(PluginBase):
    """
    The agent container plugin.
    """

    COMMANDS = {
        "attach": {
            "arguments": ['<task-id>'],
            "flags": {
                "--no-stdin": "do not attach a stdin [default: False]"
            },
            "short_help": "Attach the CLI to the stdio of a running task",
            "long_help": """
                Attach the CLI to the stdio of a running task
                To detach type the sequence CTRL-p CTRL-q."""
        },
        "exec": {
            "arguments": ['<task-id>', '<command>', '[<args>...]'],
            "flags": {
                "-i --interactive" : "interactive [default: False]",
                "-t --tty": "tty [default: False]"
            },
            "short_help": "Execute commands in a task's container",
            "long_help": "Execute commands in a task's container"
        },
        "list": {
            "arguments": [],
            "flags": {
                "-a --all": "list all tasks, not only running [default: False]"
            },
            "short_help": "List all running tasks in a Mesos agent",
            "long_help": "List all running tasks in a Mesos agent"
        }
    }

    def attach(self, argv):
        """
        Attach the stdin/stdout/stderr of the CLI to the
        STDIN/STDOUT/STDERR of a running task.
        """
        try:
            agent = self.config.agent()
        except Exception as exception:
            raise CLIException("Unable to get leading master address: {error}"
                               .format(error=exception))

        container_io = ContainerIO(agent, argv["<task-id>"])
        return container_io.attach(argv["--no-stdin"])


    def exec(self, argv):
        """
        Launch a process inside a task's container.
        """
        try:
            agent = self.config.agent()
        except Exception as exception:
            raise CLIException("Unable to get leading master address: {error}"
                               .format(error=exception))

        container_io = ContainerIO(agent, argv["<task-id>"])
        return container_io.exec(argv["<command>"],
                                 argv["<args>"],
                                 argv["--interactive"],
                                 argv["--tty"])

    def list(self, argv):
        """
        List the tasks running in a agent by checking the /tasks endpoint.
        """
        # pylint: disable=unused-argument
        try:
            master = self.config.agent()
        except Exception as exception:
            raise CLIException("Unable to get leading master address: {error}"
                               .format(error=exception))

        try:
            containers = get_containers(master)
        except Exception as exception:
            raise CLIException("Unable to get containers from leading"
                               " master '{master}': {error}"
                               .format(master=master, error=exception))

        if not containers:
            print("There are no containers running in the agent.")
            return

        try:
            table = Table(["Container ID", "Executor ID", "Framework ID"])
            for container in containers:

                table.add_row([container["container_id"],
                               container["executor_id"],
                               container["framework_id"]])
        except Exception as exception:
            raise CLIException("Unable to build table of containers: {error}"
                               .format(error=exception))

        print(str(table))
