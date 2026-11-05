<a href="https://pajiala99.github.io">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img alt="Hardik Pajiala: I build the whole system, from backend APIs and data pipelines to ML models, AI agents and apps" src="assets/header-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://pajiala99.github.io"><img src="https://img.shields.io/badge/Portfolio-pajiala99.github.io-d4a94c?style=for-the-badge&logo=githubpages&logoColor=white" alt="Portfolio"></a>
  <a href="https://linkedin.com/in/hardik-pajiala"><img src="https://img.shields.io/badge/LinkedIn-hardik--pajiala-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:hardikpajiala@gmail.com"><img src="https://img.shields.io/badge/Email-hardikpajiala%40gmail.com-555?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>

<p align="center">
  <a href="#hackathons">🏆 Hackathons</a> ·
  <a href="#projects">🛠️ Projects</a> ·
  <a href="#tech">🧰 Tech</a> ·
  <a href="#activity">📈 Activity</a> ·
  <a href="https://pajiala99.github.io">💬 Ask the guide on my portfolio</a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img alt="At a glance: contributions in the last year, public projects, hackathons, and languages across my repos" src="assets/stats-light.svg" width="100%">
</picture>

## Hackathons

<details open>
<summary><b>SafeTrail</b> · BIOS V2, problem statement winner 🏆 · <i>click to fold</i></summary>
<br>

A trail-safety app for treks and pilgrimages. I was the top contributor in a team of two.

- 📍 Geofenced danger zones: entering one sets off an alarm, a spoken warning and a red frame
- 📶 An SOS that is saved on the phone and sent when signal returns, with SMS as a fallback
- 🗺️ A responder view with a live map, SOS grouped into incidents, and signed passes checked offline
- 🛡️ The AI is never in the emergency path. It only writes and translates text, under a per-job budget, with a standard fallback
- 📊 Benchmarked four builds: 82% fewer AI tokens per trip than a naive build

`FastAPI` `React` `TypeScript` `MapLibre` `Server-Sent Events` `pytest` · [**Repository →**](https://github.com/pajiala99/BIOS-SafeTrail)

</details>

<details>
<summary><b>Smriti</b> · Smart India Hackathon, SIH26003 · <i>click to expand</i></summary>
<br>

A memory and care companion for elders with dementia in North East India, built by our team for the Ministry of DoNER problem statement.

- 🕰️ Elder screen: a large orientation clock, read-aloud, family voice messages and a one-tap SOS
- 🥁 Culturally local games, like a Bihu rhythm game, with an Assamese folk-flute sound synthesised in the browser
- 📈 Caregiver dashboard: engagement and sundowning charts, routine pace and a geofence map
- 📱 Offline Flutter tablet build: a hearing screen, an adaptive memory game and a decline alert

`React` `TypeScript` `Web Audio API` `Flutter` `SQLite` · [**Web app →**](https://github.com/urgirlgeet/Smriti) · [**Flutter app →**](https://github.com/khushidangi/Smriti)

</details>

<details>
<summary><b>PRAMAAN</b> · Homingo Hackathon, Agents track · <i>click to expand</i></summary>
<br>

An AI agent that investigates job offers for recruitment scams.

- 🔎 Claude plans the investigation across 5 tools: red-flag rules, domain age, lookalike domains, careers pages and a web search for scam reports
- ⚖️ The model never decides. Fixed rules over cited evidence give the verdict, and it never calls a scam on one source alone
- 🧪 61 tests, including a prompt-injection test

`Python` `Claude API` `Tool use` `Streamlit` · [**Repository →**](https://github.com/pajiala99/pramaan)

</details>

## Projects

<details>
<summary><b>Cricket Win-Probability Lakehouse</b> · 1.67M ball-by-ball rows · <i>click to expand</i></summary>
<br>

- 🏗️ A bronze/silver/gold Delta Lake lakehouse built from 7,000+ nested JSON files in 180 s
- 🔁 Exactly-once streaming ingestion and revision-safe MERGE upserts, guarded by 19 data-quality checks
- 🎯 A Spark MLlib win-probability model: 0.777 AUC and 1.8 pp calibration error on unseen seasons, scored live

`PySpark` `Delta Lake` `Structured Streaming` `Spark MLlib` `Airflow` · [**Repository →**](https://github.com/pajiala99/cricket-winprob-lakehouse)

</details>

<details>
<summary><b>FoodBridge</b> · backend and matching engine · <i>click to expand</i></summary>
<br>

- 🔌 26 REST endpoints over a 10-table PostgreSQL/PostGIS schema, with JWT auth and state machines
- 🧮 A FastAPI matcher that scores donor–shelter pairs and assigns them with the Hungarian algorithm

`Node.js` `TypeScript` `PostgreSQL` `PostGIS` `FastAPI` · [**Repository →**](https://github.com/pajiala99/project_SE3)

</details>

<details>
<summary><b>Indian Sign Language Recognition</b> · webcam signs to speech · <i>click to expand</i></summary>
<br>

- ✋ A BiLSTM with attention on MediaPipe keypoints that recognises 61 signs live and speaks them
- 🧪 Went beyond a saturated benchmark: 94.5% top-1 from just 5 examples per word

`PyTorch` `MediaPipe` `BiLSTM` · [**Repository →**](https://github.com/pajiala99/isl-recognition)

</details>

<details>
<summary><b>Academic Timetable Generator</b> · graph colouring meets scheduling · <i>click to expand</i></summary>
<br>

- 🧩 Clique and Hall's-theorem checks prove when no timetable can exist, before any search
- 🔍 Backtracking meets every hard constraint, then simulated annealing improves the soft ones

`Java` `JavaFX` `MySQL` · [**Repository →**](https://github.com/pajiala99/academic-timetable-generator)

</details>

## Tech

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

## Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pajiala99/pajiala99/output/snake-dark.svg">
  <img alt="A snake eating my GitHub contribution graph" src="https://raw.githubusercontent.com/pajiala99/pajiala99/output/snake-light.svg" width="100%">
</picture>

<sub>Batch Group Leader for a 300-student batch at Thapar · Saturnalia volunteer · off the keyboard: gym, running, music and anime. The images above refresh daily through a GitHub Action in this repo.</sub>
