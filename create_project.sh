#!/bin/bash

# # 创建主项目目录
# mkdir -p digital_palace

# # 进入项目目录
# cd digital_palace

# 创建基础文件
touch README.md
touch requirements.txt

# 创建配置目录
mkdir -p config
touch config/__init__.py
touch config/settings.py

# 创建源代码目录结构
mkdir -p src/{core,generators,interfaces,utils}
touch src/__init__.py

# core模块
touch src/core/__init__.py
touch src/core/palace.py
touch src/core/memory.py
touch src/core/validator.py

# generators模块
touch src/generators/__init__.py
touch src/generators/text_gen.py
touch src/generators/image_gen.py
touch src/generators/model_gen.py

# interfaces模块
touch src/interfaces/__init__.py
touch src/interfaces/chat.py
touch src/interfaces/api.py

# utils模块
touch src/utils/__init__.py
touch src/utils/helpers.py

# 创建测试目录
mkdir -p tests/{test_core,test_generators,test_interfaces}
touch tests/__init__.py

# 创建数据目录
mkdir -p data/{images,models,text}

# 创建文档目录
mkdir -p docs
touch docs/api.md
touch docs/usage.md