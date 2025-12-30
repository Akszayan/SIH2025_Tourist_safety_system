# 🧳 Smart Tourist Safety Monitoring & Incident Response System

> **Smart India Hackathon (SIH) 2025**
> **Problem Statement ID:** 25002
> **Theme:** Travel & Tourism
> **Category:** Software
> **Team Name:** TECHPRENEURS
> **Status:** ✅ *Selected in Internal Rounds (University Level)*

---

## 📌 Problem Context

Tourism is a critical economic driver in regions such as India’s North-Eastern states. However, **tourist safety in remote, high-risk, or unfamiliar areas** remains a serious challenge due to:

* Limited policing reach
* Poor network connectivity
* Lack of real-time monitoring
* Delayed incident response

The **SIH 2025 Problem Statement (ID: 25002)** calls for a **technology-driven, privacy-first system** using **AI, Geo-Fencing, Blockchain-based Digital ID, and IoT** to ensure tourist safety while maintaining ease of travel and data security.

---

## 💡 Our Solution (Prototype)

We propose a **Smart Tourist Safety Monitoring & Incident Response System** — a **modular, scalable digital ecosystem** that combines **backend intelligence, IoT sensing, and real-time alerts**.

⚠️ *This implementation is a **general / early-stage prototype** built to demonstrate feasibility, system design, and core logic as part of SIH internal evaluations.*

### 🔑 Key Components

* **Temporary Digital Tourist Pass** (time-bound, verifiable)
* **AI-driven Safety Scoring**
* **IoT-based Anomaly & Fall Detection**
* **Panic & SOS Alert System**
* **Authority-ready APIs & Dashboards (conceptual)**

---

## 🧠 System Architecture (High Level)

```
Tourist / Wearable Device (ESP32 + MPU6050)
            ↓
     Sensor & Health Data
            ↓
     FastAPI Backend (AI Logic)
            ↓
   Safety Score & Anomaly Detection
            ↓
 Alerts → Buzzer / Authorities / Dashboard
```

---

## 🧩 Implemented Modules

### 1️⃣ Digital Tourist Pass System

* Generates **temporary, hashed tourist passes**
* Includes:

  * Tourist name
  * Trip duration
  * Expiry timestamp
* Designed to be extended to **Blockchain-based Digital IDs**

**Endpoints:**

* `POST /create_pass`
* `POST /verify_pass/{hash}`

---

### 2️⃣ AI-Based Safety Scoring

* Computes a **dynamic safety score** using:

  * Location context (risk zones)
  * Physiological indicators (heart rate)
* Designed to flag unsafe conditions proactively

**Endpoint:**

* `WebSocket /ws`

---

### 3️⃣ IoT Wearable Safety Device (ESP32 + MPU6050)

* Continuously monitors:

  * Acceleration (fall / impact)
  * Gyroscope data (abnormal motion)
* Sends data periodically to backend via HTTP

**Detected Events:**

* Free-fall
* Sudden impact
* Prolonged tilt (possible unconscious state)
* Rapid rotation (distress)

---

### 4️⃣ Incident & Panic Alert System

* Automatic alerts triggered by AI anomaly detection
* Manual **panic alert endpoint** for emergencies
* Backend can **force-trigger buzzer** on the wearable

**Endpoints:**

* `POST /panic`
* `POST /trigger_buzzer`

---

## ⚙️ Tech Stack Used

### Backend & APIs

* Python
* FastAPI
* Pydantic
* WebSockets

### AI / Logic

* Rule-based anomaly detection (prototype)
* Safety scoring logic (extensible to ML models)

### IoT & Embedded Systems

* ESP32
* MPU6050 (Accelerometer + Gyroscope)
* Wi-Fi (HTTP communication)
* Buzzer-based alert feedback

### System Design (Conceptual / Proposed)

* Blockchain-based Digital Tourist ID
* Geo-fencing (unsafe / restricted zones)
* Authority dashboards (police / tourism dept.)

---

## 🎯 Outcomes & Achievements

* ✅ Successfully mapped SIH PS requirements to a **working prototype**
* ✅ Designed an **end-to-end safety pipeline** (IoT → AI → Alert)
* ✅ Selected in **Internal Rounds of SIH 2025** at our university
* ✅ Demonstrated feasibility of integrating **AI + IoT + Secure IDs**

---

## 📚 Key Learnings

* Designing **real-time safety systems** under network constraints
* IoT sensor calibration and noise handling
* Backend architecture for emergency systems
* API-first design for multi-agency integration
* Balancing **privacy, safety, and usability**

---

## 🌍 Applications & Use Cases

* Tourist safety in remote or high-risk areas
* Solo traveler monitoring
* Pilgrimage & trekking routes
* Adventure tourism zones
* Emergency response coordination

---


## 🔮 Future Enhancements

* ML-based behavior modeling
* Blockchain-backed digital tourist IDs
* Geo-fencing with live maps
* Multilingual mobile app
* Police & tourism dashboards
* LoRaWAN / hybrid connectivity

---

## 📜 Disclaimer

This repository contains a **prototype solution developed for Smart India Hackathon 2025**. It is intended for **academic, research, and evaluation purposes only**.

---

> *Built with a focus on safety, responsibility, and real-world impact — SIH 2025.*
