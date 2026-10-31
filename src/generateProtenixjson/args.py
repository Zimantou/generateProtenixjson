"""命令行参数定义——只有 argparse，没有任何业务逻辑。"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="基于 template/ 下的 JSON 模板生成 Protenix 作业",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
参数格式:
  -p seq.fa           单纯蛋白 FASTA
  -p seq.fa:./msa/1   蛋白 FASTA + 预计算 MSA 目录
  -d dna.fa           DNA FASTA
  -l CCD_P4G          CCD ID（以 CCD_ 开头的字符串）
  -l lig.smi          SMILES 文件

示例:
  python generateTemplate.py --name 7r6r -p seq.fa:./msa/1 -d dna.fa -o job.json
  python generateTemplate.py --name 7wux -p a.fa:./msa/1 -p b.fa:./msa/2 -l CCD_P4G -o job.json
""",
    )
    p.add_argument("--name", required=True, help="作业名称")
    p.add_argument(
        "-p", "--protein", action="append", default=[],
        help="蛋白 FASTA，可选 :msa_dir 后缀。可多次使用",
    )
    p.add_argument(
        "-d", "--dna", action="append", default=[],
        help="DNA FASTA。可多次使用",
    )
    p.add_argument(
        "-l", "--ligand", action="append", default=[],
        help="配体（CCD ID / SMILES 文件 / 字符串）。可多次使用",
    )
    p.add_argument(
        "-o", "--output", default="protenix_job.json",
        help="输出 JSON 路径（默认 protenix_job.json）",
    )
    return p


def parse():
    return build_parser().parse_args()
