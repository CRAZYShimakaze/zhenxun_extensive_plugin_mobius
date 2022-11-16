import json
import os
import random
import re
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Message, GroupMessageEvent, GROUP
from nonebot.params import CommandArg
from nonebot_plugin_htmlrender import text_to_pic
from .game import GameSession

__zx_plugin_name__ = "崩坏三猜语音"
__plugin_usage__ = """
usage：
    崩坏三猜语音
    指令：
        崩坏三猜语音：正常舰桥、战斗等语音
        崩坏三猜语音2/困难：简短的语气或拟声词
        崩坏三猜语音答案
        崩坏三语音[name]：随机发送指定女武神一段语音
        崩坏三语音列表[name]：查看指定女武神所有语音
        崩坏三语音[name][id]：发送指定女武神的指定语音
""".strip()
__plugin_des__ = "崩坏三猜语音"
__plugin_cmd__ = ["崩坏三猜语音"]
__plugin_type__ = ("崩坏三相关",)
__plugin_version__ = 0.1
__plugin_author__ = "mobius"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["崩坏三猜语音", "崩三猜语音", "崩3猜语音", "崩坏3猜语音"],
}


guess = on_command("崩坏三猜语音", aliases={"崩三猜语音", "崩3猜语音", "崩坏3猜语音", "猜语音"}, priority=5, permission=GROUP, block=True)
answer = on_command("崩坏三猜语音答案", aliases={"崩三猜语音答案", "崩3猜语音答案", "崩坏3猜语音答案", "猜语音答案"}, priority=6, permission=GROUP, block=True)
guessName = on_command("崩坏三语音", aliases={"崩三语音", "崩3语音", "崩坏3语音"}, priority=6, permission=GROUP, block=True)
addAnswer = on_command("崩坏三语音新增答案", aliases={"崩三语音新增答案", "崩3语音新增答案", "崩坏3语音新增答案"}, priority=5, permission=SUPERUSER, block=True)
undateVoice = on_command("更新崩坏三语音列表", aliases={"更新崩三语音列表", "更新崩3语音列表", "更新崩坏3语音列表"}, priority=5, permission=SUPERUSER, block=True)
def split_voice_by_chara(v_list: list):
    """对语音列表进行分类"""
    ret = {
        "normal": {},  # 正常语音
        "hard": {}   # 语气&拟声词
    }
    for voice in v_list:
        op_dict = ret["hard"] if "拟声词" in voice["voice_path"] else ret["normal"]
        chara = re.split("-|\(", voice["voice_name"])[0].strip()
        if re.search(r"《|【", chara):
            continue
        if not op_dict.get(chara):
            op_dict[chara] = []
        op_dict[chara].append(voice)
    return ret


def gen_voice_list(origin_path=None):
    """递归生成语音列表"""
    voice_dir = os.path.join(os.path.dirname(__file__), "../assets/record")
    if origin_path is None:
        origin_path = voice_dir
    ret_list = []
    for item in os.listdir(origin_path):
        item_path = os.path.join(origin_path, item)
        if os.path.isdir(item_path):
            ret_list.extend(gen_voice_list(item_path))
        elif item.endswith("mp3"):
            voice_path = os.path.relpath(item_path, voice_dir)
            ret_list.append({"voice_name": item, "voice_path": voice_path})
        else:
            continue
    return ret_list


