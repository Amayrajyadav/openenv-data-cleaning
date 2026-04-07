# 🧹 Data Cleaning OpenEnv

## 📌 Overview

This project implements a real-world OpenEnv environment for **data cleaning tasks**.

The environment simulates noisy datasets and evaluates cleaned outputs using a **reward-based scoring system (0–1)**.

---

## 🎯 Objective

Enable AI agents to learn data preprocessing through:

- Noisy input datasets  
- Structured cleaning tasks  
- Reward-based feedback  

---

## ⚙️ API Endpoints

### 🔹 POST `/reset`
Returns a noisy dataset.

### 🔹 POST `/step`
Accepts cleaned_data and returns reward.

### 🔹 GET `/state`
Returns current task state.

---

## 🧩 Action Space

```json
        {
          "cleaned_data": [
            {
              "name": "string",
              "age": "int",
              "email": "string"
            }
          ]
        }

