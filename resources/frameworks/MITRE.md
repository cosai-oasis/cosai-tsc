## MITRE

## 1. ATT&CK

### 2.1. Overview

The MITRE ATT&CK framework is a globally recognized, open-source knowledge base that documents real-world adversary tactics, techniques, and procedures (TTPs) across the cyber-attack lifecycle. It organizes adversary behaviors into tactics (what attackers aim to achieve) and techniques/sub-techniques (how they do it), mapped into an intuitive matrix that spans multiple domains, including enterprise, mobile, cloud, and industrial control systems (ICS). Originally focused on post-attack activities, it now also includes early-stage attacker actions like reconnaissance. 

ATT&CK serves as a practical tool for red teaming, behavioral analytics, threat intelligence enrichment, and defensive gap assessments, linking techniques to adversary groups, software, and mitigations. It provides a practical, data-driven guide to strengthening defenses against real-world threats.

#### 2.1.1. Scoping of AI system and/or cybersecurity purview

The MITRE ATT&CK framework provides a structured approach for identifying, analyzing, and addressing threats in AI systems and cybersecurity. Scoping ATT&CK for AI systems involves adapting the framework's tactics and techniques to the unique aspects of AI, while integrating it into the broader cybersecurity purview.

***Components of AI Systems and Relevant ATT&CK Techniques***

| **Component**       | **Description**                                                  | **Relevant ATT&CK Techniques**                     |
|----------------------|------------------------------------------------------------------|----------------------------------------------------|
| **Data Pipeline**    | Protect data integrity, ensure secure collection and storage.   | Data Destruction (T1485), Data Manipulation (T1565) |
| **ML Models**        | Safeguard against adversarial attacks and model theft.          | Exploit Public-Facing Applications (T1190), Adversary-in-the-Middle (T1557) |
| **APIs and Interfaces** | Secure endpoints and prevent injection attacks.                | Input Capture (T1056), Command and Scripting Interpreter (T1059) |
| **Infrastructure**   | Secure cloud, edge, and on-prem systems hosting AI.             | Resource Hijacking (T1496), Cloud Service Exploitation (T1586) |


---

***ATT&CK Tactics in Cybersecurity Purview***

| **Tactic**            | **Description**                                                                  | **Relevant Techniques**                                       |
|------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------|
| **Initial Access**     | Methods used to gain unauthorized access to AI systems.                         | Phishing (T1566), Supply Chain Compromise (T1195), Valid Accounts (T1078) |
| **Defense Evasion**    | Hiding malicious activity or bypassing defenses.                                | Indicator Removal on Host (T1070), Abuse Elevation Control Mechanism (T1574) |
| **Privilege Escalation** | Techniques to gain elevated permissions in AI systems.                         | Exploitation for Privilege Escalation (T1068), New Service (T1201) |
| **Command and Control** | Techniques to maintain communication with compromised AI systems.               | Encrypted Channel (T1573), Multi-Hop Proxy (T1090) |
| **Impact**             | Techniques that manipulate AI outcomes or disrupt operations.                   | Data Manipulation (T1565), Service Stop (T1489) |

---

***Implementation Steps***

| **Step**               | **Description**                                                                  | **Example**                                                 |
|-------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------|
| **Asset Identification** | Inventory all AI-related assets and categorize based on importance and exposure. | Identify datasets, ML models, APIs, and supporting infrastructure. |
| **ATT&CK Mapping**       | Map tactics and techniques to AI vulnerabilities and processes.                 | Link "Model Evasion" to "Defense Evasion" and Input Injection. |
| **Red and Blue Teaming** | Use ATT&CK to simulate attacks (Red) and monitor defense readiness (Blue).       | Test adversarial input attacks on deployed AI systems.      |
| **Metrics and Coverage** | Measure defensive coverage and prioritize high-risk tactics.                    | Analyze detection capabilities for TTPs like Data Manipulation (T1565). |

---

#### 2.1.2. Persona addressed


