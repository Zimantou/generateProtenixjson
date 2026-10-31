"""
序列文件读取——只负责把文件内容转成纯字符串，
不关心这些字符串最终会塞进 JSON 的哪个字段。
"""

from pathlib import Path


def read_fasta(path: Path) -> str:
    """读单条 FASTA 序列：跳过所有 > 行和空行，拼接成一串。"""
    seqs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(">"):
            continue
        seqs.append(line)
    if not seqs:
        raise ValueError(f"FASTA 文件 {path} 为空或没有序列")
    return "".join(seqs)


def read_first_line(path: Path) -> str:
    """读文本文件的第一条非空行（SMILES、CCD ID、简单串）。"""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError(f"文件 {path} 为空")
