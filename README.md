# Geosmin and MIB monitoring research: selected methods

This repository presents **selected analysis methods** from Sulav Dhungana's undergraduate research in the Department of Data Science at the University of Texas at Arlington. The research examined historical municipal laboratory records for geosmin and 2-methylisoborneol (MIB), two compounds associated with taste and odor concerns in drinking-water systems.

The project asked whether recorded sampling dates and available laboratory results could support transparent screening for elevated concentrations, especially the **first observed rise** after a lower result. Work included checking units and non-detects, separating unresolved measurements, building observed elevation episodes, and evaluating probability estimates in chronological order. A related analysis examined output-labelled measurements, sensory odor readings, and laboratory timing. These steps matter because a good average score can still hide missed first rises, and laboratory timing affects when information could become available.

The release contains two small modules drawn from the research code: episode construction and probability scoring. The laboratory workbook, dated measurements, trained models, predictions, figures, and calculated results are not included. This is **not the full pipeline** and cannot reproduce the study's numerical findings on its own.

## What the code does

- `taste_odor_methods/episodes.py` accepts a table of dated, already classified observations. A first observed elevation requires an earlier below-threshold observation within the chosen maximum gap. An elevated observation without such an anchor remains unanchored. The returned episode ledger retains the interval between last observed low and first observed high, because the true start time is unknown.
- `taste_odor_methods/evaluation.py` scores supplied outcomes and predicted probabilities. It returns Brier score, log loss, average precision, and ROC area only when each quantity is defined. Calibration estimates require enough positive and negative observations.

These functions accept inputs prepared by the caller. See [INPUTS.md](INPUTS.md) for the required fields and interpretation limits. The repository is intentionally limited to methods; readers should not treat its absence of results as evidence that the underlying analysis has not been performed.

## Scope and interpretation

The original research evaluated historical observations. This code does not establish a validated 7–14 day warning system, current water quality, customer exposure, or an operational treatment recommendation. The full research results require review under the data provider's release terms before public distribution.

The [MIT license](LICENSE) applies to the code and documentation in this repository. It does **not** license or redistribute the laboratory data used in the study.

## Author

Sulav Dhungana, undergraduate researcher, University of Texas at Arlington, Department of Data Science.