| **Activity**                                | **Red Team** | **Blue Team** | **AI/ML Engineers** | **Threat Intelligence Analysts** | **Incident Responders** | **Software Architects** | **Security Architects** | **SOC Managers** | **SREs**     | **Executives & Risk Managers** | **Product Developers** |
|---------------------------------------------|--------------|---------------|----------------------|-----------------------------------|--------------------------|--------------------------|--------------------------|-------------------|-------------|---------------------------------|-------------------------|
| **Adversary Emulation for AI Systems**      | R            | C             | C                    | C                                 | I                        | C                        | C                        | I                 | C           | I                               | C                       |
| **Threat Detection in AI Systems**          | -            | R             | C                    | C                                 | C                        | C                        | I                        | A                 | C           | I                               | C                       |
| **AI-Specific Threat Intelligence Enrichment** | C          | C             | C                    | R                                 | C                        | I                        | I                        | I                 | C           | I                               | C                       |
| **Defensive Gap Assessment for AI**         | -            | R             | C                    | C                                 | C                        | C                        | A                        | C                 | I           | I                               | -                       |
| **SOC Maturity Assessment with AI Tools**   | I            | R             | C                    | C                                 | I                        | I                        | A                        | I                 | I           | I                               | -                       |
| **Incident Response for AI Breaches**       | I            | C             | C                    | C                                 | R                        | C                        | C                        | A                 | R           | I                               | I                       |
| **AI System Security Architecture Design**  | I            | C             | C                    | I                                 | C                        | R                        | R                        | A                 | C           | C                               | -                       |
| **AI-Specific Detection Rule Development**  | I            | R             | C                    | C                                 | I                        | C                        | C                        | A                 | C           | I                               | -                       |
| **Adversary Use of AI-Based Techniques**    | R            | C             | C                    | R                                 | I                        | C                        | I                        | I                 | C           | I                               | -                       |
| **Product Alignment with ATT&CK for AI**    | I            | I             | C                    | I                                 | I                        | C                        | C                        | I                 | I           | C                               | R                       |
| **AI Cybersecurity Investment Prioritization** | I         | I             | I                    | C                                 | I                        | C                        | C                        | C                 | I           | A                               | -                       |
| **AI System Reliability & Observability**   | I            | C             | C                    | C                                 | I                        | C                        | C                        | I                 | R           | A                               | C                       |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)

#### 2.1.3. Guidance provided

The MITRE ATT&CK framework provides a robust foundation for securing AI systems by aligning traditional cybersecurity practices with AI-specific threats. By mapping adversary behaviors, simulating attacks, and enhancing detection capabilities, ATT&CK ensures AI systems are resilient against both known and emerging threats. Organizations can leverage ATT&CK to build a unified, proactive security posture that addresses the unique challenges posed by AI technology.

### 2.2. Detail on current framework

The MITRE ATT&CK framework provides a critical foundation for securing AI systems against emerging threats. AI systems introduce unique vulnerabilities and attack surfaces, such as adversarial inputs, data poisoning, and model theft, which require tailored applications of ATT&CK to ensure comprehensive threat coverage.

AI systems operate in complex environments and are susceptible to both traditional cybersecurity threats and AI-specific attacks. The ATT&CK framework offers a structured approach to:

1. Understand Threats: Map adversary behaviors targeting AI components such as data pipelines, models, APIs, and infrastructure.
2. Enhance Security Posture: Identify and mitigate vulnerabilities in AI systems by applying relevant ATT&CK techniques.
3. Integrate Defense: Bridge gaps between traditional IT security and AI-specific requirements.

***AI-Specific Threats Addressed by ATT&CK***

| **Category**         | **Threat**                                               | **Relevant ATT&CK Techniques**                     |
|-----------------------|----------------------------------------------------------|----------------------------------------------------|
| **Data-Related**      | Data poisoning to degrade AI model performance.          | Data Manipulation (T1565), Data Destruction (T1485) |
|                       | Data exfiltration from AI datasets or inference systems. | Exfiltration Over Web Service (T1567), Automated Exfiltration (T1020) |
| **Model-Specific**    | Adversarial inputs misleading AI predictions.            | Command and Scripting Interpreter (T1059), Exploit Public-Facing Applications (T1190) |
|                       | Model theft through reverse engineering or inference.    | Credential Dumping (T1003), Application Layer Protocol (T1071) |
| **Infrastructure**    | Resource hijacking for unauthorized use (e.g., cryptomining). | Resource Hijacking (T1496), Cloud Service Exploitation (T1586) |
|                       | API exploitation leading to malicious actions.           | Input Capture (T1056), API Abuse (T1555) |
| **Lifecycle Threats** | Reconnaissance for vulnerable AI components.             | Gather Victim Network Information (T1590) |
|                       | Manipulation of AI outputs to disrupt operations.        | Data Manipulation (T1565), Service Stop (T1489) |


