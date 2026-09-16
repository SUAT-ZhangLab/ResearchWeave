# BASH_TOOL_USAGE

来源：[Finch / src/fhda/prompts.py 第 80–110 行](https://github.com/Future-House/finch/blob/aea66fdf2dd2be827727de50a73cae60dff59972/src/fhda/prompts.py#L80-L110)。

许可：Apache-2.0，完整许可证在 `../original/LICENSE`。

下方为公开源码中的字符串值。f-string 中引用的固定文本已按源码展开，任务变量保留原样。未翻译或修改正文；Markdown 标题和说明为本次添加。

````text

If you need to use Busco, you can use it through udocker as follows:

```bash
# BUSCO Guidelines:
# 1. Set up the required directory structure for BUSCO:
mkdir busco_downloads
mkdir busco_downloads/lineages
mv <lineage_db> busco_downloads/lineages  # Move your downloaded lineage database

# 2. Run BUSCO analysis on protein files:
for protein_file in *.<protein_extension> ; do
  output_name=$(echo "$protein_file" | sed "s/.<protein_extension>$/.busco/g")
  udocker --allow-root run -u $(id -u)     -v /content/:/busco_wd     ezlabgva/busco:v5.8.0_cv1     busco -i $protein_file     -m prot     --offline     -o $output_name     -l <lineage_name>
done

# Note: Replace the following placeholders:
# - <lineage_db>: Your downloaded BUSCO lineage database directory
# - <protein_extension>: Your protein file extension (e.g., faa, fasta)
# - <lineage_name>: Name of the BUSCO lineage to use (e.g., eukaryota_odb10)
```

You can also use mafft, clipkit, fastqc, iqtree, metaeuk, perl, phykit through the command line.
````
