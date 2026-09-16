# Robin 的提示词组合与调用方法

**下面保留官方源码片段；解释文字是本次整理。**变量模板由程序填入。只复制角色文字，不会自动获得原有检索、排序或文件处理能力。


## cot_prompting

[原始位置](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/multitrajectory_runner.py#L76-L92)

~~~~python
def cot_prompting(
        self, query: str, language: str, configuration: RobinConfiguration
    ) -> str:
        """Apply chain-of-thought prompting to the query."""
        guidelines = configuration.prompts.general_notebook_guidelines.format(
            language=language
        )
        if language == "R":
            guidelines = configuration.prompts.r_specific_guidelines
        return (
            f"{configuration.prompts.cot_agnostic.format(language=language)}\n"
            f"{guidelines}"
            "Here is the research question to address:\n"
            "<query>\n"
            f"{query}\n"
            "</query>\n"
        )
~~~~


## format_prompt

[原始位置](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/multitrajectory_runner.py#L94-L101)

~~~~python
def format_prompt(self, configuration: RobinConfiguration) -> str:
        """Format the prompt template with the provided arguments."""
        final_prompt = self.prompt_template.format(**self.prompt_args)
        if self.cot_prompt:
            final_prompt = self.cot_prompting(
                final_prompt, self.config.language, configuration
            )
        return final_prompt
~~~~


## _create_task_requests

[原始位置](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/multitrajectory_runner.py#L158-L197)

~~~~python
def _create_task_requests(
        self, step: Step, runtime_config: RuntimeConfig
    ) -> list[TaskRequest]:
        """Create task requests with either identical or dynamic prompts.

        Args:
            step: The step configuration
            runtime_config: The runtime configuration for the task

        Returns:
            List of task requests to be executed
        """
        task_requests = []
        task_count = max(step.parallel, 1)

        if step.prompt_generator and task_count > 1:
            prompt_pairs = step.prompt_generator()
            for prompt_text, prompt_args in prompt_pairs[:task_count]:
                step_copy = copy.deepcopy(step)
                step_copy.prompt_template = prompt_text
                step_copy.prompt_args = prompt_args
                query = step_copy.format_prompt(self.configuration)
                task_requests.append(
                    TaskRequest(
                        name=step.name,
                        query=query,
                        runtime_config=runtime_config,
                    )
                )
        else:
            query = step.format_prompt(self.configuration)
            task_requests = [
                TaskRequest(
                    name=step.name,
                    query=query,
                    runtime_config=runtime_config,
                )
            ] * task_count

        return task_requests
~~~~


## run_comparisons

[原始位置](https://github.com/Future-House/robin/blob/4a5cce310f3bc7663a67117db88af43b84733ffe/robin/utils.py#L698-L818)

~~~~python
async def run_comparisons(  # noqa: PLR0912
    pairs_list: list[tuple[int, int]],
    client: LiteLLMModel,
    system_prompt: str,
    ranking_prompt_format: str,
    assay_hypothesis_df: pd.DataFrame,
    output_filepath: str,
    max_concurrent_requests: int = 100,
) -> None:
    all_comparison_results = []
    error_log = []

    semaphore = asyncio.Semaphore(max_concurrent_requests)

    logger.info(
        f"Starting comparisons for {len(pairs_list)} pairs with max concurrency"
        f" {max_concurrent_requests}..."
    )

    tasks = [
        process_comparison_pair(
            pair,
            idx,
            semaphore,
            client,
            system_prompt,
            ranking_prompt_format,
            assay_hypothesis_df,
        )
        for idx, pair in enumerate(pairs_list)
    ]

    results = await tqdm_asyncio.gather(*tasks, desc="Comparing Hypotheses")

    # Process results
    for result in results:
        if result and result["status"] == "success":
            all_comparison_results.append(result["data"])
        elif result and result["status"] == "error":
            error_log.append(result)

    logger.info("\nFinished processing pairs.")
    logger.info(f" - Successful comparisons: {len(all_comparison_results)}")
    logger.info(f" - Errors encountered: {len(error_log)}")

    if not all_comparison_results:
        logger.error("No results to save. CSV file will not be created.")

    else:
        try:
            processed_results = []
            for res_dict in all_comparison_results:
                new_row = res_dict.copy()
                llm_eval_data = new_row.pop("llm_evaluation", {})

                if isinstance(llm_eval_data, str):
                    try:
                        llm_eval_data = ast.literal_eval(llm_eval_data)
                    except (ValueError, SyntaxError):
                        logger.exception(
                            "Warning: Could not parse llm_evaluation string:"
                            f" {llm_eval_data}. Skipping llm_evaluation fields for this"
                            " row."
                        )
                        llm_eval_data = {}

                new_row["Winner"] = llm_eval_data.get(
                    "Winner", ""
                )  # Use .get for safety
                new_row["Loser"] = llm_eval_data.get("Loser", "")
                new_row["Analysis"] = llm_eval_data.get("Analysis", "")
                new_row["Reasoning"] = llm_eval_data.get("Reasoning", "")

                processed_results.append(new_row)

            if not processed_results:
                logger.error(
                    "No results after processing. CSV file will not be created."
                )
                return

            desired_fieldnames = ["Winner", "Loser", "Analysis", "Reasoning"]

            if processed_results:
                original_keys = list(processed_results[0].keys())
                for key in original_keys:
                    if key not in desired_fieldnames:
                        desired_fieldnames.append(key)
            else:
                logger.warning(
                    "Warning: Processed results are empty. Cannot determine all"
                    " fieldnames automatically."
                )

            string_buffer = io.StringIO()
            writer = csv.DictWriter(
                string_buffer,
                fieldnames=desired_fieldnames,
                extrasaction="ignore",
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(processed_results)
            csv_content_string = string_buffer.getvalue()
            string_buffer.close()

            async with aiofiles.open(output_filepath, "w", encoding="utf-8") as csvfile:
                await csvfile.write(csv_content_string)

            logger.info(
                f"Successfully saved {len(all_comparison_results)} results to"
                f" {output_filepath}"
            )

        except IndexError:
            logger.exception(
                "Error: all_comparison_results (or processed_results) is empty, cannot"
                " determine CSV headers."
            )
        except Exception:
            logger.exception("Error saving results to CSV file.")
~~~~
