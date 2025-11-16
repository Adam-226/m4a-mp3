#!/usr/bin/env python3
"""
音频格式批量转换工具
支持将.m4a文件批量转换为.mp3或.wav格式
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_audio(input_file, output_format='mp3', output_dir=None, quality='high'):
    """
    转换单个音频文件
    
    参数:
        input_file: 输入文件路径
        output_format: 输出格式 ('mp3' 或 'wav')
        output_dir: 输出目录，如果为None则使用输入文件所在目录
        quality: 音质设置 ('high', 'medium', 'low')
    """
    input_path = Path(input_file)
    
    # 确定输出目录
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = input_path.parent
    
    # 生成输出文件名
    output_file = out_dir / f"{input_path.stem}.{output_format}"
    
    # 构建ffmpeg命令
    cmd = ['ffmpeg', '-i', str(input_path)]
    
    # 根据格式和质量设置参数
    if output_format == 'mp3':
        if quality == 'high':
            cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '320k'])
        elif quality == 'medium':
            cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '192k'])
        else:  # low
            cmd.extend(['-codec:a', 'libmp3lame', '-b:a', '128k'])
    elif output_format == 'wav':
        cmd.extend(['-codec:a', 'pcm_s16le'])
    
    cmd.extend(['-y', str(output_file)])  # -y 自动覆盖已存在的文件
    
    try:
        # 执行转换
        result = subprocess.run(cmd, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              check=True)
        return True, output_file
    except subprocess.CalledProcessError as e:
        return False, str(e)


def batch_convert(input_dir, output_format='mp3', output_dir=None, quality='high', recursive=False):
    """
    批量转换文件夹中的所有.m4a文件
    
    参数:
        input_dir: 输入目录
        output_format: 输出格式 ('mp3' 或 'wav')
        output_dir: 输出目录
        quality: 音质设置
        recursive: 是否递归搜索子文件夹
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ 错误: 目录不存在: {input_dir}")
        return
    
    # 查找所有.m4a文件
    if recursive:
        m4a_files = list(input_path.rglob('*.m4a'))
    else:
        m4a_files = list(input_path.glob('*.m4a'))
    
    if not m4a_files:
        print(f"⚠️  在目录 {input_dir} 中未找到.m4a文件")
        return
    
    print(f"📁 找到 {len(m4a_files)} 个.m4a文件")
    print(f"🎵 输出格式: {output_format.upper()}")
    print(f"🎚️  音质设置: {quality}")
    print(f"{'='*60}")
    
    success_count = 0
    fail_count = 0
    
    for idx, m4a_file in enumerate(m4a_files, 1):
        print(f"\n[{idx}/{len(m4a_files)}] 正在转换: {m4a_file.name}")
        
        success, result = convert_audio(m4a_file, output_format, output_dir, quality)
        
        if success:
            print(f"✅ 成功: {result}")
            success_count += 1
        else:
            print(f"❌ 失败: {result}")
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 转换完成!")
    print(f"   ✅ 成功: {success_count} 个文件")
    print(f"   ❌ 失败: {fail_count} 个文件")


def main():
    parser = argparse.ArgumentParser(
        description='批量转换.m4a音频文件为.mp3或.wav格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 转换当前目录下的所有.m4a文件为mp3
  python convert_audio.py .
  
  # 转换指定目录下的文件为wav格式
  python convert_audio.py /path/to/music --format wav
  
  # 转换并保存到指定目录
  python convert_audio.py /path/to/music --output /path/to/output
  
  # 递归转换所有子文件夹中的文件
  python convert_audio.py /path/to/music --recursive
  
  # 指定音质（high/medium/low）
  python convert_audio.py /path/to/music --quality high
        """
    )
    
    parser.add_argument('input_dir', 
                       help='包含.m4a文件的输入目录')
    parser.add_argument('-f', '--format', 
                       choices=['mp3', 'wav'], 
                       default='mp3',
                       help='输出格式 (默认: mp3)')
    parser.add_argument('-o', '--output',
                       help='输出目录 (默认: 与输入文件相同目录)')
    parser.add_argument('-q', '--quality',
                       choices=['high', 'medium', 'low'],
                       default='high',
                       help='音质设置，仅对mp3有效 (默认: high - 320k)')
    parser.add_argument('-r', '--recursive',
                       action='store_true',
                       help='递归搜索子文件夹')
    
    args = parser.parse_args()
    
    # 检查ffmpeg
    print("🔍 检查ffmpeg...")
    if not check_ffmpeg():
        print("❌ 错误: 未找到ffmpeg，请先安装ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Ubuntu: sudo apt-get install ffmpeg")
        print("   Windows: 从 https://ffmpeg.org/download.html 下载")
        sys.exit(1)
    print("✅ ffmpeg已就绪\n")
    
    # 执行批量转换
    batch_convert(
        args.input_dir,
        args.format,
        args.output,
        args.quality,
        args.recursive
    )


if __name__ == '__main__':
    main()

