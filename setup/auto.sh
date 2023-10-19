#!/usr/bin/env sh

# echo -e "\033[32m 绿色字 \033[0m"

# 确保脚本抛出遇到的错误
set -e

# tar -xzf ./bin/fisco-bcos.tar.gz

# 生成区块链配置文件
cat > ipconf << EOF
$1:$2 agencyA 1
$1:$2 agencyB 2
EOF

# 构建节点配置文件夹
bash build_chain.sh -f ipconf -p 30300,20200,8545 -i -e ./fisco-bcos

# 启动所有节点
cd nodes/$1
bash start_all.sh

# 当前自动生成的sdk属于agencyA
mv sdk sdk_agencyA

# 为其余机构生成sdk
cp ../../gen_node_cert.sh ./
bash gen_node_cert.sh -c ../cert/agencyB -o sdk_agencyB -s