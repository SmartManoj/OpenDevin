import os
import shutil
from unittest.mock import patch

import pytest

from opendevin.core.config import config
from opendevin.runtime.docker.exec_box import DockerExecBox
from opendevin.runtime.docker.local_box import LocalBox
from opendevin.runtime.docker.ssh_box import DockerSSHBox, split_bash_commands
from opendevin.runtime.plugins import AgentSkillsRequirement, JupyterRequirement


@pytest.fixture
def clean_up_workspace():
    folder = config.workspace_base
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    print('Cleaned up workspace.')


def test_env_vars():
    os.environ['SANDBOX_ENV_FOOBAR'] = 'BAZ'
    for box_class in [DockerSSHBox, DockerExecBox, LocalBox]:
        box = box_class()
        box.add_to_env('QUUX', 'abc"def')
        assert box._env['FOOBAR'] == 'BAZ'
        assert box._env['QUUX'] == 'abc"def'
        exit_code, output = box.execute('echo $FOOBAR $QUUX')
        assert exit_code == 0, 'The exit code should be 0.'
        assert output.strip() == 'BAZ abc"def', f'Output: {output} for {box_class}'


def test_split_commands():
    cmds = [
        'ls -l',
        'echo -e "hello\nworld"',
        """
echo -e 'hello it\\'s me'
""".strip(),
        """
echo \\
    -e 'hello' \\
    -v
""".strip(),
        """
echo -e 'hello\\nworld\\nare\\nyou\\nthere?'
""".strip(),
        """
echo -e 'hello
world
are
you\\n
there?'
""".strip(),
        """
echo -e 'hello
world "
'
""".strip(),
        """
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: busybox-sleep
spec:
  containers:
  - name: busybox
    image: busybox:1.28
    args:
    - sleep
    - "1000000"
EOF
""".strip(),
    ]
    joined_cmds = '\n'.join(cmds)
    split_cmds = split_bash_commands(joined_cmds)
    for s in split_cmds:
        print('\nCMD')
        print(s)
    cmds = [
        c.replace('\\\n', '') for c in cmds
    ]  # The function strips escaped newlines, but this shouldn't matter
    assert (
        split_cmds == cmds
    ), 'The split commands should be the same as the input commands.'


def test_ssh_box_run_as_devin():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [
            DockerSSHBox()
        ]:  # FIXME: permission error on mkdir test for exec box
            exit_code, output = box.execute('ls -l')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            assert output.strip() == 'total 0'

            exit_code, output = box.execute('ls -l')
            assert exit_code == 0, 'The exit code should be 0.'
            assert output.strip() == 'total 0'

            exit_code, output = box.execute('mkdir test')
            assert exit_code == 0, 'The exit code should be 0.'
            assert output.strip() == ''

            exit_code, output = box.execute('ls -l')
            assert exit_code == 0, 'The exit code should be 0.'
            assert (
                'opendevin' in output
            ), "The output should contain username 'opendevin'"
            assert 'test' in output, 'The output should contain the test directory'

            exit_code, output = box.execute('touch test/foo.txt')
            assert exit_code == 0, 'The exit code should be 0.'
            assert output.strip() == ''

            exit_code, output = box.execute('ls -l test')
            assert exit_code == 0, 'The exit code should be 0.'
            assert 'foo.txt' in output, 'The output should contain the foo.txt file'
            box.close()


def test_ssh_box_multi_line_cmd_run_as_devin(clean_up_workspace):
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox(), DockerExecBox()]:
            exit_code, output = box.execute('pwd && ls -l')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            expected_lines = ['/workspace', 'total 0']
            line_sep = '\r\n' if isinstance(box, DockerSSHBox) else '\n'
            assert output == line_sep.join(expected_lines), (
                'The output should be the same as the input for '
                + box.__class__.__name__
            )
            box.close()


def test_ssh_box_stateful_cmd_run_as_devin(clean_up_workspace):
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [
            DockerSSHBox()
        ]:  # FIXME: DockerExecBox() does not work with stateful commands
            exit_code, output = box.execute('mkdir test')
            assert exit_code == 0, 'The exit code should be 0.'
            assert output.strip() == ''

            exit_code, output = box.execute('cd test')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            assert output.strip() == '', (
                'The output should be empty for ' + box.__class__.__name__
            )

            exit_code, output = box.execute('pwd')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            assert output.strip() == '/workspace/test', (
                'The output should be /workspace for ' + box.__class__.__name__
            )
            box.close()


