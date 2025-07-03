#!/bin/bash

# --- 配置 ---
# 源目录：您日常开发的代码文件夹路径
SOURCE_DIR="/obs/users/yiyu/rekv_new_code"

# 目标父目录：包含 .git 文件夹的仓库的上一级目录
# 例如，如果你的仓库是 /home/ma-user/code/yiyu/rekv_new_code，这里就填 /home/ma-user/code/yiyu
GIT_PARENT_DIR="/home/ma-user/code/yiyu"

# 您的代码文件夹名称
REPO_NAME="rekv_new_code"

# --- 脚本主体 ---

# 设置-e，使得脚本在任何命令返回非零退出码时立即退出
set -e

# 检查是否提供了提交信息
if [ -z "$1" ]; then
  echo "错误：缺少提交信息。"
  echo "用法: $0 \"您的提交信息\""
  exit 1
fi

COMMIT_MESSAGE="$1"
DEST_DIR="$GIT_PARENT_DIR/$REPO_NAME"

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误：源目录 '$SOURCE_DIR' 不存在。"
    exit 1
fi

echo "--- 开始同步和推送任务 ---"

# 1. 移动代码到Git仓库位置
echo "1. 正在移动 '$SOURCE_DIR' 到 '$GIT_PARENT_DIR'..."
mv "$SOURCE_DIR" "$GIT_PARENT_DIR/"
echo "   移动完成。"

# 使用 trap 命令设置一个清理函数，确保无论脚本如何退出（成功或失败），代码都会被移回
# 注意：这需要手动进入目标目录再执行移动，因为失败时可能还停留在那个目录
function cleanup {
  echo ""
  echo "--- 开始清理 ---"
  # 检查代码是否还在目标位置，如果是则移回
  if [ -d "$DEST_DIR" ]; then
    echo "检测到代码仍在Git目录，正在移回原位..."
    mv "$DEST_DIR" "/obs/users/yiyu/"
    echo "代码已移回 '$SOURCE_DIR'。"
  else
    echo "代码已不在Git目录，无需移回。"
  fi
  echo "--- 清理完成 ---"
}

# 设置 trap，在脚本退出（EXIT）时调用 cleanup 函数
# trap cleanup EXIT # 如果您希望无论成功与否都自动移回，可以取消这一行的注释。目前的设计是成功后才移回。

# 2. 执行Git命令
echo "2. 进入Git仓库 '$DEST_DIR' 并执行Git命令..."
cd "$DEST_DIR"

echo "   - git add ."
git add .

echo "   - git commit -m \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"

echo "   - git push"
git push

echo "   Git推送成功！"

# 3. 将代码移回原处
echo "3. 正在将代码移回原位 '$SOURCE_DIR'..."
# 先返回上一级目录，再执行移动操作
cd ..
mv "$REPO_NAME" "/obs/users/yiyu/"
echo "   移动完成。"

echo ""
echo "--- 所有操作成功完成！ ---"