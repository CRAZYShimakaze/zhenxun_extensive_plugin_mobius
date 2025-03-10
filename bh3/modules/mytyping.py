# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from datetime import datetime, date
from pydantic import BaseModel
from typing import List, Optional, Union
from configs.config import Config as ConfigMain


class Config:
    cookies: List[str]
    is_egenshin: bool
    egenshin_dir: Optional[str]
    cache_dir: Optional[str]
    username: Optional[str]
    password: Optional[str]

    def __init__(self, is_egenshin, egenshin_dir, cache_dir, username, password, cookies):
        self.is_egenshin = is_egenshin
        self.egenshin_dir = egenshin_dir
        self.cache_dir = cache_dir
        self.username = username
        self.password = password
        self.cookies = cookies


config = Config(is_egenshin=False, egenshin_dir=None, cache_dir=None, username="", password="", cookies = [ConfigMain.get_config("bind_bh3", "COOKIE")])
COOKIES = config.cookies[0]


class _favorite_character(BaseModel):
    id: str
    name: str
    star: int
    avatar_background_path: str
    icon_path: str
    background_path: str
    large_background_path: str


class WeeklyReport(BaseModel):
    favorite_character: Union[_favorite_character, None]
    gold_income: int
    gold_expenditure: int
    active_day_number: int
    online_hours: int
    expended_physical_power: int
    main_line_expended_physical_power_percentage: int


class _role(BaseModel):
    AvatarUrl: str
    nickname: str
    region: str
    level: int
    role_id: str


class _abyss(BaseModel):
    level: Optional[int]
    cup_number: Optional[int]
    level_of_quantum: Optional[str]
    level_of_ow: Optional[str]
    level_of_greedy: Optional[str]


class _stats(BaseModel):
    active_day_number: int
    suit_number: int
    stigmata_number: int
    armor_number: int
    sss_armor_number: int
    battle_field_ranking_percentage: str
    new_abyss: Optional[_abyss]
    old_abyss: Optional[_abyss]
    weapon_number: int
    god_war_max_punish_level: int
    god_war_extra_item_number: int
    god_war_max_challenge_score: int
    god_war_max_challenge_level: int
    god_war_max_level_avatar_number: int
    god_war_max_support_point: int
    battle_field_area: int
    battle_field_score: int
    abyss_score: int
    battle_field_rank: int


class _preference(BaseModel):
    abyss: int
    main_line: int
    battle_field: int
    open_world: int
    community: int
    comprehensive_score: int
    comprehensive_rating: str
    god_war: int
    is_god_war_unlock: bool


class Index(BaseModel):
    role: _role
    stats: _stats
    preference: _preference


class _boss(BaseModel):
    id: str
    name: str
    avatar: str


class _avatar(BaseModel):
    """角色,不含武器圣痕"""

    id: str
    name: str
    star: int
    avatar_background_path: str
    icon_path: str
    background_path: str
    large_background_path: str
    figure_path: str
    level: int
    oblique_avatar_background_path: str
    half_length_icon_path: str
    image_path: str


class _elf(BaseModel):
    id: int
    name: str
    avatar: str
    rarity: int
    star: int


class AbyssReport(BaseModel):
    score: int
    updated_time_second: Optional[datetime]
    time_second: Optional[datetime]
    area: Optional[int]
    boss: _boss
    lineup: List[_avatar]
    rank: Optional[int]
    settled_cup_number: Optional[int]
    cup_number: Optional[int]
    elf: Optional[_elf]
    level: Union[int, str]  # 段位
    settled_level: Optional[int]    # 终极区深渊结算后段位
    reward_type: Optional[str]  # 低级深渊升降级
    type: Optional[str] # 量子奇点|量子流形
    floor: Optional[int]    # 量子流形层数，量子奇点为0


class Abyss(BaseModel):
    reports: List[AbyssReport]


