# AI-Powered Blockchain-Enabled Collaborative MEC Intrusion Detection System

## Overview

This project is a distributed Intrusion Detection System (IDS) that combines Artificial Intelligence (AI), Multi-access Edge Computing (MEC), and Blockchain to detect, classify, and collaboratively respond to network attacks in real time.

Each MEC node independently analyzes network traffic using a Deep Neural Network (DNN), while a blockchain-based threat intelligence mechanism securely shares malicious IP information among nodes, enabling decentralized and resilient cyber defense.

---

## Features

- AI-powered network attack detection using Deep Neural Networks (PyTorch)
- Real-time intrusion detection through FastAPI REST APIs
- Distributed architecture with multiple MEC nodes
- Blockchain-based collaborative threat intelligence sharing
- Automatic malicious IP blacklisting using smart contract logic
- Real-time monitoring dashboard with attack visualization
- Risk assessment and confidence scoring
- Multi-class attack classification using the CICIDS2017 dataset

---

## Technologies Used

- Python
- FastAPI
- PyTorch
- Scikit-learn
- NumPy
- HTML
- CSS
- JavaScript
- Bootstrap
- Blockchain (Custom Implementation)

---

## System Architecture

```
                    Network Traffic
                           │
                           ▼
                 AI Detection Model (DNN)
                           │
                           ▼
                  Attack Classification
                           │
                           ▼
                 Smart Contract Logic
                           │
                           ▼
             Blockchain Threat Intelligence
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
        MEC Node 1      MEC Node 2      MEC Node 3
          │                │                │
          └──────── Threat Intelligence ───┘
```

---

## Project Structure

```
AI-Powered-Blockchain-MEC-IDS/
│
├── app.py
├── predict.py
├── model.py
├── blockchain.py
├── blacklist.py
├── smart_contract.py
├── mec_utils.py
├── mec_node_1.py
├── mec_node_2.py
├── mec_node_3.py
├── requirements.txt
├── templates/
├── static/
├── ids_model.pth
├── multiclass_scaler.pkl
└── label_encoder.pkl
```

---

## Dataset

- **Dataset:** CICIDS2017
- **Classes:** Multiple network attack categories including:
  - BENIGN
  - DDoS
  - DoS Hulk
  - DoS GoldenEye
  - PortScan
  - Bot
  - FTP-Patator
  - SSH-Patator
  - Web Attack

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Start the Main IDS

```bash
uvicorn app:app --reload --port 8000
```

Start MEC Node 1

```bash
uvicorn mec_node_1:app --reload --port 8001
```

Start MEC Node 2

```bash
uvicorn mec_node_2:app --reload --port 8002
```

Start MEC Node 3

```bash
uvicorn mec_node_3:app --reload --port 8003
```

---

## Future Enhancements

- Docker containerization
- Kubernetes deployment
- Real blockchain integration
- Real-time packet capture
- Cloud deployment on AWS
- Explainable AI (XAI) for attack predictions

---

## Author

**srivatsa m n**

Bachelor of Engineering (Information Science & Engineering)
