python-boost
failed 20 minutes ago in 3s
Search logs
1s
Current runner version: '2.329.0'
Runner Image Provisioner
Operating System
Runner Image
GITHUB_TOKEN Permissions
Secret source: Actions
Prepare workflow directory
Prepare all required actions
Getting action download info
Download action repository 'actions/checkout@v4' (SHA:08eba0b27e820071cde6df949e0beb9ba4906955)
Download action repository 'actions/setup-python@v4' (SHA:7f4fc3e22c37d6ff65e88745f38bd3157c663f7c)
Complete job name: python-boost
0s
Run actions/checkout@v4
Syncing repository: Wegnernando94/wegnernando94
Getting Git version info
Temporarily overriding HOME='/home/runner/work/_temp/0e8a317f-5521-44b4-98ec-a99a5a0e8192' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/wegnernando94/wegnernando94
Deleting the contents of '/home/runner/work/wegnernando94/wegnernando94'
Initializing the repository
Disabling automatic garbage collection
Setting up auth
Fetching the repository
Determining the checkout info
/usr/bin/git sparse-checkout disable
/usr/bin/git config --local --unset-all extensions.worktreeConfig
Checking out the ref
/usr/bin/git log -1 --format=%H
1004305833a42687f5c8d973ae778b7f2ccaccd7
1s
Run actions/setup-python@v4
Installed versions
0s
Run git config --local user.email "bellacandy5900g@gmail.com"
0s
Run python boost-stats.py
python: can't open file '/home/runner/work/wegnernando94/wegnernando94/boost-stats.py': [Errno 2] No such file or directory
Error: Process completed with exit code 2.
0s
0s
Post job cleanup.
/usr/bin/git version
git version 2.51.2
Temporarily overriding HOME='/home/runner/work/_temp/92e06c89-1ad5-4070-ab5f-7299ad0e08ca' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/wegnernando94/wegnernando94
/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
http.https://github.com/.extraheader
/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
