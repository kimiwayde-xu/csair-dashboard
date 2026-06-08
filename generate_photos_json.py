#!/usr/bin/env python3
"""
自动扫描 photos/ 文件夹，生成 photos.json
使用方法：python3 generate_photos_json.py
"""

import json
import os
from pathlib import Path
from datetime import datetime

# 路径设置
SCRIPT_DIR = Path(__file__).parent
DEPLOY_DIR = SCRIPT_DIR / "vercel-deploy"
PHOTOS_DIR = DEPLOY_DIR / "photos"
OUTPUT_FILE = DEPLOY_DIR / "photos.json"

def generate_photos_json():
    """扫描 photos/ 文件夹，生成 photos.json"""
    
    if not PHOTOS_DIR.exists():
        print(f"❌ 照片文件夹不存在: {PHOTOS_DIR}")
        return
    
    # 支持的图片格式
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic'}
    
    # 扫描照片
    photos = []
    
    for file_path in PHOTOS_DIR.iterdir():
        # 跳过 macOS 资源分支文件
        if file_path.name.startswith('.'):
            continue
        
        # 跳过非图片文件
        if file_path.suffix.lower() not in valid_extensions:
            continue
        
        # 获取文件信息
        stat = file_path.stat()
        
        photos.append({
            "filename": file_path.name,
            "path": f"photos/{file_path.name}",
            "title": file_path.stem,
            "description": "",
            "size": stat.st_size,
            "modified": str(stat.st_mtime)
        })
    
    # 按修改时间排序（最新的在前）
    photos.sort(key=lambda x: x['modified'], reverse=True)
    
    # 生成 JSON
    output = {
        "total": len(photos),
        "photos": photos
    }
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成 photos.json")
    print(f"   照片总数: {len(photos)}")
    print(f"   输出文件: {OUTPUT_FILE}")
    
    # Git 提交
    os.chdir(DEPLOY_DIR)
    
    import subprocess
    
    # Git add - 同时添加 photos.json 和 photos/ 文件夹里的新照片
    subprocess.run(['git', 'add', 'photos.json', 'photos/'], check=True)
    
    # Git commit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = subprocess.run(
        ['git', 'commit', '-m', f'update: 更新照片列表 {timestamp}'],
        capture_output=True
    )
    
    if result.returncode == 0:
        # Git push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print(f"✅ 已推送到 GitHub")
    else:
        print("ℹ️ 没有新的照片变化")

if __name__ == '__main__':
    generate_photos_json()
