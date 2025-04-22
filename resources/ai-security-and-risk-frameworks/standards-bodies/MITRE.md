<!-- TOC start -->

- [MITRE](#mitre)
  - [1. MITRE ATT\&CK](#1-mitre-attck)
    - [1.1. Overview](#11-overview)
    - [1.2. Scoping of AI system and/or cybersecurity purview](#12-scoping-of-ai-system-andor-cybersecurity-purview)
    - [1.3. Persona addressed](#13-persona-addressed)
    - [1.4. Guidance provided](#14-guidance-provided)
    - [1.5. Detail on current framework](#15-detail-on-current-framework)
    - [1.6. What is missing for defenders of AI systems](#16-what-is-missing-for-defenders-of-ai-systems)
  - [2. MITRE ATLAS](#2-mitre-atlas)
    - [2.1. Overview](#21-overview)
    - [2.2. Scoping of AI system and/or cybersecurity purview](#22-scoping-of-ai-system-andor-cybersecurity-purview)
    - [2.3. Persona addressed](#23-persona-addressed)
    - [2.4. Guidance provided](#24-guidance-provided)
    - [2.5. Detail on current framework](#25-detail-on-current-framework)
    - [2.6. What is missing for defenders of AI systems](#26-what-is-missing-for-defenders-of-ai-systems)
  - [3. MITRE CAPEC](#3-mitre-capec)
    - [3.1. Overview](#31-overview)
    - [3.2. Scoping of AI system and/or cybersecurity purview](#32-scoping-of-ai-system-andor-cybersecurity-purview)
    - [3.3. Persona addressed](#33-persona-addressed)
    - [3.4. Guidance provided](#34-guidance-provided)
    - [3.5. Detail on current framework](#35-detail-on-current-framework)
    - [3.6. What is missing for defenders of AI systems](#36-what-is-missing-for-defenders-of-ai-systems)
  - [4. MITRE D3FEND](#4-mitre-d3fend)
    - [4.1. Overview](#41-overview)
    - [4.2. Scoping of AI system and/or cybersecurity purview](#42-scoping-of-ai-system-andor-cybersecurity-purview)
    - [4.3. Persona addressed](#43-persona-addressed)
    - [4.4. Guidance provided](#44-guidance-provided)
    - [4.5. Detail on current framework](#45-detail-on-current-framework)
    - [4.6. What is missing for defenders of AI systems](#46-what-is-missing-for-defenders-of-ai-systems)
  - [5. References](#5-references)

<!-- TOC end -->

# MITRE

## 1. MITRE ATT&CK

### 1.1. Overview

The MITRE ATT&CK framework is a globally recognized, open-source knowledge base that documents real-world adversary tactics, techniques, and procedures (TTPs) across the cyber-attack lifecycle. It organizes adversary behaviors into tactics (the high level goals attackers intend to achieve), techniques/sub-techniques (the specific methods to accomplish those goals), and procedures (the detailed steps an adversary would take to implement the technique). The TTPs are mapped into an intuitive matrix that spans multiple domains, including enterprise, mobile, cloud, and industrial control systems (ICS). Originally focused on post-attack activities, it now also includes early-stage attacker actions like reconnaissance. 

ATT&CK serves as a practical tool for red teaming, behavioral analytics, threat intelligence enrichment, and defensive gap assessments, linking techniques to adversary groups, software, and mitigations. It provides a practical, data-driven guide to strengthening defenses against real-world threats. Of note, entries in ATT&CK are drawn from publicly reported incidents or offensive research, so that the model is grounded in real-world threats and not theoretical techniques with limited utility. 


### 1.2. Scoping of AI system and/or cybersecurity purview

The MITRE ATT&CK framework provides a structured approach for identifying, analyzing, and addressing threats in AI systems and cybersecurity. Scoping ATT&CK for AI systems involves adapting the framework's tactics and techniques to the unique aspects of AI, while integrating it into the broader cybersecurity purview.

***Components of AI Systems and Relevant ATT&CK Techniques***

| **Component**       | **Description**                                                  | **Relevant ATT&CK Techniques**                     |
|----------------------|------------------------------------------------------------------|----------------------------------------------------|
| **Data Pipeline**    | Protect data integrity, ensure secure collection and storage.   | Data Destruction (T1485), Data Manipulation (T1565) |
| **ML Models**        | Safeguard against adversarial attacks and model theft.          | Exploitation for Defense Evasion (T1211) |
| **APIs and Interfaces** | Secure endpoints and prevent injection attacks.                | Exploit Public-Facing Applications (T1190) |
| **Infrastructure**   | Secure cloud, edge, and on-prem systems hosting AI.             | Resource Hijacking (T1496), Compromise Accounts (T1586) |


---

***ATT&CK Tactics in Cybersecurity Purview***

| **Tactic**            | **Description**                                                                  | **Relevant Techniques**                                       |
|------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------|
| **Initial Access**     | Methods used to gain unauthorized access to AI systems.                         | Phishing (T1566), Supply Chain Compromise (T1195), Valid Accounts (T1078) |
| **Defense Evasion**    | Hiding malicious activity or bypassing defenses.                                | Indicator Removal (T1070), Impair Defenses (T1562) |
| **Privilege Escalation** | Techniques to gain elevated permissions in AI systems.                         | Exploitation for Privilege Escalation (T1068), Abuse Elevation Control Mechanism (T1548) |
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

### 1.3. Persona addressed

***Target Audience***

+ **CISO/SSO:** Strategic threat intelligence integration.
+ **Security Architects:** Adversarial AI threat modeling and defense design.
+ **SOC Operations:** Real-time threat detection, hunting, and incident response.
+ **Researchers/Data Scientists:** Adversarial AI research and TTPs (Tactics, Techniques, Procedures).


<br><br>

***Roles and Activities***

| **Activity**                                | **Executives** | **CISO/SSO** | **Service Architects** | **IT Architects** | **Security Architects** | **IT Operations** | **SOC Operations** | **Service Operations** | **Auditors/Policy Makers** | **Researchers/Data Scientists** | **Users/Practitioners** |
|---------------------------------------------|---------------|--------------|----------------------|---------------|------------------|---------------|---------------|------------------|-----------------------|----------------------------|------------------|
| Threat Intelligence & Analysis          | I             | **A**            | C                    | C             | R                | -             | C             | -                | I                     | R                          | -                |
| Adversary Emulation & Red Teaming       | I             | **A**            | C                    | C             | R                | -             | R             | -                | -                     | C                          | -                |
| Threat Detection & Monitoring           | I             | **A**            | C                    | R             | R                | C             | R             | C                | I                     | C                          | -                |
| Incident Response & Containment         | I             | R            | C                    | C             | **A**                | C             | R             | R                | -                     | -                          | -                |
| Security Architecture & Design          | I             | **A**            | R                    | R             | R                | -             | -             | -                | -                     | C                          | -                |
| Risk Assessment & Mitigation Planning   | **A**             | R            | C                    | C             | R                | -             | -             | -                | **A**                     | C                          | -                |
| Defensive Gap Assessment                | I             | R            | C                    | C             | **A**                | -             | R             | -                | I                     | C                          | -                |
| SOC Maturity Assessment                 | I             | **A**            | -                    | -             | R                | C             | R             | -                | I                     | -                          | -                |
| Policy & Compliance Mapping             | **A**             | R            | -                    | -             | C                | -             | -             | -                | C                     | -                          | -                |
| Security Awareness & Training           | **A**             | R            | C                    | -             | C                | C             | C             | C                | **A**                     | -                          | R                |
| AI/ML Security Integration              | I             | R            | C                    | R             | R                | -             | -             | -                | I                     | **A**                          | -                |
| Vulnerability & Patch Management        | I             | R            | C                    | C             | R                | **A**             | R             | -                | I                     | -                          | -                |
| Auditing & Regulatory Compliance        | I             | R            | -                    | -             | R                | -             | -             | -                | **A**                     | -                          | -                |
| User Access & Identity Management       | I             | R            | C                    | C             | R                | **A**             | -             | C                | I                     | -                          | R                |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement

### 1.4. Guidance provided

The MITRE ATT&CK framework provides a robust foundation for securing AI systems by aligning traditional cybersecurity practices with AI-specific threats. By mapping adversary behaviors, simulating attacks, and enhancing detection capabilities, ATT&CK ensures AI systems are resilient against both known and emerging threats. Organizations can leverage ATT&CK to build a unified, proactive security posture that addresses the unique challenges posed by AI technology.


### 1.5. Detail on current framework

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
| **Model-Specific**    | Adversarial inputs misleading AI predictions.            | Exploitation for Defense Evasion (T1211) |
|                       | Model theft through reverse engineering or inference.    | Exploit Public-Facing Applications (T1190) |
| **Infrastructure**    | Resource hijacking for unauthorized use (e.g., cryptomining). | Resource Hijacking (T1496), Compromise Accounts (T1586) |
|                       | API exploitation leading to malicious actions.           | Exploitation of Remote Services (T1210) |
| **Lifecycle Threats** | Reconnaissance for vulnerable AI components.             | Gather Victim Network Information (T1590) |
|                       | Manipulation of AI outputs to disrupt operations.        | Service Stop (T1489), Endpoint Denial of Service (T1499) |


***Application of ATT&CK Tactics to AI Systems***

| **Tactic**            | **Description**                                            | **Example Technique**                              |
|------------------------|------------------------------------------------------------|---------------------------------------------------|
| **Reconnaissance**     | Discovering weak points in AI workflows.                   | Gather Victim Network Information (T1590)         |
| **Initial Access**     | Exploiting APIs or supply chain vulnerabilities.           | Exploit Public-Facing Applications (T1190)        |
| **Execution**          | Triggering malicious actions via adversarial inputs.       | Exploitation of Remote Services (T1210)        |
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



### 1.6. What is missing for defenders of AI systems

While the MITRE ATT&CK framework provides a robust structure for addressing traditional cybersecurity threats, it lacks several critical elements specific to the unique challenges posed by AI systems. Those gaps are covered by MITRE ATLAS Framework.

***Challenges and Limitations of ATT&CK for AI Systems***

| **Challenge**           | **Description**                                                        |
|--------------------------|------------------------------------------------------------------------|
| **Dynamic Threat Landscape** | AI systems and adversaries evolve rapidly, requiring continuous updates to ATT&CK. |
| **Complexity of Mapping**     | Deep expertise in both cybersecurity and AI is needed for effective ATT&CK mapping. |
| **Operational Integration**   | Customization is required to integrate ATT&CK into existing workflows for AI security. |


## 2. MITRE ATLAS

### 2.1. Overview

The MITRE Adversarial Threat Landscape for Artificial-Intelligence Systems (ATLAS) is a knowledge base designed to address threats to AI-enabled systems. It documents adversary tactics, techniques, and real-world attack observations while complementing the MITRE ATT&CK framework.

While MITRE ATT&CK remains the framework for traditional cybersecurity and adversary behaviors, MITRE ATLAS extends this model into the AI domain. ATLAS focuses on the unique adversarial threats faced by AI systems, such as model poisoning, prompt injection, and evasion attacks, complementing the capabilities of ATT&CK for a holistic view of modern cyber and AI threats. Like ATT&CK, ATLAS focuses on real-world documented threats rather than theoretical attacks

ATLAS serves as a critical tool for understanding, simulating, and mitigating threats to AI systems. It helps stakeholders (e.g., analysts, developers, and defenders) prepare for AI-specific security challenges through shared knowledge and practical tools.


### 2.2. Scoping of AI system and/or cybersecurity purview

Scoping an AI system within the ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) framework involves identifying the unique components, vulnerabilities, and threats across its lifecycle. This also includes defining the boundaries of cybersecurity purview to secure the AI ecosystem comprehensively. 

***Components to Include***

| **Component**         | **Description**                                                                 | **Risks**                                           |
|------------------------|---------------------------------------------------------------------------------|----------------------------------------------------|
| **Data Pipelines**     | Sources of training and inference data, preprocessing, storage, and management. | Data poisoning, unauthorized access, exfiltration. |
| **Model Training and Development** | Machine learning models and workflows for training and validation.             | Adversarial attacks, algorithm manipulation.       |
| **Inference Systems**  | APIs, endpoints, and real-time decision-making systems.                         | Adversarial inputs, API abuse, output manipulation.|
| **Infrastructure**     | Hosting environments (cloud, edge, on-prem) and AI libraries/frameworks.        | Misconfigured services, resource hijacking, tampering. |

---

***Threat Landscape***

| **Threat Category**      | **Description**                                                              |
|---------------------------|------------------------------------------------------------------------------|
| **Adversarial Techniques** | Targeted attacks like adversarial examples or model evasion.                |
| **Reconnaissance**        | Discovering vulnerable AI systems, datasets, or APIs.                       |
| **Exfiltration and Theft**| Stealing intellectual property such as models or sensitive data.             |
| **Impact Tactics**        | Manipulating outputs to disrupt operations or mislead decision-making.       |

---

***Security Domains***

| **Domain**           | **Description**                                                                 | **Risks**                                           |
|-----------------------|---------------------------------------------------------------------------------|----------------------------------------------------|
| **Data Security**     | Secure collection, preprocessing, storage, and access to datasets.              | Data poisoning, unauthorized modification, or theft. |
| **Model Security**    | Protect models from adversarial inputs, reverse engineering, and theft.          | Compromised outputs, model tampering.              |
| **Endpoint/API Security** | Secure interfaces and APIs exposed to external systems.                     | Input validation bypass, API abuse.               |
| **Infrastructure Security** | Protect hosting environments like cloud, edge, and on-prem.               | Misconfigurations, resource hijacking, unauthorized access. |

---

***Defensive Capabilities***

| **Capability**           | **Description**                                                             | **Example Actions**                                 |
|---------------------------|-----------------------------------------------------------------------------|----------------------------------------------------|
| **Monitoring and Detection** | Establish pipelines to monitor model behavior and inference anomalies.    | Use logs, telemetry, and AI-enhanced tools.        |
| **Mitigation and Response**  | Develop playbooks to handle AI-specific incidents like data poisoning.    | Retrain models, revoke API access, patch issues.   |

---

***Organizational Roles***

| **Role**                 | **Responsibilities**                                                        | **Key Activities**                                 |
|---------------------------|-----------------------------------------------------------------------------|----------------------------------------------------|
| **Cross-Disciplinary Teams** | Collaboration between AI engineers, security teams, and risk managers.   | Define security boundaries, review AI risks.       |
| **Red and Blue Teams**     | Test resilience using adversarial attack scenarios.                        | Conduct red/blue team exercises specific to AI.    |
| **Regulatory Alignment**   | Ensure compliance with AI regulations and ethical standards.               | Align practices with EU AI Act, NIST AI RMF, etc.  |

---

### 2.3. Persona addressed

***Target Audience***

+ **CISO/SSO:** Strategic threat intelligence integration.
+ **Security Architects:** Adversarial AI threat modeling and defense design.
+ **SOC Operations:** Real-time threat detection, hunting, and incident response.
+ **Researchers/Data Scientists:** Adversarial AI research and TTPs (Tactics, Techniques, Procedures).


<br><br>

***Roles and Activities***

| **Activity**                    | **Executives** | **CISO/SSO** | **Service Architects** | **IT Architects** | **Security Architects** | **IT Operations** | **SOC Operations** | **Service Operations** | **Auditors/Policy Makers** | **Researchers/Data Scientists** | **Users/Practitioners** |
|--------------------------------------|--------------|--------------|----------------------|--------------|--------------------|--------------|--------------|------------------|----------------------|------------------------|------------------|
| Identify AI systems and assets       | I            | **A**            | R                    | C            | C                  | I            | -            | -                | -                      | C                      | -                |
| Perform AI threat assessments        | I            | **A**            | C                    | -            | R                  | I            | R            | -                | I                      | C                      | -                |
| Implement data integrity measures    | I            | **A**            | C                    | R            | R                  | R            | R            | R                | I                      | C                      | -                |
| Develop adversarial detection        | I            | **A**            | -                    | -            | R                  | C            | R            | -                | -                      | C                      | -                |
| Conduct adversarial red teaming      | I            | **A**            | -                    | -            | C                  | -            | R            | -                | -                      | C                      | -                |
| Establish monitoring and logging     | I            | **A**            | C                    | R            | R                  | R            | R            | R                | -                      | -                      | -                |
| Create AI security mitigation plans  | I            | **A**            | C                    | C            | R                  | -            | C            | -                | I                      | C                      | -                |
| Document and share AI incidents      | I            | **A**            | C                    | -            | R                  | I            | R            | -                | C                      | C                      | I                |
| Maintain ATLAS framework updates     | I            | **A**            | -                    | -            | R                  | -            | R            | -                | -                      | R                      | -                |
| Train staff on ATLAS principles      | R            | **A**            | -                    | -            | C                  | -            | R            | R                | I                      | C                      | I                |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement



### 2.4. Guidance provided

ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) provides comprehensive guidance for defending AI systems by addressing unique threats such as data poisoning, adversarial inputs, model theft, API exploitation, and AI misuse. It extends the MITRE ATT&CK framework with AI-specific tactics, techniques, and procedures (TTPs), emphasizing the need to secure AI across its lifecycle—from data preparation and model training to inference and operation. 

ATLAS advocates for robust detection and mitigation strategies, including behavioral analytics, adversarial robustness testing, and strict access controls, while integrating AI into red and blue team exercises and enhancing threat intelligence. It also highlights the importance of securing AI supply chains, protecting pre-trained models and frameworks, and addressing cross-domain risks in cloud, edge, and IoT environments. 


### 2.5. Detail on current framework

The design and structure of MITRE ATLAS reflect its commitment to providing a comprehensive, adaptable framework for addressing adversarial threats to AI systems. Its integration of tactics, techniques, and real-world procedures, combined with a focus on tools and mitigations, ensures its utility across diverse AI environments. By targeting the unique vulnerabilities of AI systems, ATLAS serves as both a practical resource and a strategic guide for securing the next generation of intelligent technologies.

**ATLAS Matrix**

The ATLAS Matrix provides a visual representation of adversary tactics and techniques, similar to the ATT&CK Matrix but adapted for AI systems. It organizes:

1. Tactics as the top-level categories (e.g., Data Poisoning, Evasion, Extraction).
2. Techniques under each tactic as actionable adversary behaviors.
3. Links to Procedures that document real-world use cases and observed attacks.


**Core Components**

The ATLAS Framework is organized into components that reflect the adversarial threat landscape of AI systems. These components include Tactics, Techniques, and Procedures (TTPs) and are designed to capture adversary behavior in both training and inference stages.

***Tactics***

Tactics represent adversary goals and are categorized to address the unique operational aspects of AI systems. Each tactic defines a specific objective the adversary seeks to achieve. AI-Specific Tactics include:

| **Tactic**              | **Description**                                                                                  |
|--------------------------|-------------------------------------------------------------------------------------------------|
| **Data Poisoning**       | Manipulating training datasets to degrade model performance or introduce malicious behavior.   |
| **Evasion**              | Designing adversarial inputs to mislead AI models into producing incorrect outputs.            |
| **Extraction**           | Stealing sensitive information such as model parameters, architecture, or training data.       |
| **Inversion**            | Recovering private or sensitive information about the model's training data from its outputs.  |
| **Prompt Injection**     | Injecting malicious inputs into large language models (LLMs) to override or manipulate behavior.|
| **Traditional Cyber Tactics** | Using established cyber techniques (e.g., API abuse, credential theft) to target AI systems.  |

---

***Techniques***

Techniques describe the methods adversaries use to achieve their tactical objectives. These are highly specific to the AI domain and reflect the different stages of the AI lifecycle. Each technique may apply to one or more tactics. Examples of Techniques:

| **Technique**                  | **Description**                                                                                       |
|--------------------------------|-------------------------------------------------------------------------------------------------------|
| **Training Data Poisoning**    | Introducing malicious or biased data into the training dataset to degrade model accuracy or integrity. |
| **Adversarial Perturbations**  | Modifying inputs slightly to cause the AI model to produce incorrect predictions or classifications.   |
| **API Abuse**                  | Exploiting AI model APIs to manipulate outputs or extract sensitive data.                             |
| **Model Extraction**           | Reverse engineering or stealing the AI model's parameters or architecture via inference queries.      |
| **Overfitting Exploitation**   | Identifying and exploiting a model's reliance on specific patterns in data to induce errors.           |

---

***Procedures***

Procedures represent real-world adversary actions and implementations of techniques. These are based on observed adversarial behavior and case studies. Examples of Adversary Procedures:

| **Procedure**                 | **Description**                                                                                      |
|-------------------------------|------------------------------------------------------------------------------------------------------|
| **Adversarial Input**         | Designing specific inputs (e.g., images or text) to trick AI models into producing incorrect outputs. |
| **LLM Exploitation**          | Using malicious prompts to force large language models (LLMs) to generate unintended responses.      |
| **Steganographic Poisoning**  | Embedding malicious data within seemingly benign files to influence model behavior during training.  |
| **Environmental Manipulation**| Altering real-world conditions (e.g., light, noise) to confuse AI perception systems.                |
| **Dataset Manipulation**      | Subtly modifying public datasets used for training to introduce vulnerabilities into the final model. |

---

**Attack Surface**

| **Aspect**  | **Description**  | **Examples** |
|-------------|------------------|--------------|
| **AI Access Time**    | Stages of the AI lifecycle where attacks can occur. | **1. Training Phase**: Manipulating training data or configurations. |
|  |  | **2. Inference Phase**: Targeting live AI models to manipulate outputs or extract data. |
| **AI Access Points**  | Interfaces through which adversaries interact with the AI system. | **1. Digital Access**: APIs, web services, file inputs. |
|  |  | **2. Physical Access**: Environmental data like sensor inputs. |
| **System Knowledge**  | Levels of understanding adversaries have about the AI system's internals. | **1. White-box Access**: Full access to model architecture, parameters, and training data. |
|  |  | **2. Black-box Access**: Limited to observing inputs and outputs. |

---


**Threat Mitigation**

ATLAS includes a set of mitigation techniques and security measures to prevent or reduce the impact of adversarial attacks:

| **Mitigation Category**   | **Description**  | **Examples**  |
|---------------------------|------------------|---------------|
| **Data Integrity**         | Ensures that training data is authentic, clean, and robust against manipulation. | 1. Validating data sources. |
|  |  | 2. Removing outliers or malicious entries in datasets. |
| **Adversarial Detection**  | Monitors for unusual input patterns and detects adversarial perturbations. | 1. Deploying anomaly detection systems. |
|  |  | 2. Using input validation mechanisms. |
| **Robust Model Design**    | Improves model resilience through advanced training techniques. | 1. Adversarial training to simulate attack scenarios. |
|  |  | 2. Using defensive distillation methods. |
| **Access Controls**        | Restricts unauthorized access to AI model APIs and infrastructure. | 1. Implementing API key management. |
|  |  | 2. Enforcing strong authentication and rate limiting. |
| **Monitoring and Logging** | Tracks API queries, model behavior, and system usage to detect anomalies or attacks. | 1. Setting up logging for API calls. |
|  |  | 2. Analyzing usage patterns to flag suspicious activities. |

---


### 2.6. What is missing for defenders of AI systems

MITRE ATLAS is a strong framework for understanding adversarial tactics and techniques targeting AI systems, but it needs to evolve to cover specific adversarial techniques, AI supply chain risks, and model behavior. Furthermore, defenders of AI systems would benefit from better integration with broader cybersecurity frameworks. Addressing these gaps would enhance ATLAS's ability to support defenders in securing AI systems against increasingly sophisticated and novel threats.

While ATLAS provides detail on adversarial tactics and techniques, its stated goal is a knowledge base, and does not help defenders prioritize mitigations and countermeasures. Its target audience of developers, incident responders, and security analysts means that it is not easily understood by executives and risk compliance, as it focuses on individual tactics rather than helping make decisions based on a higher level risk management framework.


## 3. MITRE CAPEC

### 3.1. Overview

The Common Attack Pattern Enumeration and Classification (CAPEC) is a standardized, community-driven framework for understanding, categorizing, and mitigating cyber-attack techniques. It provides a structured taxonomy of attack patterns that describe methods attackers use to exploit software systems. While CAPEC is not designed to defend AI systems it is relevant for AI-based systems focused on cybersecurity, as it provides machine-readable, systematic descriptions of attacks that can be used to enhance threat detection, prevention, and response capabilities.


### 3.2. Scoping of AI system and/or cybersecurity purview

CAPEC is not designed to scope cybersecurity of AI system. However it can be very valuable framework to aid building AI based cybersecurity systems.

| **Focus Area**                      | **CAPEC Integration**                                                                                  | **AI Application Examples**                                                                                 |
|------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Proactive Threat Modeling**       | CAPEC supports identifying, simulating, and mitigating attack scenarios during the design phase.      | AI analyzes system design to predict attacks like Phishing (CAPEC-98) and recommend mitigations.        |
| **Dynamic Threat Modeling**         | CAPEC enables real-time threat modeling and attack chain prediction using AI systems.                 | AI dynamically models attack chains (e.g., from Credential Theft to Privilege Escalation).          |
| **SIEM Integration**                | CAPEC patterns help AI-enhanced SIEM tools detect malicious activity by correlating logs with attacks.| AI flags network traffic anomalies based on CAPEC-defined patterns like HTTP Response Splitting (CAPEC-34). |
| **SOAR Platforms**                  | AI-driven SOAR systems automate threat response workflows based on CAPEC attack metadata.             | AI automates response playbooks for attacks such as SQL Injection (CAPEC-66) based on CAPEC severity.   |
| **Endpoint Detection and Response** | CAPEC attack descriptions guide AI-based endpoint analysis to detect malicious activity.              | AI identifies and mitigates Malware Execution (CAPEC-175) on endpoints.                                 |
| **Threat Intelligence Enrichment**  | CAPEC integrates with threat intelligence frameworks like STIX/TAXII to enrich data with attack info. | AI correlates live threat feeds with CAPEC patterns to detect emerging threats.                             |
| **Threat Actor Profiling**          | CAPEC patterns assist AI systems in analyzing TTPs (Tactics, Techniques, Procedures) of adversaries.  | AI identifies adversarial tactics through attack patterns like Credential Abuse or Malware Injection.|
| **Predictive Threat Analysis**      | CAPEC attack lifecycle context allows AI to predict emerging threats and preemptively respond.        | AI predicts new attacks based on historical CAPEC data and prioritizes preemptive mitigations.              |


### 3.3. Persona addressed

***Target Audience***

+ **CISO/SSO:** Implementing adversarial defense strategies and security controls informed by CAPEC attack patterns.
+ **Security Architects:** Advanced threat modeling, risk assessment, and security design using CAPEC AI-specific attack patterns.
+ **SOC Operations:** Real-time monitoring, detection, and incident response for adversarial AI attacks.
+ **Researchers/Data Scientists:** Investigating adversarial attack methodologies and developing adversarially robust models.


<br><br>

***Roles and Activities***

| **Task/Activity**                                 | **Executives** | **CISO/SSO** | **Service Architects** | **IT Architects** | **Security Architects** | **IT Operations** | **SOC Operations** | **Service Operations** | **Auditors/Policy Makers** | **Researchers/Data Scientists** | **Users/Practitioners** |
|---------------------------------------------------|---------------|--------------|-----------------------|-------------------|----------------------|----------------|----------------|------------------|----------------------|---------------------------|---------------------|
| Integrate CAPEC into AI Systems               | I             | **A**            | R                     | C                 | C                    | I              | I              | I                | C                      | R                         | I                   |
| Threat Modeling Using CAPEC                   | I             | **A**            | R                     | R                 | R                    | I              | C              | I                | C                      | C                         | -                   |
| Train AI Models with CAPEC Data               | I             | C            | **A**                     | C                 | C                    | -              | I              | R                | -                      | R                         | -                   |
| Identify CAPEC Attack Patterns                | I             | **A**            | R                     | C                 | R                    | -              | R              | I                | C                      | C                         | -                   |
| Automate Threat Detection Using CAPEC         | I             | **A**            | C                     | C                 | R                    | I              | R              | I                | C                      | C                         | -                   |
| Vulnerability Assessment and Simulation       | I             | **A**            | C                     | R                 | R                    | -              | R              | I                | C                      | C                         | -                   |
| Incident Response and Mitigation              | I             | **A**            | -                     | -                 | R                    | I              | R              | I                | C                      | -                         | I                   |
| Maintain and Update CAPEC Data                | I             | C            | C                     | C                 | R                    | -              | R              | I                | **A**                      | R                         | -                   |
| Align CAPEC with Threat Intelligence | I         | **A**            | C                     | R                 | R                    | -              | R              | I                | C                      | C                         | -                   |
| Report CAPEC-Based Threat Insights            | I             | **A**            | C                     | C                 | R                    | -              | R              | I                | R                      | C                         | -                   |
| CAPEC Training and Awareness                  | I             | **A**            | C                     | C                 | R                    | I              | C              | I                | R                      | R                         | I                   |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement


### 3.4. Guidance provided

CAPEC provides a robust foundation for AI systems to improve cybersecurity automation, detection, prediction, and response, making it useful for AI-driven security solutions. However it doesn't provide any guidance for AI systems security.


### 3.5. Detail on current framework

CAPEC provides a comprehensive, structured foundation that AI systems can leverage to detect, analyze, and mitigate cyber-attacks effectively. By combining CAPEC with AI pattern recognition, behavioral analysis, and automation capabilities, organizations can significantly enhance their cybersecurity posture throughout the threat lifecycle.

***CAPEC Features Applicable to AI Systems***

| **Feature**                  | **Description**                                                                 |
|------------------------------|-------------------------------------------------------------------------------|
| **Attack Patterns**          | Reusable descriptions of attack techniques like SQL Injection and XSS.       |
| **Structured Taxonomy**      | Hierarchical classification of attack methods for easy analysis and linking. |
| **Data Integration**         | Works with CWE, CVE, and CybOX to create a comprehensive security framework. |
| **Machine-Readable Format**  | Provides formats suitable for AI systems to perform automated analysis.      |
| **Attack Lifecycle Context** | Includes attack descriptions, preconditions, methods, consequences, and mitigations. |

---

***Applications of CAPEC for AI Systems***

| **Application**                    | **Description**                                                                                   | **Example Use Case**                                                                                 |
|------------------------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| **Training AI Models**             | CAPEC provides high-quality labeled datasets for supervised learning.                            | Train AI to detect SQL Injection or Buffer Overflow using CAPEC data.                              |
| **Attack Pattern Detection**       | AI uses CAPEC to recognize known and evolving attacks by matching observed behaviors.             | Identify HTTP Response Splitting (CAPEC-34) based on network traffic analysis.                     |
| **Threat Modeling and Prediction** | AI predicts potential attack scenarios during software development using CAPEC taxonomy.       | Simulate attacks like phishing or privilege escalation to find exploitable paths.                  |
| **Automated Vulnerability Assessment** | CAPEC helps simulate attack patterns for penetration testing and risk evaluation.               | AI-based scanner tests applications for vulnerabilities like XSS or SQL Injection.                 |
| **Behavioral Analysis and Anomaly Detection** | Detect deviations in system behavior by comparing it to CAPEC-defined attack patterns.         | Flag unusual process executions resembling Buffer Overflow attacks.                                |
| **Incident Classification and Response** | AI classifies incidents and suggests mitigations using CAPEC context (prerequisites, impact).  | Classify an incident as Session Fixation (CAPEC-60) and prioritize countermeasures.                |
| **Attack Chain Analysis**          | AI models the sequence of steps in an attack using CAPEC patterns to predict adversary behavior. | Predict escalation from Phishing (CAPEC-98) to credential theft or lateral movement.               |
| **Real-Time Threat Intelligence**  | CAPEC integrates with live feeds for real-time attack detection and counteractions.              | Correlate threat feeds with CAPEC patterns to detect and block ongoing attacks.                    |


### 3.6. What is missing for defenders of AI systems

CAPEC focuses primarily on traditional software and system vulnerabilities but does not include AI-specific attack patterns. It integrates with CWE, which is focused on general software vulnerabilities but lacks specificity for AI. While CAPEC is well-suited for traditional IT systems but does not sufficiently address emerging AI-specific security domains.

## 4. MITRE D3FEND

### 4.1. Overview

The MITRE D3FEND framework represents a rigorously structured, semantically enriched knowledge base designed to systematically characterize cybersecurity countermeasures in relation to offensive tactics and techniques, as delineated by the MITRE ATT&CK framework. By employing an ontologically grounded knowledge graph, D3FEND elucidates the precise mechanisms by which defensive strategies mitigate adversarial threats, thereby enabling a more nuanced understanding of cybersecurity resilience. Its application extends across security architects, red and blue teams, and threat intelligence analysts, facilitating a more evidence-based, adaptive, and scalable paradigm for cyber threat mitigation and strategic security planning.


### 4.2. Scoping of AI system and/or cybersecurity purview

D3FEND provides a comprehensive scoping framework for securing AI systems within the broader cybersecurity purview. By defining AI-specific security threats, defensive techniques, cybersecurity controls, and governance alignment, D3FEND enables AI security professionals, threat hunters, and enterprise architects to proactively mitigate AI security risks.

As AI security threats continue evolving, D3FEND's structured, adaptive, and machine-readable approach will remain critical in defining, automating, and enforcing AI security best practices across enterprises, governments, and critical infrastructure sectors. 


### 4.3. Persona addressed

***Target Audience***

+ **Security Architects:** Defensive countermeasure design against adversarial AI threats.
+ **SOC Operations:** Implementing and monitoring AI defensive measures.
+ **IT Operations:** Ensuring operational deployment of D3FEND countermeasures.
+ **Service Architects:** Integrating countermeasures into AI service design.


<br><br>

***Roles and Activities***

| Activity  | Executives | CISO/SSO | Service Architects | IT Architects | Security Architects | IT Operations | SOC Operations | Service Operations | Auditors/Policy Makers | Researchers/Data Scientists | Users/Practitioners |
|------------------|------------|-----------|--------------------|--------------|---------------------|--------------|---------------|-----------------|---------------------|------------------------|------------------|
| Define cybersecurity strategy using D3FEND | **A**          | R        | C                  | I            | C                   | I            | I             | I               | C                   | C                      | -                |
| Integrate D3FEND into enterprise security architecture | I          | **A**        | R                  | R            | R                   | C            | I             | I               | C                   | C                      | -                |
| Develop AI security countermeasures using D3FEND | I          | I        | C                  | C            | **A**                   | I            | R             | R               | I                   | R                      | -                |
| Align D3FEND security controls with compliance frameworks | I          | **A**        | C                  | I            | R                   | I            | I             | I               | R                   | C                      | -                |
| Threat modeling and mapping ATT&CK to D3FEND | I          | R        | C                  | C            | **A**                   | I            | R             | C               | C                   | C                      | -                |
| SOC implementation of D3FEND-based monitoring | I          | C        | C                  | C            | **A**                   | I            | R             | C               | I                   | I                      | -                |
| Incident response & investigation using D3FEND | I          | C        | C                  | C            | **A**                   | C            | R             | C               | I                   | I                      | -                |
| AI security risk assessment leveraging D3FEND | C          | R        | C                  | C            | **A**                   | I            | I             | I               | C                   | R                      | -                |
| Implementation of D3FEND security controls in AI models | I          | I        | C                  | R            | **A**                   | R            | I             | C               | C                   | R                      | -                |
| Development of AI security best practices with D3FEND | I          | C        | C                  | C            | **A**                   | C            | C             | C               | **A**                   | R                      | -                |
| Research on AI threat detection and mitigation via D3FEND | I          | I        | I                  | C            | **A**                   | C            | C             | C               | C                   | **A**                      | -                |
| Security awareness and training on D3FEND | **A**          | R        | C                  | C            | R                   | C            | C             | C               | C                   | C                      |  I              |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement


### 4.4. Guidance provided

The MITRE D3FEND framework provides structured defensive cybersecurity guidance that can be directly applied to AI systems, particularly in securing machine learning models, AI-driven decision-making, and autonomous security architectures. Given the unique attack surfaces introduced by AI systems, D3FEND helps organizations map, implement, and automate cybersecurity controls to protect AI models from adversarial attacks, data manipulation, and exploitation.

### 4.5. Detail on current framework

The MITRE D3FEND framework is an ontology-driven cybersecurity knowledge base designed to systematically categorize, relate, and structure cybersecurity countermeasures in a way that is machine-readable, semantically rigorous, and actionable. It complements MITRE ATT&CK by providing a defensive knowledge model that helps security practitioners map, analyze, and implement cybersecurity defenses.

**Core Design Principles**

| **Design Principle**                     | **Description** |
|-------------------------------------------|--------------------------------------------------------------|
| **Semantic Knowledge Representation**    | Uses an ontology-based structure to define cybersecurity countermeasures in a machine-readable format. |
| **Interoperability with ATT&CK**         | Directly maps defensive techniques to adversarial TTPs from MITRE ATT&CK, enabling structured threat defense strategies. |
| **Scalability and Extensibility**        | Designed for continuous updates to incorporate emerging threats, security controls, and AI-driven enhancements. |
| **Vendor-Agnostic Approach**             | Provides a standardized, neutral cybersecurity framework that integrates with SIEMs, SOAR, and compliance frameworks. |
| **Graph-Based Structure**                | Uses knowledge graph principles to model relationships between threats, countermeasures, and security controls. |
| **Machine Learning and AI Readiness**    | Supports AI-driven security automation, anomaly detection, and adversarial machine learning defense strategies. |

**Core Taxonomy**

D3FEND categorizes cybersecurity defensive techniques into structured domains, which define the different layers of security controls.

| **Category**                          | **Description** |
|---------------------------------------|--------------------------------------------------------------|
| **Identity & Access Management**      | Controls related to authentication, authorization, and user identity protection. |
| **Network Security & Traffic Analysis** | Techniques to monitor, filter, and protect network communications from adversarial activity. |
| **Malware Detection & Analysis**      | Methods for identifying and mitigating malicious software and anomalous behaviors. |
| **Data Protection & Encryption**      | Cryptographic and integrity-based methods to secure sensitive data. |
| **Endpoint Security & Hardening**     | Protection mechanisms that secure devices and applications from exploitation. |
| **Security Monitoring & Threat Detection** | Techniques to detect, log, and analyze cybersecurity threats in real time. |


**D3FEND Knowledge Graph**

D3FEND is structured as a graph-based knowledge model, where nodes represent different security concepts, and edges define relationships between them.

***Graph Nodes (Core Entities)***
+ Defensive Techniques  Security measures used to prevent, detect, or mitigate cyber threats.
+ Adversarial Techniques (ATT&CK) - The offensive methods used by attackers to compromise systems.
+ Security Controls - Specific technical implementations of defensive techniques.
+ Security Policies - Organizational security best practices mapped to defensive techniques.
+ Threat Intelligence Artifacts - Indicators of compromise (IOCs), behavioral patterns, and intelligence reports linked to defensive strategies.

***Graph Edges (Relationships)***
+ Mitigates - Links a D3FEND defensive technique to an ATT&CK adversarial technique it counteracts.
+ Implements - Connects a defensive technique to a specific security control.
+ Requires - Defines dependencies between security measures (e.g., MFA requires Identity Management).
+ Enhances - Shows how a technique strengthens another defense (e.g., AI-driven anomaly detection enhances traditional log analysis).
+ Correlates - Establishes links between threat intelligence indicators and defensive techniques.


**Data Model and Schema**

| **Attribute**            | **Description** |
|--------------------------|--------------------------------------------------------------|
| **Technique Name**       | Unique identifier of the defensive technique. |
| **Description**          | Brief summary of the countermeasure and its application. |
| **Mapped ATT&CK Techniques** | List of adversarial techniques that this defensive technique mitigates. |
| **Implementation Details** | Steps required to deploy and configure the technique effectively. |
| **Security Controls**     | Specific technologies or configurations that implement the defensive technique. |
| **Effectiveness**        | Metrics, evidence, and case studies demonstrating the technique's effectiveness. |
| **Data Sources**         | Required logs, telemetry, or forensic artifacts needed for detection and analysis. |


**D3FEND Deployment and Integration**

***Security Architecture Integration***

D3FEND can be used to enhance security architectures by integrating structured defensive knowledge into enterprise security operations:
+ SOC Operations - Improves threat detection and incident response workflows.
+ SIEM & SOAR Platforms - Automates security monitoring by mapping defensive techniques to log sources.
+ Threat Intelligence Platforms - Provides context-aware defensive insights.
+ Zero Trust Security Models - Enables adaptive security measures based on dynamic risk evaluation.

***AI and Machine Learning Applications***

D3FEND is particularly valuable in AI-driven cybersecurity, where it enables:
+ Automated anomaly detection using structured defensive mappings.
+ Adversarial AI defense techniques for machine learning security.
+ Intelligent security automation for self-adaptive cyber defenses.



### 4.6. What is missing for defenders of AI systems

D3FEND is primarily designed for mapping defensive cybersecurity techniques to known adversarial TTPs from MITRE ATT&CK, focusing on traditional cybersecurity defenses rather than AI security. At this point D3FEND does not yet integrate AI-specific threat mappings covered by MITRE ATLAS. There are no current D3FEND techniques explicitly addressing adversarial ML, model robustness, AI compliance, or LLM security, indicating gaps in AI security defense strategies.

| What is Missing?                           | Details |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Comprehensive Adversarial ML Defense      | D3FEND does not currently provide structured defensive techniques for mitigating adversarial ML attacks, including perturbation-based evasion and data poisoning. |
| AI-Specific Threat Intelligence Mapping   | D3FEND lacks mappings to AI-related attack techniques from MITRE ATLAS or AI-specific threat intelligence sources, limiting AI defenders' ability to track adversarial tactics. |
| LLM Security & Prompt Injection Protection | D3FEND does not cover security mechanisms for mitigating prompt injection attacks, adversarial instruction manipulation, or harmful AI-generated outputs in large language models (LLMs). |
| AI Supply Chain Security                  | D3FEND does not define security techniques for verifying AI model provenance, cryptographic signing of AI models, or securing the AI model supply chain. |
| Real-Time AI Model Telemetry & Monitoring | The framework does not provide techniques for continuously monitoring AI model behavior, detecting adversarial drift, or preventing inference manipulation. |
| Model Robustness & Integrity Verification | There are no defined defensive techniques in D3FEND for verifying AI model robustness against adversarial ML attacks, including model evasion and inversion attacks. |
| Secure AI Model Access & API Protections  | D3FEND does not outline access control mechanisms specific to AI models, including protections against API abuse, unauthorized access, and model inversion attacks. |

<br><br>

## 5. References

| Framework | Referenced Material |
| --- | --- |
| MITRE ATT&CK | [MITRE ATT&CK](https://attack.mitre.org/) |
| MITRE ATLAS | [MITRE ATLAS](https://atlas.mitre.org/) |
| MITRE CAPEC | [MITRE CAPEC](https://capec.mitre.org/) |
| MITRE D3FEND | [MITRE D3FEND](https://d3fend.mitre.org/) |