***Application of ATT&CK Tactics to AI Systems***

| **Tactic**            | **Description**                                            | **Example Technique**                              |
|------------------------|------------------------------------------------------------|---------------------------------------------------|
| **Reconnaissance**     | Discovering weak points in AI workflows.                   | Gather Victim Network Information (T1590)         |
| **Initial Access**     | Exploiting APIs or supply chain vulnerabilities.           | Exploit Public-Facing Applications (T1190)        |
| **Execution**          | Triggering malicious actions via adversarial inputs.       | Command and Scripting Interpreter (T1059)         |
| **Persistence**        | Maintaining access to AI systems.                         | Account Manipulation (T1098)                      |
| **Exfiltration**       | Stealing datasets, models, or outputs.                     | Exfiltration Over Web Service (T1567)             |
| **Impact**             | Manipulating functionality or disrupting AI operations.    | Data Manipulation (T1565), Service Stop (T1489)   |


***Integration of ATT&CK into AI Security Lifecycle***

| **Step**               | **Description**                                          | **Example**                                                   |
|-------------------------|----------------------------------------------------------|--------------------------------------------------------------|
| **Asset Identification** | Inventory and categorize AI-related assets.              | Identify datasets, ML models, APIs, and supporting infrastructure. |
| **ATT&CK Mapping**       | Map tactics and techniques to AI vulnerabilities.        | Link "Model Evasion" to "Defense Evasion" and Input Injection. |
| **Threat Simulation**    | Simulate real-world adversary behaviors.                 | Test adversarial input attacks or model theft scenarios.      |
| **Continuous Monitoring** | Monitor for adversarial behaviors using ATT&CK-aligned analytics. | Detect adversarial inputs or unauthorized API access.          |
| **Incident Management**  | Develop playbooks for AI-specific incidents.             | Retrain poisoned models or revoke exploited APIs.             |



### 2.3. What is missing for defenders of AI systems

While the MITRE ATT&CK framework provides a robust structure for addressing traditional cybersecurity threats, it lacks several critical elements specific to the unique challenges posed by AI systems. Those gaps are covered by MITRE ATLAS Framework.

***Challenges and Limitations of ATT&CK for AI Systems***

| **Challenge**           | **Description**                                                        |
|--------------------------|------------------------------------------------------------------------|
| **Dynamic Threat Landscape** | AI systems and adversaries evolve rapidly, requiring continuous updates to ATT&CK. |
| **Complexity of Mapping**     | Deep expertise in both cybersecurity and AI is needed for effective ATT&CK mapping. |
| **Operational Integration**   | Customization is required to integrate ATT&CK into existing workflows for AI security. |


## 2. ATLAS

### 2.1. Overview

The MITRE Adversarial Threat Landscape for AI Systems (ATLAS) is a knowledge base designed to address threats to AI-enabled systems. It documents adversary tactics, techniques, and real-world attack observations while complementing the MITRE ATT&CK framework.

While MITRE ATT&CK remains the framework for traditional cybersecurity and adversary behaviors, MITRE ATLAS extends this model into the AI domain. ATLAS focuses on the unique adversarial threats faced by AI systems, such as model poisoning, prompt injection, and evasion attacks, complementing the capabilities of ATT&CK for a holistic view of modern cyber and AI threats.

ATLAS serves as a critical tool for understanding, simulating, and mitigating threats to AI systems. It helps stakeholders (e.g., analysts, developers, and defenders) prepare for AI-specific security challenges through shared knowledge and practical tools.

#### 2.1.1. Scoping of AI system and/or cybersecurity purview

#### 2.1.2. Persona addressed

#### 2.1.3. Guidance provided

### 2.2. Detail on current framework

### 2.3. What is missing for defenders of AI systems


## 3. CAPEC

### 2.1. Overview

#### 2.1.1. Scoping of AI system and/or cybersecurity purview

#### 2.1.2. Persona addressed

#### 2.1.3. Guidance provided

### 2.2. Detail on current framework

### 2.3. What is missing for defenders of AI systems