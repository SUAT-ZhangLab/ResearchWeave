# Third-party sources

ZhangLuo's original integration code and documentation are licensed under Apache-2.0; see LICENSE.
This license does not replace the original terms of the following materials.

- **Robin**, FutureHouse contributors: Apache-2.0. Source snapshot `4a5cce310f3bc7663a67117db88af43b84733ffe`.
  This repository includes the prompt source needed to verify the extracted templates, not the full Robin application.
  See vendor/robin/LICENSE and agent-prompts/robin/manifest.json.
- **ERA**, Google contributors: Apache-2.0. Source snapshot `b836730b5c000526af95116b1d0e2c60c8cf0a10`.
  The unmodified FUTS implementation is in vendor/era/implementation/futs.py; see vendor/era/LICENSE.
- **Finch**, FutureHouse contributors: original source and license in agent-prompts/robin-components/original/.
- **Co-Scientist**, Juraj Gottweis, Wei-Hung Weng, Alexander Daryin et al.:
  Accelerating scientific discovery with Co-Scientist, Nature (2026), DOI 10.1038/s41586-026-10644-y.
  Public supplementary material is used under CC BY 4.0. See agent-prompts/co-scientist/source/SOURCE-LICENSE.md.
  Markdown extraction changes format and layout; Chinese guides are project adaptations.

The integration, research record format, Docker runner and agent installation workflow are project additions.
Original prompt bodies remain attributed to their sources. Public methods do not provide access to hosted Google or Edison services.