@guess.handle()
async def guess_voice(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if re.search(r"2|困难", msg):
        difficulty = "hard"
    else:
        difficulty = "normal"
    game = GameSession(event.group_id)
    ret = await game.start(difficulty=difficulty)
    await guess.send(ret)


@answer.handle()
async def check_answer(event: GroupMessageEvent, arg: Message = CommandArg()):
    game = GameSession(event.group_id)
    if not game.is_start:
        return
    msg = arg.extract_plain_text().strip()
    msg = msg.lower().replace(",", "和").replace("，", "和")
    await game.check_answer(msg, event.user_id)


@guessName.handle()
async def send_voice(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    a_list = GameSession.__load__("answer.json")
    assert isinstance(a_list, dict)
    listCmd=re.compile(r"^列表")#命令头
    idCmd = re.compile(r"\d+$")#(语音id)
    if listCmd.search(msg):
        msg=listCmd.sub('', msg)  
        for k, v in a_list.items():
            if msg in v:
                try:
                    v_list = GameSession.__load__()["normal"][k]
                except KeyError:
                    await guessName.finish(f"语音列表未生成或有错误，请先发送‘更新崩坏三语音列表’来更新")
                #voice = random.choice(v_list)
                #voice_path = f"file:///{os.path.join(os.path.dirname(os.path.dirname(__file__)),'assets/record',voice['voice_path'])}"
                text=""
                for i in range(len(v_list)):
                    text+=f'{i}   {(v_list[i]["voice_name"])[:-4]}\n'
                pic = await text_to_pic(text=text)
                await guessName.finish(MessageSegment.image(pic))
        await guessName.send(f"没找到【{msg}】的语音，请检查输入。", at_sender=True)
    elif idCmd.search(msg):
        id=idCmd.search(msg)
        name=idCmd.sub('', msg)
        for k, v in a_list.items():
            if name in v:
                try:
                    v_list = GameSession.__load__()["normal"][k]
                    voice = v_list[int(id.group())]
                except KeyError:
                    await guessName.finish(f"语音列表未生成或有错误，请先发送‘更新崩坏三语音列表’来更新")                
                voice_path = f"file:///{os.path.join(os.path.dirname(os.path.dirname(__file__)),'assets/record',voice['voice_path'])}"
                await guessName.finish(MessageSegment.record(voice_path))
        await guessName.finish(f"没找到【{msg}】的语音，请检查输入。", at_sender=True)
    else:
        for k, v in a_list.items():
            if msg in v:
                try:
                    v_list = GameSession.__load__()["normal"][k]
                except KeyError:
                    await guessName.finish(f"语音列表未生成或有错误，请先发送‘更新崩坏三语音列表’来更新")
                voice = random.choice(v_list)
                voice_path = f"file:///{os.path.join(os.path.dirname(os.path.dirname(__file__)),'assets/record',voice['voice_path'])}"
                await guessName.finish(MessageSegment.record(voice_path))
        await guessName.send(f"没找到【{msg}】的语音，请检查输入。", at_sender=True)


@addAnswer.handle()
async def add_answer(event: MessageEvent, arg: Message = CommandArg()):
    msg=arg.extract_plain_text().strip()
    if not msg:
        await addAnswer.finish(f"未输入答案", at_sender=True)
    msgArr=msg.replace("：", ":").split(":")
    if len(msgArr) != 2:
        await addAnswer.finish(f"答案有误，输入参考：崩坏三语音新增答案丽塔(标准答案):缭乱星棘(别称)", at_sender=True)
    origin = msgArr[0].strip()
    new = msgArr[1].strip()
    data = GameSession.__load__("answer.json")
    if origin not in data:
        await addAnswer.finish(f"{origin}不存在。")
    if new in data[origin]:
        await addAnswer.finish(f"答案已存在。")
    data[origin].append(new)
    with open(
        os.path.join(os.path.dirname(__file__), "answer.json"), "w", encoding="utf8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    await addAnswer.finish("添加完成。")


@undateVoice.handle()
async def update_voice_list():
    data = gen_voice_list()
    data_dict = split_voice_by_chara(data)
    with open(
        os.path.join(os.path.dirname(__file__), "record.json"), "w", encoding="utf8"
    ) as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)
    num_normal = sum(len(data_dict["normal"][v]) for v in data_dict["normal"])
    num_hard = sum(len(data_dict["hard"][v]) for v in data_dict["hard"])
    await undateVoice.finish(f"崩坏3语音列表更新完成，当前共有语音{num_hard+num_normal}条，其中普通{num_normal}条，困难{num_hard}条")


if __name__ == "__main__":
    data = gen_voice_list()
    with open(
        os.path.join(os.path.dirname(__file__), "record.json"), "w", encoding="utf8"
    ) as f:
        json.dump(split_voice_by_chara(data), f, indent=4, ensure_ascii=False)
