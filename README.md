<a href="https://pajiala99.github.io">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg?v=4">
    <img alt="Hardik Pajiala: I build the whole system, from backend APIs and data pipelines to ML models, AI agents and apps" src="assets/header-light.svg?v=4" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://pajiala99.github.io"><img src="https://img.shields.io/badge/Portfolio-pajiala99.github.io-d4a94c?style=for-the-badge&logo=githubpages&logoColor=white" alt="Portfolio"></a>
  <a href="https://linkedin.com/in/hardik-pajiala"><img src="https://img.shields.io/badge/LinkedIn-hardik--pajiala-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:hardikpajiala@gmail.com"><img src="https://img.shields.io/badge/Email-hardikpajiala%40gmail.com-555?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>

<p align="center">
  <a href="#whoami"><kbd>&nbsp;whoami&nbsp;</kbd></a>
  <a href="#results"><kbd>&nbsp;Results&nbsp;</kbd></a>
  <a href="#selected-builds"><kbd>&nbsp;Selected builds&nbsp;</kbd></a>
  <a href="#how-an-sos-survives-no-signal"><kbd>&nbsp;SOS lifecycle&nbsp;</kbd></a>
  <a href="#all-projects"><kbd>&nbsp;All projects&nbsp;</kbd></a>
  <a href="#toolkit"><kbd>&nbsp;Toolkit&nbsp;</kbd></a>
</p>

## whoami

