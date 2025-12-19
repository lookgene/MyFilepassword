#!/usr/bin/env python3
"""
ZIP Cracker CLI - 命令行版本的密码破解工具
从图形界面版本提取核心功能
"""

import os
import sys
import time
import argparse
import subprocess
import re
from utils import get_current_dir, check_cuda_support, find_tool, get_file_format, dict_file


class CrackerCLI:
    def __init__(self, file_path, mode="cpu"):
        self.file_path = file_path
        self.current_dir = get_current_dir()
        self.is_running = True
        self.enable_cuda = check_cuda_support()
        self.max_password_length = 12
        self.timeout_seconds = 30
        self.file_format = get_file_format(file_path)
        self.mode = mode
        self.tool_paths = {}
        self.hash_patterns = {
            "rar": re.compile(r"\$rar5\$.*"),
            "zip": re.compile(r"\$zip2\$.*"),
            "7z": re.compile(r"\$7z\$.*"),
            "word": re.compile(r"\$office\$.*?\*.*"),
            "pdf": re.compile(r"\$pdf\$.*"),
        }

    def log(self, message):
        """输出日志信息"""
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")

    def create_temp_file(self, hash_value):
        """创建临时哈希文件"""
        try:
            temp_hash_file = os.path.join(self.current_dir, "temp_hash.txt")
            with open(temp_hash_file, "w", encoding="utf-8") as f:
                f.write(hash_value)
            return temp_hash_file
        except Exception as e:
            raise Exception(f"创建临时文件失败: {str(e)}")

    def get_algorithm_id_bk(self, hash_value):
        """根据文件格式和哈希值返回对应的算法ID"""
        # 特定格式检测
        if "$rar5$" in hash_value:
            return 13000  # RAR5
        elif "$rar3$" in hash_value:
            return 12500  # RAR3
        elif "$pkzip2$" in hash_value:
            return 17200  #
        elif "$oldoffice$" in hash_value:
            return 9700  #
        elif " $zip2$" in hash_value:
            return 13600   # WinZip

        # 其他格式的算法ID映射
        algo_map = {
            "zip": 13600,  # WinZip
            "rar": 13000,  # RAR5 (默认)
            "7z": 11600,  # 7-Zip
            "pdf": 10500,  # PDF 1.7 Level 8
            "word": 9400,  # MS Office 2007
            "excel": 9400,  # MS Office 2007
            "powerpoint": 9400,  # MS Office 2007
        }

        algo_id = algo_map.get(self.file_format)
        if not algo_id:
            raise Exception(f"无法识别文件格式: {self.file_format}")

        self.log(f"使用算法ID: {algo_id}")
        return algo_id

    def get_algorithm_id(self, hash_str):
        # 1. 基础前缀直接返回
        if hash_str.startswith("$rar5$"):
            return 13000
        if hash_str.startswith("$RAR3$"):
            return 12500
        if hash_str.startswith("$zip2$"):
            return 13600
        if hash_str.startswith("$7z$"):
            return 11600

        # 2. 复杂前缀分析
        
        # --- PDF 分析 ---
        if hash_str.startswith("$pdf$"):
            # 移除前缀 "$pdf$" 后按 "*" 分割
            parts = hash_str[5:].split("*")
            v_version = parts[0]
            r_revision = parts[1]
            
            if v_version == "1":
                return 10400
            elif v_version in ["2", "4"]:
                return 10500 # 或者是 25400，视具体需求定
            elif v_version == "5":
                if r_revision == "5":
                    return 10600
                elif r_revision == "6":
                    return 10700
        
        # --- Office 分析 ---
        if hash_str.startswith("$office$"):
            # 检查是否包含特定版本字符串
            if "*2007*" in hash_str:
                return 9400
            if "*2010*" in hash_str:
                return 9500
            if "*2013*" in hash_str:
                return 9600
            if "$2016$" in hash_str or "2016" in hash_str: # 2016结构比较特殊
                return 25300

        # --- Old Office 分析 ---
        if hash_str.startswith("$oldoffice$"):
            # 获取 $oldoffice$ 后的第一个字符
            type_code = hash_str.split("$")[2][0] 
            if type_code in ["0", "1"]:
                return 9700
            if type_code in ["3", "4"]:
                return 9800

        # --- PKZIP 分析 ---
        if hash_str.startswith("$pkzip2$"):
            parts = hash_str[8:].split("*") # 移除 $pkzip2$
            chunk_count = parts[0]
            if chunk_count == "1":
                return 17200
            if chunk_count == "3":
                return 17220

    def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            temp_hash_file = os.path.join(self.current_dir, "temp_hash.txt")
            if os.path.exists(temp_hash_file):
                os.remove(temp_hash_file)
        except Exception as e:
            self.log(f"清理临时文件时出错: {str(e)}")

    def extract_hash(self):
        tool_map = {
            "rar": "rar2john.exe",
            "zip": "zip2john.exe",
            "7z": "7z2john.pl",
            "word": "office2john.py",
            "excel": "office2john.py",
            "powerpoint": "office2john.py",
            "pdf": "pdf2john.pl",
            "ssh": "ssh2john.py",
            "keepass": "keepass2john.exe",
            "gpg": "gpg2john.exe",
            "bitlocker": "bitlocker2john.exe",
            "wifi": "hccap2john.exe",
        }

        tool_name = tool_map.get(self.file_format)
        if not tool_name:
            raise Exception(f"不支持的文件格式: {self.file_format}")

        tool_path = find_tool(tool_name, self.tool_paths)
        if not tool_path:
            raise Exception(f"找不到工具: {tool_name}")

        try:
            # 特殊处理unshadow工具，它需要两个文件参数
            if tool_name == "unshadow.exe":
                passwd_file = self.file_path.replace("shadow", "passwd")
                if not os.path.exists(passwd_file):
                    raise Exception("处理shadow文件需要对应的passwd文件")
                cmd = [tool_path, passwd_file, self.file_path]
            else:
                cmd = [tool_path, self.file_path]

            if tool_name in ["7z2john.pl", "pdf2john.pl"]:
                cmd.insert(0, "perl")
            elif tool_name == "office2john.py":
                cmd.insert(0, "python")

            self.log(f"开始获取hash值，执行命令: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                errors="ignore",
                encoding="utf-8",
            )

            if result.returncode != 0:
                error_msg = self.parse_tool_error(result.stderr)
                raise Exception(error_msg)

            self.log(f"hash值提取完成,值如下: {result.stdout}")
            return self.parse_hash_output(result.stdout)
        except subprocess.TimeoutExpired:
            raise Exception("哈希提取超时，可能遇到大文件或复杂加密")

    def parse_hash_output(self, output):
        """解析哈希输出"""
        if not output:
            raise Exception("无法提取哈希值")

        hash_lines = [line.strip() for line in output.split("\n") if line.strip()]
        if not hash_lines:
            raise Exception("提取的哈希值为空")

        raw_hash = hash_lines[-1]
        hash_prefixes = [
            "$rar5$", "$rar3$", "$zip2$", "$pkzip2$", "$7z$", "$office$",
            "$oldoffice$", "$pdf$", "$ssh$", "$keepass$", "$gpg$",
            "$bitlocker$", "$WPAPSK$", "$vnc$",
        ]

        if ":" in raw_hash:
            parts = raw_hash.split(":")
            for part in parts:
                for prefix in hash_prefixes:
                    if part.startswith(prefix):
                        return part
            return parts[-1]
        return raw_hash

    def parse_tool_error(self, stderr):
        """解析工具错误输出"""
        if not stderr:
            return "未知错误"
        return stderr.strip()

    def process_output(self, proc):
        """处理破解进程的输出"""
        try:
            while True:
                line = proc.stdout.readline()
                if not line:
                    break

                line = line.strip()
                if line:
                    self.log(line)

                # 检测错误信息
                if "ERROR" in line.upper() or "FAILED" in line.upper():
                    self.log(f"检测到错误: {line}")

                # 处理成功信息
                if (":" in line and not line.startswith("[") and
                    not line.startswith("*") and not line.startswith("Approaching")):
                    try:
                        # 格式应该是 hash:password
                        hash_part, password = line.split(":", 1)
                        if hash_part.startswith("$"):
                            self.is_running = False
                            return password.strip()
                    except Exception as e:
                        self.log(f"解析结果时出错: {str(e)}")
        except Exception as e:
            self.log(f"处理输出时出错: {str(e)}")
        finally:
            proc.wait()
        return None

    def check_tools(self):
        """检查必要的工具文件是否存在"""
        required_tools = ["hashcat.exe", "rar2john.exe", "zip2john.exe"]
        optional_tools = [
            "7z2john.pl", "office2john.py", "pdf2john.pl", "ssh2john.py",
            "keepass2john.exe", "gpg2john.exe", "bitlocker2john.exe", "hccap2john.exe"
        ]

        missing_tools = []

        for tool in required_tools:
            tool_path = find_tool(tool)
            if not tool_path:
                missing_tools.append(tool)
                self.log(f"警告: 找不到必要工具 {tool}")
            else:
                self.log(f"找到工具: {tool} 位置: {tool_path}")

        for tool in optional_tools:
            tool_path = find_tool(tool)
            if not tool_path:
                self.log(f"提示: 找不到可选工具 {tool}，相关格式文件将无法处理")
            else:
                self.log(f"找到工具: {tool} 位置: {tool_path}")

        return len(missing_tools) == 0

    def crack(self):
        """执行破解过程"""
        try:
            self.log("=== ZIP Cracker CLI 开始破解 ===")
            self.log(f"目标文件: {self.file_path}")
            self.log(f"文件格式: {self.file_format.upper()}")
            self.log(f"破解模式: {self.mode.upper()}")

            # 检查工具
            self.log("检查必要工具...")
            if not self.check_tools():
                raise Exception("缺少必要工具，无法开始破解")

            # 1. 提取哈希
            self.log("步骤1: 提取哈希值")
            hash_value = self.extract_hash()
            if hash_value:
                self.log(f"哈希值: {hash_value}")
            else:
                raise Exception("无法提取哈希值")

            # 2. 获取算法编号
            self.log("步骤2: 识别哈希类型")
            algo_id = self.get_algorithm_id(hash_value)
            if not algo_id:
                raise Exception("无法识别算法类型")
            self.log(f"算法编号: {algo_id}")

            # 3. 创建临时文件
            temp_hash_file = self.create_temp_file(hash_value)

            # 4. 调用Hashcat破解
            self.log("步骤3: 开始破解")
            hashcat_path = find_tool("hashcat.exe", self.tool_paths)
            if not hashcat_path:
                raise Exception("找不到hashcat工具")

            hashcat_dir = os.path.dirname(hashcat_path)

            # 阶段1: 6位数字组合
            if self.is_running:
                num_cmd = (
                    f'cd /d "{hashcat_dir}" && hashcat.exe -m {algo_id} -a 3 "{temp_hash_file}" '
                    f'"?d?d?d?d?d?d" --potfile-disable --session=crack_session --restore-disable '
                    f"--status --status-timer=1 --force"
                )

                self.log("第1阶段: 尝试6位数字组合")
                self.log(f"执行命令: {num_cmd}")

                proc = subprocess.Popen(
                    num_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                password = self.process_output(proc)
                if password:
                    return password
            # 阶段2: 字典模式
            dict_cmd = (
                f'cd /d "{hashcat_dir}" && hashcat.exe -m {algo_id} -a 0 "{temp_hash_file}" '
                f'"{dict_file}" --potfile-disable --session=crack_session --restore-disable '
                f"--status --status-timer=1 --force"
            )

            self.log("第2阶段: 尝试常见密码")
            self.log(f"执行命令: {dict_cmd}")

            proc = subprocess.Popen(
                dict_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            password = self.process_output(proc)
            if password:
                return password

            

            # 阶段3: 暴力破解 1-8位任意字符
            if self.is_running:
                brute_cmd = (
                    f'cd /d "{hashcat_dir}" && hashcat.exe -m {algo_id} -a 3 "{temp_hash_file}" '
                    f'--increment --increment-min=1 --increment-max=8 "?a?a?a?a?a?a?a?a" '
                    f"--potfile-disable --session=crack_session --restore-disable "
                    f"--status --status-timer=1 --force"
                )

                self.log("第3阶段: 尝试1-8位任意字符组合")
                self.log(f"执行命令: {brute_cmd}")

                proc = subprocess.Popen(
                    brute_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                password = self.process_output(proc)
                if password:
                    return password

            return None

        except Exception as e:
            self.log(f"错误: {str(e)}")
            return None
        finally:
            self.cleanup_temp_files()


def main():
    parser = argparse.ArgumentParser(
        description="ZIP Cracker CLI - 命令行密码破解工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的文件格式:
  ZIP, RAR, 7Z, DOC, DOCX, XLS, XLSX, PPT, PPTX, PDF
  KDB, KDBX (KeePass), GPG, PGP, VHD, VHDY (BitLocker)
  HCCAP, HCCAPX (WiFi), PEM, KEY, PPK (SSH), shadow (Unix Shadow)

示例:
  %(prog)s file.zip                    # 破解ZIP文件
  %(prog)s file.docx --mode gpu        # 使用GPU模式破解Word文档
  %(prog)s file.rar --verbose          # 显示详细输出
        """
    )

    parser.add_argument("file", help="要破解的文件路径")
    parser.add_argument("--mode", choices=["cpu", "gpu"], default="cpu",
                       help="破解模式 (默认: cpu)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="显示详细输出")

    args = parser.parse_args()

    # 验证文件存在
    if not os.path.exists(args.file):
        print(f"错误: 文件 '{args.file}' 不存在")
        sys.exit(1)

    if not os.path.isfile(args.file):
        print(f"错误: '{args.file}' 不是文件")
        sys.exit(1)

    # 检查文件格式
    file_format = get_file_format(args.file)
    if file_format == "unknown":
        print(f"错误: 不支持的文件格式")
        sys.exit(1)

    try:
        # 创建破解器实例
        cracker = CrackerCLI(args.file, args.mode)

        # 显示信息
        print("=" * 50)
        print("ZIP Cracker CLI")
        print("=" * 50)
        print(f"目标文件: {args.file}")
        print(f"文件格式: {file_format.upper()}")
        print(f"破解模式: {args.mode.upper()}")
        print("=" * 50)

        # 开始破解
        start_time = time.time()
        password = cracker.crack()
        end_time = time.time()

        # 显示结果
        elapsed_time = end_time - start_time
        print("\n" + "=" * 50)
        print("破解完成")
        print("=" * 50)
        print(f"用时: {elapsed_time:.2f} 秒")

        if password:
            print(f"✅ 破解成功!")
            print(f"🔑 密码: {password}")
            sys.exit(0)
        else:
            print("❌ 破解失败")
            print("提示: 尝试使用更大的字典文件或增加破解时间")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断破解过程")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()