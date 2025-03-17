# Optimization Methods for Image Restoration

This repository contains the code and implementation details for the project "Optimization Methods for Image Restoration," authored by Felipe Vicentin and Franz Yuri. The project explores image restoration techniques using Tychonov and Total Variation regularizations, implemented both analytically and numerically. The focus is on applications like denoising, deblurring, and demasking.

## Table of Contents

- Introduction
- Features
- Installation
- Usage
- Experiments
- Contributors
- License

## Introduction

Image restoration deals with improving the quality of degraded images by addressing issues like noise, blur, and occlusions. This project implements two popular restoration methods: Tychonov Regularization, suitable for smooth restoration, and Total Variation Regularization, which is better at preserving edges. The project includes both analytical and numerical approaches, leveraging libraries like NumPy and PyTorch.

## Features

- Analytical and numerical implementations of Tychonov regularization.
- Numerical implementation of Total Variation regularization.
- Generalized gradient descent for optimization.
- Support for colored images.
- Handling of image masking.
- Comparative experiments and analysis using metrics like Peak Signal-to-Noise Ratio (PSNR).

## Installation

Clone this repository and install the required dependencies to get started. Ensure Python and pip are installed on your system.
The dependencies are provided in the `requirements.txt` file.

## Usage

The repository provides scripts to perform analytical denoising using Tychonov regularization, numerical restoration for both methods, and parameter tuning for scenarios like deblurring and demasking. Experimentation with different parameter values, such as λ, ε, and learning rates, is supported via configuration files.

## Experiments

The project includes several experiments to validate the implementations:
- Denoising: Comparing analytical and numerical solutions for Tychonov regularization.
- Comparison of Methods: Evaluating Tychonov and Total Variation methods in restoring image quality.
- Deblurring: Testing restoration on images affected by blur and noise.
- Demasking: Restoring masked and noisy images.

Results from experiments, including PSNR metrics and restored images, are saved in the `results/` directory.

## Contributors

Felipe Vicentin and Franz Yuri are the authors of this project. Contributions are welcome; feel free to open issues or pull requests.

## License

This project is licensed under the MIT License. Refer to the `LICENSE` file for details.
