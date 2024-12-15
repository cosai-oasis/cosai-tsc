# NIST

## 1. Cybersecurity Framework

### 1.1. NIST CSF 2.0

#### 1.1.1. Overview

The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, is a flexible and non-prescriptive framework designed to help organizations manage cybersecurity risks effectively. It applies to entities of all sizes and across sectors, various missions, technologies (including AI), and regulatory environments, integrating cybersecurity with enterprise risk management.

##### 1.1.1.1. Scoping of AI system and/or cybersecurity purview

The NIST CSF 2.0 provides a flexible structure for scoping cybersecurity efforts, including AI systems, by integrating governance, risk management, and technical safeguards into a unified framework.

*By using the NIST CSF 2.0, organizations can effectively:*

1. *Define and document the scope of AI systems, aligning with organizational risk management practices.*
2. *Ensure that cybersecurity safeguards and monitoring mechanisms address the unique challenges of AI technologies.*
3. *Establish clear roles and responsibilities for managing risks associated with AI and other scoped systems.*
4. *Continuously improve scoping practices to adapt to emerging threats, technologies, and regulatory changes.*

##### 1.1.1.2. Persona addressed

| Responsibilities | CEO | CTO | CISO | Program & Project Manager | Infrastructure Maintainer | AI Practitioner | Data Analyst | Data Scientist | ML Researcher | SW Architect | SW Engineer | Model Maintainer | SRE/DevOps | Security Architect | Security Analyst | Security Focal |
| :---: | :---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |:---: |
| **Govern (GV)**  | I | I | I/A | I/A | R |  |  |  |  | C/R |  |  | R | A/C |  | R |
| **Identify (ID)** | I | I | I/A | I/A |  |  |  |  |  | A/C/R |  |  |  | A/C/R |  | R |
| **Protect (PR)** | I | I | I/A | I/A | R | R | R | R | C/R | R | R | R | R | A/C |  | C |
| **Detect (DE)** | I | I | I/A | I/A |  |  |  |  |  | C/R |  |  | R | A/C | R | C |
| **Respond (RS)** | I | I | I/A | I/A |  |  |  |  |  | C/R |  |  |  | A/C | R | C |
| **Recover (RC)** | I | I | I/A | I/A | R |  |  |  |  | C/R | R |  | R | A/C |  | C |

##### 1.1.1.3. Guidance provided

The NIST Cybersecurity Framework (CSF) 2.0 provides guidance for organizations to manage cybersecurity risks effectively and integrate cybersecurity practices with broader enterprise risk management strategies. 

The NIST CSF 2.0 serves as a foundational tool to:

1. Standardize cybersecurity practices across organizations, sectors, and regions.
2. Integrate cybersecurity into business strategies and risk management frameworks.
3. Adapt to emerging challenges in technology, supply chains, and global threats.
4. Foster a culture of proactive risk management and continuous improvement.

#### 1.1.2. Detail on current framework

CSF consists of three core sections:

1. ***CSF Core:*** A hierarchy of cybersecurity outcomes categorized into six Functions: Govern, Identify, Protect, Detect, Respond, and Recover.
2. ***Profiles:*** Mechanisms to describe an organization's current and target cybersecurity postures.
3. ***Tiers:*** Four levels (Partial, Risk Informed, Repeatable, Adaptive) for evaluating the rigor of cybersecurity governance and risk management.
   


##### 1.1.2.1. CSF functions and key concepts applicable to scoping AI systems #####


***1. Govern (GV): Defining Scope and Strategy***

| Function | Details |
| --- | --- |
| **GV.OC (Organizational Context)** | 1. Understand the mission and objectives of the AI system. |
| | 2. Assess internal and external stakeholders expectations, such as customers or regulatory bodies. |
| | 3. Document legal, regulatory, and contractual requirements related to AI systems, such as GDPR or AI-specific laws. |
| **GV.RM (Risk Management Strategy)** | 1. Define the organization's risk appetite and tolerance specific to AI and cybersecurity risks. |
| | 2. Develop a strategy to address risks from AI systems, such as adversarial attacks, model drift, and data poisoning. |
| | 3. Align AI system goals with broader enterprise risk management (ERM) strategies. |
| **GV.SC (Supply Chain Risk Management)** | 1. Integrate supply chain considerations for AI, such as third-party datasets, pre-trained models, and cloud services. |
| | 2. Establish roles, responsibilities, and contractual requirements with suppliers managing AI components. |


***2. Identify (ID): Mapping Scope and Risks***