class BattleFieldInfo(BaseModel):
    elf: Union[_elf, None]
    lineup: List[_avatar]
    boss: _boss
    score: int


class BattleFieldReport(BaseModel):
    score: int
    rank: int
    ranking_percentage: str
    area: int
    battle_infos: List[BattleFieldInfo]
    time_second: datetime


class BattleField(BaseModel):
    reports: List[BattleFieldReport]


class godWarBuff(BaseModel):
    icon: str
    number: int
    id: int


class godWarCondition(BaseModel):
    name: str
    desc: str
    difficulty: int


class godWarRecord(BaseModel):
    settle_time_second: datetime
    score: int
    punish_level: int
    level: int
    buffs: List[godWarBuff]
    conditions: List[godWarCondition]
    main_avatar: _avatar
    support_avatars: List[_avatar]
    elf: Union[_elf, None]
    extra_item_icon: str


class godWarCollection(BaseModel):
    type: str
    collected_number: int
    total_number: int


class godWarSummary(BaseModel):
    max_level_avatar_number: int
    max_support_point: int
    extra_item_number: int
    max_punish_level: int
    max_challenge_score: int
    avatar_numbers: int
    max_challenge_level: int


class godWarAvatar(BaseModel):
    avatar: _avatar
    level: int
    challenge_success_times: int
    max_challenge_score: int
    max_punish_level: int
    max_challenge_level: int


class _godWar(BaseModel):
    records: List[godWarRecord]
    collections: List[godWarCollection]
    summary: godWarSummary
    avatar_transcript: List[godWarAvatar]


class _weapon(BaseModel):
    id: int
    name: str
    max_rarity: int
    rarity: int
    icon: str


class _stigamata(BaseModel):
    id: int
    name: str
    max_rarity: int
    rarity: int
    icon: str


class Chara_chara(BaseModel):
    avatar: _avatar
    weapon: _weapon
    stigmatas: List[_stigamata]


class Chara(BaseModel):
    character: Chara_chara
    is_chosen: bool


class Character(BaseModel):
    characters: List[Chara]


class FullInfo(BaseModel):
    """all in one"""

    godWar: Optional[_godWar]
    characters: Optional[Character]
    index: Index
    newAbyssReport: Optional[Abyss]
    latestOldAbyssReport: Optional[Abyss]
    weeklyReport: WeeklyReport
    battleFieldReport: BattleField


# 手账部分
class sourcepercent(BaseModel):
    action_id: int
    num: int
    name: str
    percent: int


class LastMonthInfo(BaseModel):
    group_by: List[sourcepercent]
    month_star: int
    month_hcoin: int
    last_month_star: int
    last_month_hcoin: int
    star_rate: int
    hcoin_rate: int
    month_start: datetime
    month_end: datetime
    month: int
    last_month: int
    uid: str
    month_level: int


class findex(BaseModel):
    uid: str
    date: date
    month: int
    month_hcoin: int
    month_star: int
    month_level: int
    day_hcoin: int
    day_star: int
    last_hcoin: int
    last_star: int


class finance_record(BaseModel):
    action_id: int
    time: datetime
    add_num: int
    action: str


class FinanceRecord(BaseModel):
    """水晶星石通用"""
    page: int
    month: int
    list: List[finance_record]


class FinanceInfo(BaseModel):
    getLastMonthInfo: LastMonthInfo
    index: findex
    getHcoinRecords: FinanceRecord
    getStarRecords: FinanceRecord


class result(BaseModel):
    """签到用"""
    region:str
    game_uid:str
    nickname:str
    level:int
    region_name:str
    total_sign_day:int
    is_sign:bool
    reward_icon:str
    reward_name:str
    reward_cnt:int
    # reward_total_sign_day:int
    # reward_today:str
    # icon:str
    # name:str
    # cnt:int
    # reward_sign_cnt_missed:int
    today:str
    status:str
    addons:str
    sign_response:Optional[dict]
    end:str