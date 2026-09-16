# FINAL_REPORT_FORMATTING_USER_MESSAGE

**性质：官方代码中的提示词字符串，英文内容未改写。**

- 出处：[FINAL_REPORT_FORMATTING_USER_MESSAGE](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/prompts.py#L785-L830)
- 提交号：4a5cce310f3bc7663a67117db88af43b84733ffe
- 作者/来源：FutureHouse technical staff / Future-House/robin
- 许可：Apache-2.0，全文见 ../LICENSE。
- 提取方式：Python AST literal_eval；合并相邻字符串并还原源码转义，不执行原程序。
- 模板变量（仅供阅读）：answer_text, sources_text。
- 下面是替换变量前的字符串；不会自动调用原系统的检索或执行工具。

## 原文

~~~~text
Reformat this text for APA 7th Style references, including both in-text citations and the reference list. DO NOT change any of the text body or the sources list, only the references formatting.

**APA 7th Citation Rules Summary:**

**I. In-Line Citations (Author-Date):**
*   **Parenthetical:** `(Lastname, Year)` or `(Lastname1 and Lastname2, Year)` for 2 authors or `(Lastname et al., Year)` for 3+ authors.
*   **Narrative:** `Lastname (Year)` or `Lastname et al. (Year)`.
*   **No Author:** `("Short Article Title", Year)` or `(*Short Book Title*, Year)`.
*   **No Date:** `(Lastname, n.d.)`.
*   **Organization:** `(Organization Name, Year)`.

**II. Reference List (titled "References", alphabetical, hanging indent):**
*   **Core Elements:** Author(s). (Date). *Title*. Source (publication info/publisher/URL/DOI).
*   **Journal Article:** `Author, A. A. (Year). Article title: Subtitle. *Journal Title*, *Volume*(Issue), page-range. DOI/URL`
*   **Book:** `Author, A. A. (Year). *Book title: Subtitle*. Publisher.`
*   **Chapter:** `Author, A. A. (Year). Chapter title. In E. Editor (Ed.), *Book title* (pp. X-Y). Publisher.`

Key clarifications:
*   If the same paper is cited multiple times in the reference list, just with different page numbers, you should consolidate these references into one reference. 
*   If the same paper is cited multiple times in-line, you should consolidate these references into one reference. For example, an in-line citation such as (smith2000xyz pages 14-16, smith2000xyz pages 1-3) should just be consolidated into the proper APA in-line citation for the single smith2000xyz reference.
*   The reference list will include extraneous details, such as a parenthetical note for how it is cited in the text body. You should remove these.
*   The reference list will include extraneous details, such as how many citations it has and the type of source (e.g. peer-reviewed journal). You should remove these.
*   Do not change any of the text body or the sources list, only the references formatting.
*   If there are any clinical trials that are not cited properly, include a summary of the title in the reference list and indicate it is a web search from ClinicalTrials.gov. For such in-line citations, just say (ClinicalTrials.gov with the date, if available)
*   MOST IMPORTANTLY, DO NOT MAKE UP ANY REFERENCES THAT ARE NOT IN THE SOURCES LIST. IF YOU ARE NOT SURE ABOUT A REFERENCE, JUST SAY (Unknown Reference). DO NOT MAKE UP ANY REFERENCES. JUST REFORMAT THE ONES THAT ARE PROVIDED.

Your output should be exactly the same text as given below, but just formatted with APA 7th Style references. Do not include anything else in your response except the reformatted text (including the APA formatted references). Text begins here:

{answer_text}


References:
{sources_text}

~~~~