| Function | Details |
| --- | --- |
| **ID.AM (Asset Management)*** | 1. Create an inventory of AI system components, including data sources, algorithms, hardware, and cloud services. |
|  | 2. Maintain a list of critical assets across the cybersecurity domain, ensuring dependencies are mapped. |
| **ID.RA (Risk Assessment)** | 1. Assess potential threats to the AI system, such as adversarial manipulation or data breaches. |
| | 2. Evaluate vulnerabilities in AI lifecycle stages (e.g., training, deployment) and external dependencies. |
| | 3. Quantify the likelihood and impact of risks, such as model exploitation or ethical violations. |
| **ID.IM (Improvement)** | 1. Use lessons learned from AI system incidents or evaluations to refine scoping. |
| | 2. Identify gaps in cybersecurity coverage or governance that impact AI-specific risks. |



***3. Protect (PR): Defining Safeguards Within Scope***

| Function | Details |
| --- | --- |
| **PR.AA (Identity Management and Access Control)** | 1. Enforce access controls to safeguard AI models, training data, and outputs. |
| | 2. Ensure identity management practices for users accessing AI systems are robust. |
| **PR.DS (Data Security)** | 1. Protect AI data at rest, in transit, and in use from unauthorized access and tampering. |
| | 2. Secure sensitive datasets used for training and inference processes. |
| **PR.PS (Platform Security)** | 1. Implement secure configurations for AI infrastructure, including cloud environments and hardware accelerators. |
| | 2. Prevent unauthorized software installation or execution within AI pipelines. |


***4. Detect (DE): Monitoring for Threats***


| Function | Details |
| --- | --- |
| **DE.CM (Continuous Monitoring)** | 1. Monitor AI system performance for anomalies, such as adversarial inputs or unexpected outputs. |
| | 2. Track network activity and system logs for indicators of compromise in AI components. |
| **DE.AE (Adverse Event Analysis)** | 1. Analyze anomalies in AI behavior to determine root causes, such as training data corruption or adversarial manipulation. |
| | 2. Correlate information from multiple sources, including threat intelligence, to understand incidents affecting AI systems. |


***5. Respond (RS): Taking Action Within Scope***


| Function | Details |
| --- | --- |
| **RS.MA (Incident Management)** | 1. Execute incident response plans for AI-related events, such as data breaches or system exploitation. |
| | 2. Coordinate responses with external stakeholders, including cloud providers and AI model vendors. |
| **RS.CO (Incident Communication)** | 1. Communicate incident details to internal teams, partners, and customers to mitigate downstream impacts. |
| | 2. Share lessons learned with stakeholders to improve future scoping efforts. |


***6. Recover (RC): Post-Incident Adjustments***


| Function | Details |
| --- | --- |
| **RC.RP (Incident Recovery Plan Execution)** | 1. Restore AI systems to operational status while ensuring the integrity of restored components, such as data and models. |
| | 2. Validate backups before using them for recovery to avoid reintroducing vulnerabilities. |
| **RC.CO (Incident Recovery Communication)** | 1. Inform stakeholders about recovery progress and measures taken to prevent recurrence. |
| | 2. Update scoping documents and risk assessments based on lessons learned. |



#### 1.1.3. What is missing for defenders of AI systems

The NIST CSF 2.0 provides a strong general framework but could be enhanced for AI system defenders by:

1. Incorporating AI-specific risks, such as adversarial attacks, model drift, and poisoning.
2. Addressing supply chain vulnerabilities unique to AI.
3. Providing detailed guidance for AI-focused incident response, recovery, and monitoring.
4. Integrating AI ethics, explainability, and transparency into governance practices.
5. Explicitly aligning with NIST AI RMF for a holistic approach to AI risk management.


### 1.2. NIST RMF

#### 1.2.1. Overview

##### 1.2.1.1. Scoping of AI system and/or cybersecurity purview

##### 1.2.1.2. Persona addressed

##### 1.2.1.3. Guidance provided

#### 1.2.2. Detail on current framework

#### 1.2.3. What is missing for defenders of AI systems

## 2. AI Risk Management Framework

### 2.1. NIST AI RMF 1.0

#### 2.1.1. Overview

##### 2.1.1.1. Scoping of AI system and/or cybersecurity purview

##### 2.1.1.2. Persona addressed

##### 2.1.1.2. Guidance provided

#### 2.1.2. Detail on current framework

#### 2.1.3. What is missing for defenders of AI systems

### 2.2. NIST AI RMF 1.0 for Generative AI (GAI)

#### 2.2.1. Overview

##### 2.2.1.1. Scoping of AI system and/or cybersecurity purview

##### 2.2.1.2. Persona addressed

##### 2.2.1.3. Guidance provided

#### 2.2.2. Detail on current framework

#### 2.2.3. What is missing for defenders of AI systems

### 2.3. NIST AI Adversarial Machine Learning (AML)

#### 2.3.1. Overview

##### 2.3.1.1. Scoping of AI system and/or cybersecurity purview

##### 2.3.1.2. Persona addressed

##### 2.3.1.3. Guidance provided

#### 2.3.2. Detail on current framework

#### 2.3.3. What is missing for defenders of AI systems

