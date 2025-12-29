# ⚡ OptiFlow: Enterprise A/B Testing Intelligence

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **OptiFlow** is a full-stack experimentation platform designed to bridge the gap between statistical rigor and rapid business decision-making. Unlike basic A/B test calculators, OptiFlow simulates real-world traffic volatility using **Monte Carlo methods**, visualizes risk with **Bayesian posterior distributions**, and ensures experiment validity through dynamic **Statistical Power Analysis**.

---

## 📸 Dashboard Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/3b7075c2-7491-4064-ade9-4fbf93deb54e" alt="Dashboard Demo 1" width="700"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/38cf041b-7375-4c99-baee-651bc64deeba" alt="Dashboard Demo 2" width="700"/>
</p>




---

## 🚀 Key Capabilities

### 1. 🔮 Monte Carlo Simulation
Visualizes **50+ alternate future realities** to demonstrate the volatility and risk inherent in random sampling. This helps stakeholders understand that "flat lines" in data are rare and prepares them for real-world variance.

### 2. 📊 Bayesian Inference
Plots **posterior probability density functions (PDFs)** to visualize the "overlap" and certainty between Control and Test groups. This provides a more intuitive understanding of risk compared to raw P-values.

### 3. ⚡ Dynamic Power Analysis
Real-time calculation of **Statistical Power (1 - β)** and **Cohen's *h* effect size**. The app warns users if their sample size is too low to detect a meaningful difference, preventing "underpowered" experiments.

### 4. 🏭 Industrial UX/UI
Features a **glassmorphism interface**, interactive Lottie animations, and a custom "loading state" engine to mimic the latency and feel of enterprise SaaS applications.

---

## 🛠️ Tech Stack & Architecture

This project follows industry-standard **Object-Oriented Programming (OOP)** principles:

* **`src/experiment.py`**: Encapsulates the core logic (A/B testing engine, simulation, stats).
* **`app.py`**: Handles the Streamlit frontend and visualization layer (decoupled from logic).
* **`tests/`**: Contains `pytest` suites to ensure statistical accuracy.

**Libraries Used:**
* **Core:** `NumPy`, `Pandas`, `SciPy`
* **Stats:** `Statsmodels` (Power Analysis, Z-tests)
* **Visualization:** `Plotly Graph Objects` (Interactive Charts)
* **Frontend:** `Streamlit`, `Streamlit-Lottie`

---

## 💻 How to Run Locally

**1. Clone the repository**
```bash
git clone [https://github.com/Athma-26/optiflow-ab-platform.git](https://github.com/Athma-26/optiflow-ab-platform.git)
cd optiflow-ab-platform
