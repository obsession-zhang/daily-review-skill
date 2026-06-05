#!/usr/bin/env python3
"""
Version Manager
复盘报告版本存档与回滚
"""

import os
import shutil
import json
from datetime import datetime
from typing import List, Optional, Dict


class VersionManager:
    """版本管理器"""

    def __init__(self, review_dir: str = "./skills/daily-review/review_history",
                 archive_dir: str = "./skills/daily-review/archive"):
        self.review_dir = review_dir
        self.archive_dir = archive_dir
        os.makedirs(archive_dir, exist_ok=True)

    def archive_version(self, date: str, reason: str = "auto") -> str:
        """归档指定日期的复盘报告"""
        # 查找文件
        md_file = None
        yaml_file = None

        for f in os.listdir(self.review_dir):
            if f.startswith(f"review_{date}"):
                if f.endswith(".md"):
                    md_file = f
                elif f.endswith(".yaml"):
                    yaml_file = f

        if not md_file:
            return f"Error: No review found for {date}"

        # 创建归档目录
        archive_path = os.path.join(self.archive_dir, date)
        os.makedirs(archive_path, exist_ok=True)

        # 生成版本号
        version = datetime.now().strftime("%H%M%S")

        # 复制文件
        if md_file:
            shutil.copy2(
                os.path.join(self.review_dir, md_file),
                os.path.join(archive_path, f"{md_file}.{version}")
            )

        if yaml_file:
            shutil.copy2(
                os.path.join(self.review_dir, yaml_file),
                os.path.join(archive_path, f"{yaml_file}.{version}")
            )

        # 记录元数据
        meta = {
            "date": date,
            "version": version,
            "archived_at": datetime.now().isoformat(),
            "reason": reason,
            "files": [md_file, yaml_file]
        }

        with open(os.path.join(archive_path, f"meta_{version}.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        return f"Archived {date} version {version} (reason: {reason})"

    def list_versions(self, date: str) -> List[Dict]:
        """列出指定日期的所有版本"""
        archive_path = os.path.join(self.archive_dir, date)

        if not os.path.exists(archive_path):
            return []

        versions = []
        for f in os.listdir(archive_path):
            if f.startswith("meta_") and f.endswith(".json"):
                with open(os.path.join(archive_path, f), "r", encoding="utf-8") as file:
                    meta = json.load(file)
                    versions.append(meta)

        versions.sort(key=lambda x: x["version"], reverse=True)
        return versions

    def rollback(self, date: str, version: str) -> str:
        """回滚到指定版本"""
        archive_path = os.path.join(self.archive_dir, date)

        if not os.path.exists(archive_path):
            return f"Error: No archive found for {date}"

        # 先归档当前版本
        self.archive_version(date, reason="rollback")

        # 找到指定版本的文件
        md_source = None
        yaml_source = None

        for f in os.listdir(archive_path):
            if f.endswith(f".{version}"):
                if f.endswith(".md"):
                    md_source = f
                elif f.endswith(".yaml"):
                    yaml_source = f

        if not md_source:
            return f"Error: Version {version} not found for {date}"

        # 复制回主目录
        if md_source:
            # 找到主目录中的当前文件
            for f in os.listdir(self.review_dir):
                if f.startswith(f"review_{date}") and f.endswith(".md"):
                    shutil.copy2(
                        os.path.join(archive_path, md_source),
                        os.path.join(self.review_dir, f)
                    )
                    break

        if yaml_source:
            for f in os.listdir(self.review_dir):
                if f.startswith(f"review_{date}") and f.endswith(".yaml"):
                    shutil.copy2(
                        os.path.join(archive_path, yaml_source),
                        os.path.join(self.review_dir, f)
                    )
                    break

        return f"Rolled back {date} to version {version}"

    def list_all_dates(self) -> List[str]:
        """列出所有有归档的日期"""
        dates = []
        for d in os.listdir(self.archive_dir):
            if os.path.isdir(os.path.join(self.archive_dir, d)):
                dates.append(d)
        dates.sort(reverse=True)
        return dates


def main():
    """CLI 入口"""
    manager = VersionManager()
    print("Version Manager v1.0.0")
    print(f"Archive directory: {manager.archive_dir}")

    dates = manager.list_all_dates()
    print(f"Archived dates: {len(dates)}")

    if dates:
        print(f"Latest: {dates[0]}")
        versions = manager.list_versions(dates[0])
        print(f"Versions for {dates[0]}: {len(versions)}")


if __name__ == "__main__":
    main()
