# Churchland-Shenoy Macaque M1/PMd Rotational Dynamics Reaching Suite (`Churchland2012-jPCA` / `DANDI:000070`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Catalyzed the **dynamical-systems revolution in motor neuroscience** (`Churchland, Cunningham, Kaufman, Foster, Nuyujukian, Ryu & Shenoy, Nature, 2012`), overturning static directional-tuning views (`Georgopoulos` cosine tuning) by showing that `M1/PMd` preparatory activity sets the initial state $\mathbf{x}(t_0)$ of an **autonomous low-dimensional dynamical generator** (`\dot{\mathbf{x}} \approx M_{\text{skew}}\mathbf{x}`) whose quasi-oscillatory (`~1.5–2.5 Hz`) rotational trajectories drive multiphasic muscle EMG even during straight, non-periodic point-to-point reaches.
- **Delayed Center-Out & Curved-Barrier Maze Paradigms**:
  - Monkeys fixate and hold a central touch target during an instructed delay period (`0–1,000 ms`) while target(s) and virtual barriers appear on a vertical screen, then execute rapid straight or curved reaches upon the Go cue (`27` to `108` reach conditions across `Monkeys J, N, A, B`).

## 2. Recording Specifications & Preprocessing
- **Open NWB Release (`DANDI:000070`) + Classic `jPCA` MATLAB Pack**:
  - **`DANDI:000070`** (*Neural population dynamics during reaching*): Standardized **NWB** files spanning `10` dual-Utah-array (`M1 + PMd`) sessions from rhesus macaques (`Monkeys Jenkins & Nitschke`, `~1,911` total sorted units) with `1 ms` spike timestamps, continuous 3D optical bead hand trajectories, target/barrier geometry, and trial event markers (`torch_brain` / `brainsets` native support).
  - **Columbia Churchland Lab `jPCA` Pack**: Pre-aligned peri-movement (`[-50, +350] ms`) condition-averaged firing-rate tensors (`Data` structs) + deltoid/pectoralis/triceps `EMG` control populations (which show *non-rotational* multiphasic patterns) used directly in Figs. 3–5 of Churchland et al. (2012).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Tasks**: Skew-symmetric `jPCA` subspace projection ($\dot{X} = M_{\text{skew}} X$, $M_{\text{skew}}^\top = -M_{\text{skew}}$), preparatory output-null to movement output-potent subspace transition (`Kaufman et al. 2014`), single-trial latent ODE / `LFADS` (`Sussillo et al. 2015` / `Pandarinath et al. 2018`), and multi-session spike tokenization (`POYO`, `Azabou et al. 2023`).
- **Critical Modeling Pitfalls**:
  1. **Always Run Tensor Maximum Entropy (`TME`) Null Controls**: Temporal differentiation of *any* smooth bell-shaped sequence (`PC1` vs. `d(PC1)/dt`) yields `90°` phase-shifted curves! When claiming non-trivial rotational dynamics in new models or brain areas, test `R^2_Mskew` against covariance-matched `TME` surrogates (`Elsayed & Cunningham, Nature Neuroscience, 2017`) and compare against simultaneous `EMG` controls.
  2. **Align Strictly to Kinematic Movement Onset**: Reaction times after the Go cue vary by `50–150 ms` from trial to trial; trial-averaging locked to Go cue blurs high-frequency rotational phase—lock execution windows (`[-50, +250] ms`) to physical movement onset.
  3. **Avoid Overlap Leakage with `NLB-21 MC_Maze` (`DANDI:000128`)**: If pretraining a multi-session motor foundation model on `DANDI:000070` and evaluating downstream on `NLB-21 MC_Maze`, check recording dates/sessions carefully so identical Jenkins maze sessions are not leaked across pretrain and test!

## 4. Programmatic Download & Quickstart
```bash
# Download all 10 NWB sessions of Churchland & Shenoy (2012) directly from DANDI Archive
uvx dandi download DANDI:000070
```

## 5. Verified Primary References
- **`churchland2012rotational`**: Churchland, M. M., Cunningham, J. P., Kaufman, M. T., Foster, J. D., Nuyujukian, P., Ryu, S. I., & Shenoy, K. V. (2012). *Neural population dynamics during reaching*. Nature (`10.1038/nature11129`).
