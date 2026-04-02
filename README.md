---
title: EcoRoute RL Agent Environment
emoji: 🚴
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
  - reinforcement-learning
  - sustainability
  - transportation
---

# EcoRoute RL Agent Environment

EcoRoute RL Agent is a custom OpenEnv environment designed for **sustainable route and transport decision-making**.  
It simulates an urban commuting scenario where an agent selects a transport mode and receives rewards based on:

- **Travel time**
- **CO₂ emissions**
- **Eco score**
- **Air quality exposure**

This environment is built for reinforcement learning experiments focused on **green mobility**, **smart commuting**, and **eco-friendly transportation planning**.

---

## 🌍 Problem Statement

Urban transportation contributes heavily to:

- Traffic congestion
- Fuel consumption
- Carbon emissions
- Poor air quality

EcoRoute RL Agent provides a simplified but realistic environment where an AI agent can learn to prefer **low-emission, healthier, and more sustainable travel choices** such as cycling, walking, or public transport.

---

## 🚀 Features

- Custom OpenEnv-compatible environment
- Supports `reset()`, `step()`, and `state`
- Multiple transport modes:
  - `walk`
  - `cycle`
  - `bus`
  - `car`
- Reward function based on:
  - Lower CO₂ emissions
  - Better eco score
  - Lower air pollution exposure
  - Reasonable travel time
- Session-based interaction through OpenEnv client/server architecture
- Deployable to Hugging Face Spaces

---

## 🧠 Environment Overview

The agent chooses a transport mode for a trip.

The environment returns:

- A **suggested route**
- Estimated travel time
- CO₂ emissions
- Eco score
- Air quality exposure
- A reward score

The goal is to maximize sustainable commuting outcomes.

---

## 📦 Action Space

### `EcorouteRlAgentAction`

The action contains:

- `transport_mode` (`str`)  
  Allowed values:
  - `"walk"`
  - `"cycle"`
  - `"bus"`
  - `"car"`

Example:

```python
EcorouteRlAgentAction(transport_mode="cycle")