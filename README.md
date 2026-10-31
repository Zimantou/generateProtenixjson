用模板生成protenix输入json的小工具

使用`pip install -e .`后， 使用命令`generateforprotenix`调用

例子：

> generateforprotenix  --name 7r6r -p seq.fa:./msa/1 -d dna.fa -o job.json
>
> generateforprotenix  --name 7wux -p a.fa:./msa/1 -p b.fa:./msa/2 -l CCD\_P4G -o job.json

