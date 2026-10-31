"""
模板加载与占位符替换。

所有 JSON 结构由 template/ 目录下的模板文件决定，
本模块不硬编码任何 JSON 字段——模板改了，输出结构就跟着改。
"""

import json
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "template"

# 占位符格式：{{key}}（双花括号包围任意非空 key）
_PLACEHOLDER_PREFIX = "{{"
_PLACEHOLDER_SUFFIX = "}}"


# ---------- 模板加载 ----------

def load_json(name: str) -> dict | list:
    """从 template/ 目录加载一个 JSON 模板。"""
    path = TEMPLATE_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


# ---------- 占位符替换 ----------

def _replace_str(s: str, values: dict) -> str:
    """
    在一个字符串中查找所有 {{key}} 并替换为 values[key]。

    - 替换前先把 values 的值统一转成字符串（json.dumps 再剥壳，
      以便数字 / 布尔 / None 也能正确落入 JSON 字符串里）。
    - 如果 values[key] 是 dict 或 list，直接替换成 JSON 子对象
      （调用方用 apply_placeholders 做值级别替换即可）。
    """
    for key, val in values.items():
        placeholder = f"{_PLACEHOLDER_PREFIX}{key}{_PLACEHOLDER_SUFFIX}"
        if placeholder in s:
            if isinstance(val, (dict, list)):
                # 把子结构直接嵌进字符串 → 不可能（字符串是原子值），
                # 这种情况交给 apply_placeholders 在值级别处理，
                # 这里只替换原始类型。
                continue
            s = s.replace(placeholder, str(val))
    return s


def apply_placeholders(obj, values: dict):
    """
    递归遍历 dict/list，把所有字符串里的 {{key}} 替换为 values[key]，
    如果 values[key] 是 dict/list，则直接替换掉占位符所在的整个值
    （适用于「某个键整个被替换成子结构」的场景）。
    """
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            new_v = apply_placeholders(v, values)
            result[k] = new_v
        return result
    elif isinstance(obj, list):
        return [apply_placeholders(item, values) for item in obj]
    elif isinstance(obj, str):
        # 尝试整串匹配：{{key}} → 整个替换成 values[key]
        stripped = obj.strip()
        if (stripped.startswith(_PLACEHOLDER_PREFIX)
                and stripped.endswith(_PLACEHOLDER_SUFFIX)):
            key = stripped[len(_PLACEHOLDER_PREFIX):-len(_PLACEHOLDER_SUFFIX)]
            if key in values:
                return values[key]
        # 否则做子串替换
        return _replace_str(obj, values)
    else:
        return obj  # int / float / bool / None 原样


# ---------- 常用模板组合 ----------

def new_job_skeleton(name: str) -> list:
    """用 template_onejob.json 生成一个空 job 外壳。"""
    tpl = load_json("template_onejob.json")
    return apply_placeholders(tpl, {"name": name}) # type:ignore


def new_entry(template_name: str, values: dict) -> dict:
    """
    用指定的 entry 模板生成一个序列条目。

    Args:
        template_name: template/ 下的文件名（如 "proteinChain.json"）
        values: 占位符 → 替换值 的 dict
    """
    tpl = load_json(template_name)
    return apply_placeholders(tpl, values) # type:ignore