| | |
|---|---|
| **Education** | B.E. Computer Engineering, Thapar Institute of Engineering & Technology, 2024–2028 |
| **Based in** | Patiala, India |
| **Works on** | Backend APIs · data pipelines on Spark and Delta Lake · ML models · AI agents with guardrails |
| **Currently** | Open to software, data and ML internships |
| **Reach me** | [Portfolio](https://pajiala99.github.io) · [LinkedIn](https://linkedin.com/in/hardik-pajiala) · [hardikpajiala@gmail.com](mailto:hardikpajiala@gmail.com) |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg?v=4">
  <img alt="At a glance: first place at BIOS 2026, three hackathons, public projects, and languages across my repos" src="assets/stats-light.svg?v=4" width="100%">
</picture>

## Results

| Result | Event |
|---|---|
| 🏆 **First place** | **BIOS 2026 hackathon**, Thapar Institute · built [SafeTrail](https://github.com/pajiala99/BIOS-SafeTrail) in a team of two, as the top contributor · [certificate](assets/certificate-bios-2026.jpg) |
| 🧩 **Team entry** | **Smart India Hackathon**, problem statement SIH26003 (Ministry of DoNER) · built [Smriti](https://github.com/urgirlgeet/Smriti), a memory and care companion for elders with dementia |
| 🤖 **Agents track** | **Homingo Hackathon** · built [PRAMAAN](https://github.com/pajiala99/pramaan), an AI agent that investigates recruitment scams |

<details>
<summary>🎖️ <b>View the first-place certificate</b></summary>
<br>
<img src="assets/certificate-bios-2026.jpg" alt="First place certificate for the winning project at BIOS 2026, presented to Hardik Pajiala" width="640">
</details>

## Selected builds

Each card replays the idea its project is built around. Click a card to open the repo.

<p align="center">
  <a href="https://github.com/pajiala99/BIOS-SafeTrail"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-safetrail-dark.svg?v=4"><img alt="SafeTrail: SOS calls are saved on the phone while there is no signal, then delivered to the responder when signal returns" src="assets/card-safetrail-light.svg?v=4" width="49%"></picture></a>
  <a href="https://github.com/pajiala99/cricket-winprob-lakehouse"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-cricket-dark.svg?v=4"><img alt="Cricket lakehouse: rows flow from bronze to silver to gold, and a bad row is quarantined at the quality gate" src="assets/card-cricket-light.svg?v=4" width="49%"></picture></a>
</p>
<p align="center">
  <a href="https://github.com/pajiala99/project_SE3"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-foodbridge-dark.svg?v=4"><img alt="FoodBridge: greedy matching scores 2.40 on a 4 by 4 example, and the Hungarian algorithm scores 2.97 on the same scores" src="assets/card-foodbridge-light.svg?v=4" width="49%"></picture></a>
  <a href="https://github.com/pajiala99/academic-timetable-generator"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-timetable-dark.svg?v=4"><img alt="Timetable generator: classes are coloured like a graph, and each colour becomes a time slot with no clashes" src="assets/card-timetable-light.svg?v=4" width="49%"></picture></a>
</p>

## How an SOS survives no signal

SafeTrail's SOS path, from the button to a resolved incident. Drag or zoom the diagram.

```mermaid
stateDiagram-v2
    direction LR
    state "Saved on phone" as Saved
    state "Send by SMS offered" as Sms
    state "Received by server" as Received
    state "Incident open" as Open
    state "Accepted" as Accepted
    state "En route" as EnRoute
    state "Resolved" as Resolved
    state "Cancelled by tourist" as Cancelled
    [*] --> Saved: hold SOS for 1.5 s
    Saved --> Saved: no signal, retry with backoff
    Saved --> Received: POST /sos, idempotent on client_id
    Saved --> Sms: still unsent after 120 s
    Sms --> Received: coded SMS
    Received --> Open: rules set priority, DBSCAN groups nearby SOS
    Open --> Accepted: responder accepts
    Accepted --> EnRoute
    EnRoute --> Resolved
    Open --> Cancelled: second hold on Cancel
    Resolved --> [*]
```

The server answers the moment an SOS arrives, and priority and grouping are plain rules. The AI writes the incident report afterwards, and nothing on this path waits for it.

## All projects

<details>
<summary><b>SafeTrail</b> · 🏆 First place, BIOS 2026 · trail safety that works without signal</summary>
<br>

A trail-safety app for treks and pilgrimages. I was the top contributor in a team of two.

- 📍 Geofenced danger zones: entering one sets off an alarm, a spoken warning and a red frame
- 📶 An SOS that is saved on the phone and sent when signal returns, with SMS as a fallback
- 🗺️ A responder view with a live map, SOS grouped into incidents, and signed passes checked offline
- 🛡️ The AI is never in the emergency path. It only writes and translates text, under a per-job budget, with a standard fallback
- 📊 Benchmarked four builds: 82% fewer AI tokens per trip than a naive build

`FastAPI` `React` `TypeScript` `MapLibre` `Server-Sent Events` `pytest` · [**Repository →**](https://github.com/pajiala99/BIOS-SafeTrail) · [**Certificate →**](assets/certificate-bios-2026.jpg)

</details>

<details>
<summary><b>Smriti</b> · Smart India Hackathon, SIH26003 · dementia care for North East India</summary>
<br>

A memory and care companion for elders with dementia in North East India, built by our team for the Ministry of DoNER problem statement.

- 🕰️ Elder screen: a large orientation clock, read-aloud, family voice messages and a one-tap SOS
- 🥁 Culturally local games, like a Bihu rhythm game, with an Assamese folk-flute sound synthesised in the browser
- 📈 Caregiver dashboard: engagement and sundowning charts, routine pace and a geofence map
- 📱 Offline Flutter tablet build: a hearing screen, an adaptive memory game and a decline alert

`React` `TypeScript` `Web Audio API` `Flutter` `SQLite` · [**Web app →**](https://github.com/urgirlgeet/Smriti) · [**Flutter app →**](https://github.com/khushidangi/Smriti)

</details>

<details>
<summary><b>PRAMAAN</b> · Homingo Hackathon, Agents track · an AI agent that checks job offers</summary>
<br>

- 🔎 Claude plans the investigation across 5 tools: red-flag rules, domain age, lookalike domains, careers pages and a web search for scam reports
- ⚖️ The model never decides. Fixed rules over cited evidence give the verdict, and it never calls a scam on one source alone
- 🧪 61 tests, including a prompt-injection test

`Python` `Claude API` `Tool use` `Streamlit` · [**Repository →**](https://github.com/pajiala99/pramaan)

</details>

<details>
<summary><b>Cricket Win-Probability Lakehouse</b> · 1.67M ball-by-ball rows</summary>
<br>

- 🏗️ A bronze/silver/gold Delta Lake lakehouse built from 7,000+ nested JSON files in 180 s
- 🔁 Exactly-once streaming ingestion and revision-safe MERGE upserts, guarded by 19 data-quality checks
- 🎯 A Spark MLlib win-probability model: 0.777 AUC and 1.8 pp calibration error on unseen seasons, scored live

`PySpark` `Delta Lake` `Structured Streaming` `Spark MLlib` `Airflow` · [**Repository →**](https://github.com/pajiala99/cricket-winprob-lakehouse)

</details>

<details>
<summary><b>FoodBridge</b> · backend and matching engine</summary>
<br>

- 🔌 26 REST endpoints over a 10-table PostgreSQL/PostGIS schema, with JWT auth and state machines
- 🧮 A FastAPI matcher that scores donor–shelter pairs and assigns them with the Hungarian algorithm

`Node.js` `TypeScript` `PostgreSQL` `PostGIS` `FastAPI` · [**Repository →**](https://github.com/pajiala99/project_SE3)

</details>

<details>
<summary><b>Indian Sign Language Recognition</b> · webcam signs to speech</summary>
<br>

- ✋ A BiLSTM with attention on MediaPipe keypoints that recognises 61 signs live and speaks them
- 🧪 Went beyond a saturated benchmark: 94.5% top-1 from just 5 examples per word

`PyTorch` `MediaPipe` `BiLSTM` · [**Repository →**](https://github.com/pajiala99/isl-recognition)

</details>

<details>
<summary><b>Academic Timetable Generator</b> · graph colouring meets scheduling</summary>
<br>

- 🧩 Clique and Hall's-theorem checks prove when no timetable can exist, before any search
- 🔍 Backtracking meets every hard constraint, then simulated annealing improves the soft ones

`Java` `JavaFX` `MySQL` · [**Repository →**](https://github.com/pajiala99/academic-timetable-generator)

</details>

## Toolkit

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java">
  <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++">
  <img src="https://img.shields.io/badge/Apache%20Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" alt="Apache Spark">
  <img src="https://img.shields.io/badge/Delta%20Lake-00ADD4?style=flat-square" alt="Delta Lake">
  <img src="https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" alt="Airflow">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Claude%20API-D97757?style=flat-square&logo=anthropic&logoColor=white" alt="Claude API">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
</p>

<sub>The header, the stats card and the project cards are drawn by <a href="scripts/build_assets.py">scripts/build_assets.py</a>; a GitHub Action refreshes the stats daily. Off the keyboard: Batch Group Leader for a 300-student batch at Thapar, Saturnalia volunteer, gym, running, music and anime.</sub>
