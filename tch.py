from faker.providers import BaseProvider
from faker import Faker
import pymysql
import random


class CustomProvider(BaseProvider):
    def belong_college(self):
        belong_college = ["人工智能学院", "网络与通信学院", "智能制造学院", "数字商务学院", "电子信息学院",
                          '智能交通学院', "数码艺术学院", "士官学院"]
        return self.random_element(elements=belong_college)

    def human_sex(self):
        probability = random.random()
        if probability < 0.4:
            return "男"
        else:
            return "女"

    def belong_major(self, college):
        belong_major = {
            "人工智能学院": ["人工智能技术应用", "大数据技术", "嵌入式技术应用", "软件技术", "移动应用开发",
                             "计算机应用技术", "信息安全技术"],
            "网络与通信学院": ["物联网应用技术", "现代通信技术", "云计算技术与应用", "电信服务与管理",
                               "计算机网络技术"],
            "智能制造学院": ["机电一体化技术", "工业机器人技术", "智能控制技术", "电气自动化技术", "机械制造及自动化"],
            "数字商务学院": ["集成电路技术", "电子信息工程技术", "嵌入式技术应用", "电子信息工程技术",
                             "电子产品检测技术", "智能光电技术应用", "光伏工程技术"],
            "电子信息学院": ["集成电路技术", "电子信息工程技术", "嵌入式技术应用", "电子信息工程技术",
                             "电子产品检测技术", "智能光电技术应用", "光伏工程技术"],
            "智能交通学院": ["智能交通技术", "城市轨道交通通信信号技术", "汽车制造与试验技术", "新能源汽车技术",
                             "汽车智能技术", "智能网联汽车技术"],
            "数码艺术学院": ["虚拟现实技术应用", "数字媒体艺术设计", "影视动画", "录音技术与艺术", "视觉传达设计",
                             "数字媒体技术"],
            "士官学院": ["电子信息工程技术", "计算机应用技术", "计算机网络技术", "通信技术"]
        }
        return self.random_element(elements=belong_major[college])


def storage(name, sex, college, major):
    conn = pymysql.connect(host='localhost', user='root', passwd='Root1234!', db='teacher')
    cur = conn.cursor()
    cur.execute(
        "insert into tch (姓名, 性别, 学院, 专业) values (%s, %s, %s, %s)",
        (name, sex, college, major))
    cur.close()
    conn.commit()
    conn.close()


fake = Faker('zh-CN')
fake.add_provider(CustomProvider)

for i in range(0, 1500):
    name = fake.name()
    college = fake.belong_college()
    sex = fake.human_sex()
    major = fake.belong_major(college)
    storage(name, sex, college, major)
