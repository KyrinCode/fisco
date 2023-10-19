# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export PATH

# added by Kyrin 2021.10
# setup proxy with ClashX or Squidman
# set proxy
function setproxy() {
        agent_ip=http://10.21.4.216:8081
        export all_proxy=$agent_ip
}
# unset proxy
function unsetproxy() {
    unset all_proxy
}

# added by Kyrin 2021.11
# show/kill processes by a keyword
function showps() {
        key=$1
        ps -ef | grep $key | grep -v grep
}
function killps() {
        key=$1
        ps -ef | grep $key | grep -v grep | cut -c 9-15 | xargs sudo kill -9
}

conda activate fisco