#!/usr/bin/env python3
"""
Protenix 作业 JSON 生成器（编排层）。

本文件只做「参数 → 模板 → 填值 → 拼装 → 输出」的串联，
JSON 结构由 template/ 下的模板文件决定，
文件读取逻辑由 readers.py 决定，
命令行接口由 args.py 决定。
"""

import json
from pathlib import Path

from args import parse
import readers as readers
import templates as templates


# ---------- 单条参数 → 序列条目 ----------

def _build_protein(arg: str) -> dict:
    """
    蛋白参数格式:
      seq.fa           → 无 MSA
      seq.fa:./msa/1   → 带 MSA 目录
    """
    parts = arg.split(":", 1)
    fasta_path = Path(parts[0])
    sequence = readers.read_fasta(fasta_path)

    if len(parts) > 1:
        return templates.new_entry(
            "proteinChain_msa.json",
            {"sequence": sequence, "msa_dir": parts[1]},
        )
    return templates.new_entry(
        "proteinChain.json",
        {"sequence": sequence},
    )


def _build_dna(arg: str) -> dict:
    sequence = readers.read_fasta(Path(arg))
    return templates.new_entry(
        "dnaSequence.json",
        {"sequence": sequence},
    )


def _build_ligand(arg: str) -> dict:
    """
    配体参数格式:
      CCD_xxx          → CCD ID 字符串（以 CCD_ 开头不走文件）
      其他             → 尝试当文件路径，否则当原始字符串
    """
    if arg.startswith("CCD_"):
        ligand_val = arg
    else:
        p = Path(arg)
        ligand_val = readers.read_first_line(p) if p.exists() else arg

    return templates.new_entry(
        "ligand.json",
        {"ligand": ligand_val},
    )


# ---------- 主流程 ----------

_BUILDERS = {
    "protein": _build_protein,
    "dna": _build_dna,
    "ligand": _build_ligand,
}


def main():
    args = parse()

    entries = []
    for arg in args.protein:
        entries.append(_BUILDERS["protein"](arg))
    for arg in args.dna:
        entries.append(_BUILDERS["dna"](arg))
    for arg in args.ligand:
        entries.append(_BUILDERS["ligand"](arg))

    if not entries:
        raise SystemExit("错误：至少需要一个 -p / -d / -l")

    job = templates.new_job_skeleton(args.name)
    job[0]["sequences"] = entries

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(job, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"✓ {out}  ← {len(entries)} 个序列条目")


if __name__ == "__main__":
    main()
