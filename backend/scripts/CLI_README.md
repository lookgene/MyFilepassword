# ZIP Cracker CLI 使用说明

## 简介

这是从图形界面版本提取的命令行密码破解工具，支持多种压缩文件和加密文档格式的密码破解。

## 支持的文件格式

- **压缩文件**: ZIP, RAR, 7Z
- **Office文档**: DOC, DOCX, XLS, XLSX, PPT, PPTX
- **PDF文档**: PDF
- **密码管理器**: KDB, KDBX (KeePass)
- **加密文件**: GPG, PGP
- **系统加密**: VHD, VHDY (BitLocker)
- **网络抓包**: HCCAP, HCCAPX (WiFi)
- **SSH密钥**: PEM, KEY, PPK
- **系统文件**: shadow (Unix Shadow)

## 安装要求

1. **Python 3.7+**
2. **必要工具** (需要放在程序目录或系统PATH中):
   - `hashcat.exe` - 主要破解工具
   - `rar2john.exe` - RAR文件哈希提取
   - `zip2john.exe` - ZIP文件哈希提取

3. **可选工具** (用于支持更多格式):
   - `7z2john.pl` - 7Z文件支持
   - `office2john.py` - Office文档支持
   - `pdf2john.pl` - PDF文件支持
   - `ssh2john.py` - SSH密钥支持
   - `keepass2john.exe` - KeePass支持
   - `gpg2john.exe` - GPG文件支持
   - `bitlocker2john.exe` - BitLocker支持
   - `hccap2john.exe` - WiFi抓包支持

## 使用方法

### 基本用法

```bash
# 直接运行Python脚本
python zip_cracker_cli.py file.zip

# 或使用入口脚本
python cli_main.py file.zip

# 或使用批处理文件 (Windows)
zip_cracker.bat file.zip
```

### 高级选项

```bash
# 使用GPU模式破解 (如果有NVIDIA显卡)
python zip_cracker_cli.py file.docx --mode gpu

# 显示详细输出
python zip_cracker_cli.py file.rar --verbose

# 查看帮助信息
python zip_cracker_cli.py --help
```

### 命令行参数

- `file`: 要破解的文件路径 (必需)
- `--mode`: 破解模式，可选 `cpu` 或 `gpu` (默认: cpu)
- `-v, --verbose`: 显示详细输出
- `-h, --help`: 显示帮助信息

## 破解流程

工具采用三阶段破解策略：

1. **字典攻击**: 使用内置的常见密码字典 (`rockyou.txt`)
2. **数字组合**: 尝试6位数字组合
3. **暴力破解**: 尝试1-8位任意字符组合

## 使用示例

### 破解ZIP文件
```bash
python zip_cracker_cli.py protected.zip
```

### 破解Word文档 (GPU模式)
```bash
python zip_cracker_cli.py document.docx --mode gpu
```

### 破解RAR文件
```bash
python zip_cracker_cli.py archive.rar --verbose
```

### 破解PDF文件
```bash
python zip_cracker_cli.py encrypted.pdf
```

## 注意事项

1. **工具依赖**: 确保所有必要的工具文件都存在且可访问
2. **权限要求**: 某些文件可能需要管理员权限
3. **时间消耗**: 暴力破解可能需要很长时间，取决于密码复杂度
4. **GPU支持**: GPU模式需要NVIDIA显卡和CUDA支持
5. **临时文件**: 程序会在当前目录创建临时文件，完成后自动清理

## 故障排除

### 常见错误

1. **"找不到工具"**: 检查工具文件是否在程序目录或系统PATH中
2. **"不支持的文件格式":** 检查文件扩展名是否在支持列表中
3. **"无法提取哈希值":** 文件可能损坏或不支持的加密方式
4. **"破解失败"**: 密码可能太复杂，尝试使用更大的字典文件

### 解决方案

1. **检查工具路径**:
   - 将工具文件放在程序目录下
   - 或将工具目录添加到系统PATH环境变量

2. **更新工具版本**:
   - 确保使用最新版本的hashcat和John工具

3. **增加字典**:
   - 替换 `rockyou.txt` 为更大的密码字典文件

## 性能优化

- **GPU加速**: 如果有NVIDIA显卡，使用 `--mode gpu` 可以大幅提升破解速度
- **内存设置**: 根据系统内存调整hashcat的内存使用
- **并发数**: GPU模式下可以调整hashcat的并发数设置

## 法律声明

本工具仅供学习和合法的安全测试使用。请勿用于非法破解他人文件。使用本工具时请确保你有权破解目标文件。

## 技术支持

如遇到问题，请检查：
1. Python版本是否正确
2. 依赖工具是否完整
3. 文件权限是否足够
4. 系统资源是否充足