def test_ssh_box_failed_cmd_run_as_devin():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox(), DockerExecBox()]:
            exit_code, output = box.execute('non_existing_command')
            assert exit_code != 0, (
                'The exit code should not be 0 for a failed command for '
                + box.__class__.__name__
            )
            box.close()


def test_single_multiline_command():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox(), DockerExecBox()]:
            exit_code, output = box.execute('echo \\\n -e "foo"')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            if isinstance(box, DockerExecBox):
                assert output == 'foo', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            else:
                # FIXME: why is there a `>` in the output? Probably PS2?
                assert output == '> foo', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            box.close()


def test_multiline_echo():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox(), DockerExecBox()]:
            exit_code, output = box.execute('echo -e "hello\nworld"')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            if isinstance(box, DockerExecBox):
                assert output == 'hello\nworld', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            else:
                # FIXME: why is there a `>` in the output?
                assert output == '> hello\r\nworld', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            box.close()


def test_sandbox_whitespace():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox(), DockerExecBox()]:
            exit_code, output = box.execute('echo -e "\\n\\n\\n"')
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            if isinstance(box, DockerExecBox):
                assert output == '\n\n\n', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            else:
                assert output == '\r\n\r\n\r\n', (
                    'The output should be the same as the input for '
                    + box.__class__.__name__
                )
            box.close()


def test_sandbox_jupyter_plugin():
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox()]:
            box.init_plugins([JupyterRequirement])
            exit_code, output = box.execute('echo "print(1)" | execute_cli')
            print(output)
            assert exit_code == 0, (
                'The exit code should be 0 for ' + box.__class__.__name__
            )
            assert output == '1\r\n', (
                'The output should be the same as the input for '
                + box.__class__.__name__
            )
            box.close()


def _test_sandbox_jupyter_agentskills_fileop_pwd_impl(box):
    box.init_plugins([AgentSkillsRequirement, JupyterRequirement])
    exit_code, output = box.execute('mkdir test')
    print(output)
    assert exit_code == 0, 'The exit code should be 0 for ' + box.__class__.__name__

    exit_code, output = box.execute('echo "create_file(\'a.txt\')" | execute_cli')
    print(output)
    assert exit_code == 0, 'The exit code should be 0 for ' + box.__class__.__name__
    assert output.strip().split('\r\n') == (
        '[File: /workspace/a.txt (1 lines total)]\r\n' '1|\r\n' '[File a.txt created.]'
    ).strip().split('\r\n')

    exit_code, output = box.execute('cd test')
    print(output)
    assert exit_code == 0, 'The exit code should be 0 for ' + box.__class__.__name__

    exit_code, output = box.execute('echo "create_file(\'a.txt\')" | execute_cli')
    print(output)
    assert exit_code == 0, 'The exit code should be 0 for ' + box.__class__.__name__
    assert output.strip().split('\r\n') == (
        '[File: /workspace/test/a.txt (1 lines total)]\r\n'
        '1|\r\n'
        '[File a.txt created.]'
    ).strip().split('\r\n')

    exit_code, output = box.execute('rm -rf /workspace/*')
    assert exit_code == 0, 'The exit code should be 0 for ' + box.__class__.__name__
    box.close()


def test_sandbox_jupyter_agentskills_fileop_pwd(clean_up_workspace):
    with patch.object(config, 'run_as_devin', new='true'), patch.object(
        config, 'sandbox_type', new='ssh'
    ):
        for box in [DockerSSHBox()]:
            _test_sandbox_jupyter_agentskills_fileop_pwd_impl(box)


@pytest.mark.skipif(
    os.getenv('TEST_IN_CI') != 'true',
    reason='The unittest need to download image, so only run on CI',
)
def test_agnostic_sandbox_jupyter_agentskills_fileop_pwd():
    for base_sandbox_image in ['ubuntu:22.04', 'debian:11']:
        # get a temporary directory
        with patch.object(config, 'run_as_devin', new='true'), patch.object(
            config, 'sandbox_type', new='ssh'
        ), patch.object(config, 'sandbox_container_image', new=base_sandbox_image):
            for box in [DockerSSHBox()]:
                _test_sandbox_jupyter_agentskills_fileop_pwd_impl(box)
