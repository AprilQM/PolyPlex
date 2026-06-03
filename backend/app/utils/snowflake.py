# cores/snowflake.py
import time
import threading


def _current_millis() -> int:
    return int(time.time() * 1000)


class TypedSnowflakeIDGenerator:
    def __init__(self, type_id: int = 0):
        """
        初始化带类型的精简雪花 ID 生成器
        :param type_id: ID 类型 (0 ~ 31)
        """
        if not (0 <= type_id < 32):
            raise ValueError("type_id must be between 0 and 31")

        self.type_id = type_id

        # 位分配
        self.sequence_bits = 7  # 每毫秒 128 个 ID (0-127)
        self.type_id_bits = 5  # 32 种类型 (0-31)
        self.max_sequence = (1 << self.sequence_bits) - 1  # 127

        self.type_id_shift = self.sequence_bits
        self.timestamp_left_shift = self.sequence_bits + self.type_id_bits  # 7 + 5 = 12

        # 起始时间戳：2024-01-01 00:00:00 UTC (毫秒)
        self.epoch = 1704067200000

        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def generate_id(self) -> int:
        with self.lock:
            timestamp = _current_millis()

            if timestamp < self.last_timestamp:
                raise RuntimeError("Clock moved backwards. Refusing to generate id.")

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    # 序列号用完，等待下一毫秒
                    while timestamp <= self.last_timestamp:
                        timestamp = _current_millis()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                    ((timestamp - self.epoch) << self.timestamp_left_shift)
                    | (self.type_id << self.type_id_shift)
                    | self.sequence
            )


# === 类型常量定义 ===
USER_ID_TYPE = 1  # 用户
PROJECT_ID_TYPE = 2  # 项目
USER_TAG_ID_TYPE = 3  # 用户标签
PROJECT_TAG_ID_TYPE = 4  # 项目标签
NOTIFICATION_ID_TYPE = 5  # 通知
PROJECT_PAGE_ID_TYPE = 6  # 项目页面
PROJECT_BRANCH_ID_TYPE = 7  # 项目分支
PROJECT_MERGE_REQUEST_ID_TYPE = 8  # 项目合并请求
FILE_ID_TYPE = 9  # 文件
USER_TAG_RELATION_ID_TYPE = 10  # 用户标签关系
PROJECT_TAG_RELATION_ID_TYPE = 11  # 项目标签关系
PROJECT_USER_RELATION_ID_TYPE = 12  # 项目用户关系
COMPONENT_ID_TYPE = 15  # 组件
PAGE_COMPONENT_RELATION_ID_TYPE = 16  # 页面组件关系
FILE_PACKAGE_ID_TYPE = 17  # 文件包
FILE_PACKAGE_RELATION_ID_TYPE = 18  # 文件包关系
BRANCH_VERSION_ID_TYPE = 19  # 分支版本
BRANCH_VERSION_CHANGE_ID_TYPE = 20  # 分支版本变更
GROUP_ID_TYPE = 21  # 用户组
GROUP_USER_RELATION_ID_TYPE = 22  # 用户组成员关系
PROJECT_GROUP_ID_TYPE = 23  # 项目组权限
FILE_GROUP_ID_TYPE = 24  # 文件组权限

# === 预创建生成器===
user_id_gen = TypedSnowflakeIDGenerator(type_id=USER_ID_TYPE)
project_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_ID_TYPE)
user_tag_id_gen = TypedSnowflakeIDGenerator(type_id=USER_TAG_ID_TYPE)
project_tag_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_TAG_ID_TYPE)
notification_id_gen = TypedSnowflakeIDGenerator(type_id=NOTIFICATION_ID_TYPE)
project_page_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_PAGE_ID_TYPE)
project_branch_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_BRANCH_ID_TYPE)
project_merge_request_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_MERGE_REQUEST_ID_TYPE)
file_id_gen = TypedSnowflakeIDGenerator(type_id=FILE_ID_TYPE)
user_tag_relation_id_gen = TypedSnowflakeIDGenerator(type_id=USER_TAG_RELATION_ID_TYPE)
project_tag_relation_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_TAG_RELATION_ID_TYPE)
project_user_relation_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_USER_RELATION_ID_TYPE)
component_id_gen = TypedSnowflakeIDGenerator(type_id=COMPONENT_ID_TYPE)
page_component_relation_id_gen = TypedSnowflakeIDGenerator(type_id=PAGE_COMPONENT_RELATION_ID_TYPE)
file_package_id_gen = TypedSnowflakeIDGenerator(type_id=FILE_PACKAGE_ID_TYPE)
file_package_relation_id_gen = TypedSnowflakeIDGenerator(type_id=FILE_PACKAGE_RELATION_ID_TYPE)
branch_version_id_gen = TypedSnowflakeIDGenerator(type_id=BRANCH_VERSION_ID_TYPE)
branch_version_change_id_gen = TypedSnowflakeIDGenerator(type_id=BRANCH_VERSION_CHANGE_ID_TYPE)
group_id_gen = TypedSnowflakeIDGenerator(type_id=GROUP_ID_TYPE)
group_user_relation_id_gen = TypedSnowflakeIDGenerator(type_id=GROUP_USER_RELATION_ID_TYPE)
project_group_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_GROUP_ID_TYPE)
file_group_id_gen = TypedSnowflakeIDGenerator(type_id=FILE_GROUP_ID_TYPE)


# === 便捷函数 ===
def generate_user_id() -> int:
    return user_id_gen.generate_id()

def generate_project_id() -> int:
    return project_id_gen.generate_id()

def generate_user_tag_id() -> int:
    return user_tag_id_gen.generate_id()

def generate_project_tag_id() -> int:
    return project_tag_id_gen.generate_id()

def generate_notification_id() -> int:
    return notification_id_gen.generate_id()

def generate_project_page_id() -> int:
    return project_page_id_gen.generate_id()

def generate_project_branch_id() -> int:
    return project_branch_id_gen.generate_id()

def generate_project_merge_request_id() -> int:
    return project_merge_request_id_gen.generate_id()

def generate_file_id() -> int:
    return file_id_gen.generate_id()

def generate_user_tag_relation_id() -> int:
    return user_tag_relation_id_gen.generate_id()

def generate_project_tag_relation_id() -> int:
    return project_tag_relation_id_gen.generate_id()

def generate_project_user_relation_id() -> int:
    return project_user_relation_id_gen.generate_id()

def generate_component_id() -> int:
    return component_id_gen.generate_id()

def generate_page_component_relation_id() -> int:
    return page_component_relation_id_gen.generate_id()

def generate_file_package_id() -> int:
    return file_package_id_gen.generate_id()

def generate_file_package_relation_id() -> int:
    return file_package_relation_id_gen.generate_id()

def generate_branch_version_id() -> int:
    return branch_version_id_gen.generate_id()

def generate_branch_version_change_id() -> int:
    return branch_version_change_id_gen.generate_id()

def generate_group_id() -> int:
    return group_id_gen.generate_id()

def generate_group_user_relation_id() -> int:
    return group_user_relation_id_gen.generate_id()

def generate_project_group_id() -> int:
    return project_group_id_gen.generate_id()

def generate_file_group_id() -> int:
    return file_group_id_gen.generate_id()
