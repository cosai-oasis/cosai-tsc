<!-- TOC start -->

- [NIST](#nist)
  - [1. Cybersecurity Framework](#1-cybersecurity-framework)
    - [1.1. NIST CSF 2.0](#11-nist-csf-20)
      - [1.1.1. Overview](#111-overview)
        - [1.1.1.1. Scoping of AI system and/or cybersecurity purview](#1111-scoping-of-ai-system-andor-cybersecurity-purview)
        - [1.1.1.2. Persona addressed](#1112-persona-addressed)
        - [1.1.1.3. Guidance provided](#1113-guidance-provided)
      - [1.1.2. Detail on current framework](#112-detail-on-current-framework)
        - [1.1.2.1. CSF functions and key concepts applicable to scoping AI systems](#1121-csf-functions-and-key-concepts-applicable-to-scoping-ai-systems)
      - [1.1.3. What is missing for defenders of AI systems](#113-what-is-missing-for-defenders-of-ai-systems)
    - [1.2. NIST RMF](#12-nist-rmf)
      - [1.2.1. Overview](#121-overview)
        - [1.2.1.1. Scoping of AI system and/or cybersecurity purview](#1211-scoping-of-ai-system-andor-cybersecurity-purview)
        - [1.2.1.2. Persona addressed](#1212-persona-addressed)
        - [1.2.1.3. Guidance provided](#1213-guidance-provided)
      - [1.2.2. Detail on current framework](#122-detail-on-current-framework)
      - [1.2.3. What is missing for defenders of AI systems](#123-what-is-missing-for-defenders-of-ai-systems)
  - [2. AI Risk Management Framework](#2-ai-risk-management-framework)
    - [2.1. NIST AI RMF 1.0](#21-nist-ai-rmf-10)
      - [2.1.1. Overview](#211-overview)
        - [2.1.1.1. Scoping of AI system and/or cybersecurity purview](#2111-scoping-of-ai-system-andor-cybersecurity-purview)
        - [2.1.1.2. Persona addressed](#2112-persona-addressed)
        - [2.1.1.2. Guidance provided](#2112-guidance-provided)
      - [2.1.2. Detail on current framework](#212-detail-on-current-framework)
      - [2.1.3. What is missing for defenders of AI systems](#213-what-is-missing-for-defenders-of-ai-systems)
    - [2.2. NIST AI RMF 1.0 for Generative AI (GAI)](#22-nist-ai-rmf-10-for-generative-ai-gai)
      - [2.2.1. Overview](#221-overview)
        - [2.2.1.1. Scoping of AI system and/or cybersecurity purview](#2211-scoping-of-ai-system-andor-cybersecurity-purview)
        - [2.2.1.2. Persona addressed](#2212-persona-addressed)
        - [2.2.1.3. Guidance provided](#2213-guidance-provided)
      - [2.2.2. Detail on current framework](#222-detail-on-current-framework)
      - [2.2.3. What is missing for defenders of AI systems](#223-what-is-missing-for-defenders-of-ai-systems)
    - [2.3. NIST AI Adversarial Machine Learning (AML)](#23-nist-ai-adversarial-machine-learning-aml)
      - [2.3.1. Overview](#231-overview)
        - [2.2.1.1. Scoping of AI system and/or cybersecurity purview](#2211-scoping-of-ai-system-andor-cybersecurity-purview-1)
        - [2.3.1.2. Persona addressed](#2312-persona-addressed)
        - [2.3.1.3. Guidance provided](#2313-guidance-provided)
      - [2.3.2. Detail on current framework](#232-detail-on-current-framework)
      - [2.3.3. What is missing for defenders of AI systems](#233-what-is-missing-for-defenders-of-ai-systems)
  - [3. References](#3-references)

<!-- TOC end -->

<!-- TOC --><a name="nist"></a>
# NIST

<br><br>

<!-- TOC --><a name="1-cybersecurity-framework"></a>
## 1. Cybersecurity Framework

<br><br>

<!-- TOC --><a name="11-nist-csf-20"></a>
### 1.1. NIST CSF 2.0

<!-- TOC --><a name="111-overview"></a>
#### 1.1.1. Overview

The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, is a flexible and non-prescriptive framework designed to help organizations manage cybersecurity risks effectively. It applies to entities of all sizes and across sectors, various missions, technologies (including AI), and regulatory environments, integrating cybersecurity with enterprise risk management.

<br><br>

<!-- TOC --><a name="1111-scoping-of-ai-system-andor-cybersecurity-purview"></a>
##### 1.1.1.1. Scoping of AI system and/or cybersecurity purview

The NIST CSF 2.0 provides a flexible structure for scoping cybersecurity efforts, including AI systems, by integrating governance, risk management, and technical safeguards into a unified framework.

*By using the NIST CSF 2.0, organizations can effectively:*

1. *Define and document the scope of AI systems, aligning with organizational risk management practices.*
2. *Ensure that cybersecurity safeguards and monitoring mechanisms address the unique challenges of AI technologies.*
3. *Establish clear roles and responsibilities for managing risks associated with AI and other scoped systems.*
4. *Continuously improve scoping practices to adapt to emerging threats, technologies, and regulatory changes.*

<br><br>

<!-- TOC --><a name="1112-persona-addressed"></a>
##### 1.1.1.2. Persona addressed

| **CSF Function / Activity**                | **AI System Owner** | **Cybersecurity Team** | **Data Scientist / AI Engineer** | **Software Development Team** | **SRE Team** | **Software Architecture Team** | **Legal / Compliance Team** | **Executive Leadership** | **External Vendors** |
| ------------------------------------------ | ------------------- | ---------------------- | -------------------------------- | ----------------------------- | ------------ | ------------------------------ | --------------------------- | ------------------------ | -------------------- |
| **Govern (GV)**                            |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Define AI cybersecurity governance scope   | R                   | A                      | C                                | C                             | I            | C                              | C                           | I                        | I                    |
| Establish AI risk management strategy      | A                   | R                      | C                                | C                             | C            | C                              | C                           | I                        | I                    |
| Develop supply chain risk policies for AI  | R                   | C                      | I                                | I                             | I            | C                              | A                           | I                        | R                    |
| Define ethical AI usage guidelines         | A                   | C                      | R                                | C                             | I            | C                              | R                           | I                        | I                    |
| **Identify (ID)**                          |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Inventory AI systems and dependencies      | R                   | C                      | R                                | C                             | C            | C                              | I                           | I                        | C                    |
| Conduct AI-specific risk assessments       | C                   | R                      | A                                | C                             | I            | C                              | C                           | I                        | C                    |
| Map AI data flow and privacy risks         | R                   | C                      | R                                | C                             | I            | C                              | A                           | I                        | I                    |
| Evaluate third-party AI components         | R                   | R                      | C                                | C                             | I            | C                              | I                           | I                        | A                    |
| **Protect (PR)**                           |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Implement access controls for AI systems   | C                   | R                      | C                                | C                             | R            | C                              | I                           | I                        | I                    |
| Secure training data and models            | R                   | R                      | A                                | C                             | C            | C                              | I                           | I                        | I                    |
| Encrypt data in AI pipelines               | I                   | R                      | A                                | C                             | R            | C                              | I                           | I                        | C                    |
| Enforce secure software development        | C                   | R                      | A                                | R                             | C            | A                              | I                           | I                        | R                    |
| **Detect (DE)**                            |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Monitor AI models for adversarial inputs   | C                   | R                      | R                                | I                             | R            | C                              | I                           | I                        | C                    |
| Detect anomalies in AI behavior            | C                   | R                      | A                                | C                             | R            | C                              | I                           | I                        | I                    |
| Monitor AI supply chain for threats        | C                   | R                      | I                                | I                             | C            | C                              | I                           | I                        | R                    |
| Analyze cybersecurity incidents in AI      | R                   | A                      | C                                | I                             | R            | C                              | I                           | I                        | I                    |
| **Respond (RS)**                           |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Activate incident response for AI attacks  | R                   | A                      | C                                | I                             | R            | C                              | C                           | I                        | C                    |
| Mitigate data poisoning or model tampering | C                   | R                      | A                                | C                             | R            | C                              | I                           | I                        | I                    |
| Report AI-related incidents to regulators  | I                   | R                      | C                                | I                             | I            | C                              | A                           | C                        | I                    |
| Share threat intelligence with partners    | C                   | R                      | I                                | I                             | I            | C                              | C                           | I                        | A                    |
| **Recover (RC)**                           |                     |                        |                                  |                               |              |                                |                             |                          |                      |
| Rebuild or retrain compromised models      | R                   | C                      | A                                | C                             | C            | C                              | I                           | I                        | I                    |
| Validate integrity of restored AI systems  | R                   | R                      | C                                | C                             | C            | A                              | I                           | I                        | C                    |
| Communicate recovery progress              | I                   | R                      | C                                | I                             | C            | C                              | C                           | A                        | I                    |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)

<br><br>

<!-- TOC --><a name="1113-guidance-provided"></a>
##### 1.1.1.3. Guidance provided

The NIST Cybersecurity Framework (CSF) 2.0 provides guidance for organizations to manage cybersecurity risks effectively and integrate cybersecurity practices with broader enterprise risk management strategies. 

The NIST CSF 2.0 serves as a foundational tool to:

1. Standardize cybersecurity practices across organizations, sectors, and regions.
2. Integrate cybersecurity into business strategies and risk management frameworks.
3. Adapt to emerging challenges in technology, supply chains, and global threats.
4. Foster a culture of proactive risk management and continuous improvement.

<br><br>

<!-- TOC --><a name="112-detail-on-current-framework"></a>
#### 1.1.2. Detail on current framework

CSF consists of three core sections:

1. ***CSF Core:*** A hierarchy of cybersecurity outcomes categorized into six Functions: Govern, Identify, Protect, Detect, Respond, and Recover.
2. ***Profiles:*** Mechanisms to describe an organization's current and target cybersecurity postures.
3. ***Tiers:*** Four levels (Partial, Risk Informed, Repeatable, Adaptive) for evaluating the rigor of cybersecurity governance and risk management.
   
<br><br>

<!-- TOC --><a name="1121-csf-functions-and-key-concepts-applicable-to-scoping-ai-systems-"></a>
##### 1.1.2.1. CSF functions and key concepts applicable to scoping AI systems #####

<br><br>

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

<br><br>

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

<br><br>

***3. Protect (PR): Defining Safeguards Within Scope***

| Function | Details |
| --- | --- |
| **PR.AA (Identity Management and Access Control)** | 1. Enforce access controls to safeguard AI models, training data, and outputs. |
| | 2. Ensure identity management practices for users accessing AI systems are robust. |
| **PR.DS (Data Security)** | 1. Protect AI data at rest, in transit, and in use from unauthorized access and tampering. |
| | 2. Secure sensitive datasets used for training and inference processes. |
| **PR.PS (Platform Security)** | 1. Implement secure configurations for AI infrastructure, including cloud environments and hardware accelerators. |
| | 2. Prevent unauthorized software installation or execution within AI pipelines. |

<br><br>

***4. Detect (DE): Monitoring for Threats***


| Function | Details |
| --- | --- |
| **DE.CM (Continuous Monitoring)** | 1. Monitor AI system performance for anomalies, such as adversarial inputs or unexpected outputs. |
| | 2. Track network activity and system logs for indicators of compromise in AI components. |
| **DE.AE (Adverse Event Analysis)** | 1. Analyze anomalies in AI behavior to determine root causes, such as training data corruption or adversarial manipulation. |
| | 2. Correlate information from multiple sources, including threat intelligence, to understand incidents affecting AI systems. |

<br><br>

***5. Respond (RS): Taking Action Within Scope***


| Function | Details |
| --- | --- |
| **RS.MA (Incident Management)** | 1. Execute incident response plans for AI-related events, such as data breaches or system exploitation. |
| | 2. Coordinate responses with external stakeholders, including cloud providers and AI model vendors. |
| **RS.CO (Incident Communication)** | 1. Communicate incident details to internal teams, partners, and customers to mitigate downstream impacts. |
| | 2. Share lessons learned with stakeholders to improve future scoping efforts. |

<br><br>

***6. Recover (RC): Post-Incident Adjustments***


| Function | Details |
| --- | --- |
| **RC.RP (Incident Recovery Plan Execution)** | 1. Restore AI systems to operational status while ensuring the integrity of restored components, such as data and models. |
| | 2. Validate backups before using them for recovery to avoid reintroducing vulnerabilities. |
| **RC.CO (Incident Recovery Communication)** | 1. Inform stakeholders about recovery progress and measures taken to prevent recurrence. |
| | 2. Update scoping documents and risk assessments based on lessons learned. |

<br><br>

<!-- TOC --><a name="113-what-is-missing-for-defenders-of-ai-systems"></a>
#### 1.1.3. What is missing for defenders of AI systems

The NIST CSF 2.0 provides a strong general framework but could be enhanced for AI system defenders by:

1. Incorporating AI-specific risks, such as adversarial attacks, model drift, and poisoning.
2. Addressing supply chain vulnerabilities unique to AI.
3. Providing detailed guidance for AI-focused incident response, recovery, and monitoring.
4. Integrating AI ethics, explainability, and transparency into governance practices.
5. Explicitly aligning with NIST AI RMF for a holistic approach to AI risk management.

<br><br>

<!-- TOC --><a name="12-nist-rmf"></a>
### 1.2. NIST RMF

<!-- TOC --><a name="121-overview"></a>
#### 1.2.1. Overview
 
The NIST Risk Management Framework (RMF) is a structured framework, that integrates security and privacy into the lifecycle of information systems (including AI systems). It is widely used in federal agencies and private organizations to ensure a consistent, scalable, and effective method for protecting sensitive information.

The RMF is mandatory for federal agencies under laws like FISMA (Federal Information Security Modernization Act) and is recommended for private organizations seeking robust risk management practices. It aligns closely with the NIST Cybersecurity Framework (CSF) for broader risk management.

<br><br>

<!-- TOC --><a name="1211-scoping-of-ai-system-andor-cybersecurity-purview"></a>
##### 1.2.1.1. Scoping of AI system and/or cybersecurity purview

In the NIST RMF, scoping is critical to the Prepare, Categorize, and Select steps. It ensures that the boundaries of the system, its operational context, and applicable controls are well-defined to align with organizational objectives, compliance requirements, and risk management strategies.

| **RMF Step**       | **Scoping Objective**                                                                                           |
|---------------------|----------------------------------------------------------------------------------------------------------------|
| **Prepare**         | Define the scope of the system, including boundaries, stakeholders, critical assets, and risk management strategies. |
| **Categorize**      | Identify the scope of information and systems to be categorized based on their confidentiality, integrity, and availability impact. |
| **Select**          | Determine the scope of security and privacy controls required to address identified risks and tailor them to system needs. |
| **Implement**       | Apply controls to all scoped system components and document how they address the defined security and privacy boundaries. |
| **Assess**          | Validate that scoped controls operate effectively within the defined boundaries and meet security/privacy objectives. |
| **Authorize**       | Ensure the scoped system and its components are evaluated for residual risks within the defined authorization boundary. |
| **Monitor**         | Continuously monitor scoped assets and controls to detect changes, emerging threats, and ensure compliance with security objectives. |

<br><br>

<!-- TOC --><a name="1212-persona-addressed"></a>
##### 1.2.1.2. Persona addressed

| **RMF Activity**                     | **Senior Accountable Official for Risk Management** | **Chief Information Officer (CIO)** | **Authorizing Official (AO)** | **Senior Agency Official for Privacy (SAOP)** | **Senior Agency Information Security Officer (SAISO)** | **System Owner** | **Control Assessor** | **System Security Officer (SSO)** | **System Privacy Officer** | **Data Scientist/AI Engineer** | **Software Development Team** | **SRE** | **Software Architecture Team** | **Common Control Provider** | **Mission/Business Owner** |  
|--------------------------------------|----------------------------------------------------|-------------------------------------|-------------------------------|-----------------------------------------------|--------------------------------------------------------|------------------|-----------------------|-----------------------------------|---------------------------|----------------------------------|----------------------------------|-------|------------------------------|-----------------------------|-----------------------------|  
| **Prepare**                          | A                                                | R                                   | C                             | C                                             | C                                                      | I                | I                     | I                                 | I                         | C                                | I                                | I     | C                            | C                           | A                           |  
| Identify Risk Management Roles       | A                                                | R                                   | C                             | C                                             | R                                                      | I                | I                     | I                                 | I                         | I                                | I                                | I     | I                            | I                           | A                           |  
| Define Risk Management Strategy      | A                                                | C                                   | R                             | C                                             | C                                                      | I                | I                     | I                                 | I                         | I                                | C                                | I     | R                            | I                           | A                           |  
| Perform Risk Assessment              | R                                                | C                                   | A                             | C                                             | R                                                      | C                | R                     | I                                 | I                         | C                                | R                                | C     | C                            | I                           | C                           |  
| **Categorize AI Systems**            | R                                                | C                                   | A                             | C                                             | R                                                      | R                | I                     | C                                 | C                         | R                                | R                                | C     | R                            | I                           | A                           |  
| Identify Privacy/Security Impacts    | C                                                | C                                   | A                             | R                                             | C                                                      | R                | I                     | R                                 | C                         | R                                | R                                | I     | C                            | C                           | A                           |  
| **Select Controls**                  | A                                                | C                                   | R                             | C                                             | R                                                      | R                | C                     | C                                 | C                         | C                                | C                                | I     | R                            | I                           | A                           |  
| Tailor Controls to AI Systems        | A                                                | C                                   | R                             | C                                             | R                                                      | R                | C                     | R                                 | R                         | C                                | R                                | I     | R                            | I                           | A                           |  
| **Implement Controls**               | C                                                | C                                   | A                             | C                                             | C                                                      | R                | I                     | R                                 | R                         | R                                | R                                | R     | R                            | C                           | I                           |  
| Deploy Privacy & Security Features   | C                                                | C                                   | A                             | R                                             | R                                                      | R                | I                     | R                                 | R                         | R                                | R                                | R     | R                            | I                           | I                           |  
| **Assess Controls**                  | C                                                | C                                   | A                             | C                                             | C                                                      | I                | R                     | R                                 | R                         | C                                | I                                | I     | C                            | C                           | I                           |  
| Validate AI Security and Privacy     | C                                                | C                                   | A                             | C                                             | C                                                      | I                | R                     | R                                 | R                         | R                                | I                                | I     | C                            | I                           | I                           |  
| **Authorize AI System**              | C                                                | C                                   | A                             | C                                             | C                                                      | C                | C                     | C                                 | C                         | C                                | C                                | C     | C                            | I                           | A                           |  
| Risk Decision and Authorization      | C                                                | C                                   | A                             | C                                             | C                                                      | C                | C                     | C                                 | C                         | C                                | I                                | C     | C                            | I                           | A                           |  
| **Monitor AI Systems**               | C                                                | C                                   | A                             | C                                             | R                                                      | R                | I                     | R                                 | R                         | C                                | R                                | R     | R                            | I                           | A                           |  
| Continuous Monitoring Strategy       | A                                                | C                                   | R                             | C                                             | R                                                      | C                | C                     | R                                 | R                         | C                                | C                                | R     | R                            | C                           | C                           |  

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)

<br><br>

<!-- TOC --><a name="1213-guidance-provided"></a>
##### 1.2.1.3. Guidance provided

The NIST RMF provides general risk management principles that can be tailored to address the unique risks associated with AI systems. 

<br><br>

<!-- TOC --><a name="122-detail-on-current-framework"></a>
#### 1.2.2. Detail on current framework

Applying the NIST Risk Management Framework (RMF) to AI systems involves tailoring the framework's steps to address the unique challenges and risks associated with AI technologies. AI systems introduce complexities such as data bias, model integrity, adversarial vulnerabilities, and explainability requirements, which must be integrated into the RMF process.

<br><br>

| **RMF Step**       | **Objective**                                                                                   | **AI-Specific Tasks**                                                                                                  | **Output**                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Prepare**         | Establish readiness to manage AI-specific risks.                                              | Define AI system boundaries, identify stakeholders, develop AI-specific risk management strategy.                      | AI-specific risk strategy and system inventory.                                           |
| **Categorize**      | Determine the AI system’s security impact level.                                              | Evaluate sensitivity of data, assess impact of model failures, identify AI-specific vulnerabilities (e.g., adversarial). | Categorization documentation that includes AI-specific risks.                            |
| **Select**          | Choose controls to mitigate AI risks.                                                         | Tailor controls for privacy, bias, adversarial robustness, and explainability. Integrate supply chain risk management.  | Control baselines tailored for the AI system.                                             |
| **Implement**       | Deploy controls within the AI system’s lifecycle.                                             | Apply data governance policies, implement runtime protections, document model and data lineage.                        | Evidence of implemented controls (e.g., secure pipelines, data protection measures).      |
| **Assess**          | Validate that controls mitigate AI-specific risks effectively.                                | Test for model robustness, bias detection, performance validation, and incident response readiness.                    | Security Assessment Report (SAR) with AI-specific findings.                              |
| **Authorize**       | Approve the AI system for operation after evaluating residual risks.                          | Review ethical and regulatory compliance, evaluate residual risks with input from data scientists and legal advisors.   | Authorization decision (ATO or denial).                                                  |
| **Monitor**         | Continuously track AI system risks and update controls as needed.                             | Monitor for model drift, detect adversarial attacks, maintain data usage logs, automate monitoring processes.           | Updated risk assessments and monitoring reports.                                          |

<br><br>

<!-- TOC --><a name="123-what-is-missing-for-defenders-of-ai-systems"></a>
#### 1.2.3. What is missing for defenders of AI systems

While the RMF is adaptable, it lacks AI-specific extensions that address unique risks, such as adversarial threats, explainability, bias, and dynamic system behaviors. 

Defenders need:
1. Tailored threat models for AI.
2. Explicit controls for adversarial robustness, fairness, and privacy.
3. Enhanced guidance for real-time monitoring, secure AI development, and incident response.
4. Focus on training and interdisciplinary collaboration for AI and cybersecurity teams.

<br><br>

<!-- TOC --><a name="2-ai-risk-management-framework"></a>
## 2. AI Risk Management Framework

<!-- TOC --><a name="21-nist-ai-rmf-10"></a>
### 2.1. NIST AI RMF 1.0

<!-- TOC --><a name="211-overview"></a>
#### 2.1.1. Overview

The NIST AI RMF 1.0, published in January 2023, is a voluntary framework designed to help organizations manage risks associated with artificial intelligence (AI) systems. It aims to promote the responsible design, development, deployment, and use of AI technologies while mitigating potential harms. 

The NIST AI RMF serves as a comprehensive tool for organizations to navigate the complexities of managing AI risks, ensuring their systems are secure, reliable, and aligned with ethical and societal standards.

<br><br>

<!-- TOC --><a name="2111-scoping-of-ai-system-andor-cybersecurity-purview"></a>
##### 2.1.1.1. Scoping of AI system and/or cybersecurity purview

In the AI RMF, cybersecurity plays a key role in ensuring the confidentiality, integrity, and availability of AI systems. Scoping for cybersecurity purview involves identifying specific areas of focus to protect the AI system and its data.

<br><br>

| **Category**            | **Description**                                                                                                   | **Examples**                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **Threat Landscape**     | Identifying cybersecurity threats specific to AI systems.                                                       | Adversarial attacks, data poisoning, model theft, system exploitation, inference attacks.        |
| **Security Requirements**| Establishing security objectives to protect AI systems and their data.                                           | Secure data storage, protect model infrastructure, safeguard APIs, control third-party access.    |
| **System Boundaries**    | Defining components and scope for cybersecurity measures.                                                        | Data storage, model infrastructure, APIs, third-party tools.                                     |
| **Cybersecurity Controls**| Applying technical and organizational measures to secure the AI system.                                          | Access control, encryption, monitoring, resilience planning.                                     |
| **Regulatory Compliance**| Ensuring adherence to legal and regulatory standards related to cybersecurity.                                   | FISMA, GDPR, CCPA, HIPAA, NIST SP 800-53, SP 800-171.                                            |
| **Incident Response**    | Planning for and responding to cybersecurity incidents affecting AI systems.                                     | Addressing model poisoning, adversarial attacks, recovery from data corruption.                  |
| **Governance and Oversight**| Integrating cybersecurity considerations into organizational governance and risk management practices.           | Assigning roles, monitoring risks, ensuring accountability.                                      |

<br><br>

<!-- TOC --><a name="2112-persona-addressed"></a>
##### 2.1.1.2. Persona addressed


| **Function / Task**                  | **AI System Owner** | **Risk Managers** | **Cybersecurity Team** | **Software Development Team** | **SRE (Site Reliability Engineering)** | **Software Architecture Team** | **Executive Leadership** | **Legal & Compliance Teams** | **External Vendors** | **Data Scientist / AI Engineer** | **End Users** | **Policy Makers / Regulators** |
|---------------------------------------|---------------------|-------------------|-------------------------|--------------------------------|----------------------------------------|--------------------------------|-------------------------|-----------------------------|-----------------------|--------------------------------|--------------|----------------------------|
| **1. Govern** |  |  |  |  |  |   |   |   |   |   |   |   |
| Establish governance framework        | A                   | R                 | C                       |                                |                                        | C                              | A                       | C                           | C                     |                                |              |                            |
| Set risk tolerance levels             | A                   | R                 | C                       |                                |                                        |                                | A                       | C                           |                       |                                |              |                            |
| Define policies and processes         | C                   | R                 | C                       |                                |                                        | C                              | A                       | C                           | C                     |                                |              |                            |
| Assign roles and accountability       | A                   | R                 | C                       |                                |                                        |                                | A                       | C                           |                       |                                |              |                            |
| Integrate AI risk governance into ERM | A                   | R                 | C                       |                                |                                        | C                              | A                       | C                           |                       |                                |              |                            |
| **2. Map**                           |                     |                   |                         |                                |                                        |                                |                         |                             |                       |                                |              |                            |
| Identify AI-specific risks            | R                   | R                 | C                       |                                | C                                      | C                              | C                       | C                           | C                     | A                              |              |                            |
| Identify societal impacts of AI       | C                   | R                 |                         |                                |                                        | C                              | C                       | C                           |                       | C                              | I            | A                          |
| Map risks to lifecycle stages         | R                   | A                 | C                       | C                              |                                        | C                              |                         |                             |                       |                                |              |                            |
| Contextualize risks to applications   | C                   | R                 | C                       | R                              | C                                      | C                              |                         | C                           | C                     | C                              |              |                            |
| **3. Measure**                       |                     |                   |                         |                                |                                        |                                |                         |                             |                       |                                |              |                            |
| Assess system performance risks       | R                   | C                 | C                       | R                              | R                                      | A                              |                         |                             |                       | R                              |              |                            |
| Validate trustworthiness criteria     | C                   | C                 | R                       |                                |                                        | R                              |                         |                             |                       | C                              |              |                            |
| Monitor emergent risks                | R                   | A                 | R                       | C                              | R                                      | C                              |                         |                             |                       |                                |              |                            |
| Conduct TEVV (Testing/Evaluation)     | R                   | C                 | C                       | R                              | R                                      | A                              |                         |                             | C                     |                                |              |                            |
| Document risk measurement processes   | C                   | R                 | C                       |                                |                                        | R                              |                         |                             |                       |                                |              |                            |
| **4. Manage**                        |                     |                   |                         |                                |                                        |                                |                         |                             |                       |                                |              |                            |
| Develop mitigation strategies         | R                   | R                 | C                       | C                              | R                                      | R                              | C                       | C                           |                       |                                |              |                            |
| Prioritize risks for action           | C                   | R                 | C                       |                                | C                                      |                                | A                       |                             |                       |                                |              |                            |
| Implement mitigation controls         | C                   | C                 | R                       | R                              | R                                      | R                              |                         |                             | C                     |                                |              |                            |
| Monitor effectiveness of actions      | R                   | R                 | C                       |                                | R                                      | C                              |                         |                             |                       |                                |              |                            |
| Communicate residual risks            | R                   | A                 | C                       |                                |                                        |                                | A                       | C                           | C                     |                                |              |                            |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)


<br><br>

<!-- TOC --><a name="2112-guidance-provided"></a>
##### 2.1.1.2. Guidance provided

The NIST AI RMF 1.0 provides actionable guidance to manage AI risks effectively, ensuring systems are trustworthy, safe, and aligned with organizational goals and societal values. It emphasizes flexibility, continuous improvement, and stakeholder collaboration to address the complexities of deploying AI responsibly.

<br><br>

<!-- TOC --><a name="212-detail-on-current-framework"></a>
#### 2.1.2. Detail on current framework

AI RMF framework structure consists of two main sections: Framing Risk and Core Functions.

<br><br>

***Framing Risk***


| **Aspect**              | **Description**                                                                                                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Risk Identification** | AI risks are identified across technical and socio-technical dimensions, considering both anticipated and emergent risks throughout the AI lifecycle.                                |
| **Dynamic Risks**        | AI risks evolve over time due to changing data, deployment contexts, and interactions with other systems or users, requiring continuous assessment and adaptation.                   |
| **Trustworthiness Characteristics** | Trustworthy AI must demonstrate attributes such as being valid and reliable, safe, privacy-enhanced, secure, accountable, transparent, explainable, and fair.                        |
| **Key Challenges**       | Challenges include managing emergent risks, addressing biases, ensuring transparency and explainability, and balancing trade-offs between trustworthiness attributes (e.g., fairness vs. accuracy). |
| **Stakeholders**         | Includes developers, operators, end users, impacted communities, and regulators who contribute to or are affected by AI systems.                                                   |
| **Ethical and Societal Risks** | Risks include harm to civil liberties, discrimination, inequities, and environmental impacts, requiring socio-technical alignment to mitigate potential negative outcomes.                          |

<br><br>

***Core Functions***

| **Function**   | **Purpose**                                                                                                   | **Key Activities**                                                                                                                                          |
|-----------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Govern**     | Establishes governance structures and processes for AI risk management.                                      | 1. Define roles and accountability. |
|  |  | 2. Align AI development with organizational values. |
|  |  | 3. Integrate AI risks into enterprise risk management (ERM). |
| **Map**        | Identifies and contextualizes AI risks throughout the AI lifecycle.                                          | 1. Identify risks across design, build, deployment, and operation stages. |
|  |  | 2. Assess societal, ethical, and operational impacts of AI systems. |
| **Measure**    | Evaluates risks and trustworthiness using quantitative and qualitative metrics.                              | 1. Conduct TEVV (Testing, Evaluation, Verification, Validation). |
|  |  | 2. Assess trustworthiness attributes like bias, fairness, and robustness. |
| **Manage**     | Prioritizes and mitigates risks to minimize harm and enhance AI system reliability.                          | 1. Implement mitigation strategies. |
|  |  | 2. Monitor systems for emergent risks. |
|  |  | 3. Communicate residual risks to stakeholders. |

<br><br>

<!-- TOC --><a name="213-what-is-missing-for-defenders-of-ai-systems"></a>
#### 2.1.3. What is missing for defenders of AI systems

While the NIST AI Risk Management Framework (AI RMF 1.0) provides comprehensive guidance for managing AI risks, there are areas where it could be enhanced to better address cybersecurity concerns, such as adversarial threats, malicious use, and other vulnerabilities. 

<br><br>

<!-- TOC --><a name="22-nist-ai-rmf-10-for-generative-ai-gai"></a>
### 2.2. NIST AI RMF 1.0 for Generative AI (GAI)

<!-- TOC --><a name="221-overview"></a>
#### 2.2.1. Overview

NIST AI RMF 1.0 for Generative AI (GAI) provides guidance on managing risks associated with generative AI (GAI) systems. The framework offers a structured approach to managing GAI risks through proactive governance, lifecycle management, and continuous improvement based on empirical evidence and stakeholder feedback​. It is a companion resource to the NIST AI Risk Management Framework (AI RMF 1.0), addressing risks unique to generative AI.

<br><br>

<!-- TOC --><a name="2211-scoping-of-ai-system-andor-cybersecurity-purview"></a>
##### 2.2.1.1. Scoping of AI system and/or cybersecurity purview

As an extension of the NIST AI RMF 1.0 this framework inherits most of the characteristics of its parent. However there are some key scoping deferences specific to Generative AI.


| **Aspect**                 | **NIST AI RMF**    | **NIST AI RMF GAI**      |
|----------------------------|--------------------|-----------------------------------|
| **Purpose**                | A broad framework for managing risks across all types of AI systems, regardless of specific applications.             | Focused specifically on risks unique to or exacerbated by Generative AI (GAI) systems.   |
| **Scoping Applicability**  | Covers AI systems across sectors and use cases without being specific to any particular AI technology.  | Tailored to cross-sectoral risks and specific GAI use cases, such as those involving LLMs, multimodal models, or fine-tuned systems. |
| **Focus on AI Lifecycle**  | Covers all lifecycle stages but emphasizes high-level principles for governance, design, deployment, and monitoring. | Addresses risks specific to GAI at each stage of the lifecycle, including risks during training (e.g., data quality), deployment, and operation. |
| **Dual-Use Considerations**| General acknowledgment of dual-use risks (e.g., misuse of AI tools). | Detailed focus on GAI misuse risks, such as generating harmful content (e.g., deepfakes, CBRN design, disinformation). |
| **Cybersecurity Scope**    | Cybersecurity considered as a subset of AI risks, with focus on general vulnerabilities. | Addresses specific cybersecurity risks in GAI, such as prompt injection, data poisoning, adversarial misuse, and reverse engineering. |
| **Transparency and Provenance** | Recommends transparency and documentation of AI system components and decision-making processes.  | Focuses extensively on content provenance, emphasizing tracing training data, generated outputs, and model lineage to ensure transparency. |
| **Third-Party Integration**| Broad recommendation to assess and manage risks from third-party data or models.  | Emphasizes the scale of third-party reliance in GAI systems (e.g., datasets, pre-trained models) and risks from non-transparent integration. |
| **Data Privacy**           | General principles for protecting user data and complying with privacy regulations.  | Focuses on data memorization and inference risks in GAI, which could expose sensitive personal data from training datasets. |
| **Environmental Impacts**  | Brief mention of energy efficiency and resource usage in AI systems.  | Explicit concern about resource-intensive training and inference in GAI systems and their carbon footprints.       |
| **Bias and Homogenization**| Broad treatment of bias in AI systems and mitigation through diverse datasets and inclusive design.  | Highlights specific GAI issues, such as amplifying societal biases, representational harms, and risks of algorithmic monoculture. |
| **Incident Response**      | General recommendations for incident monitoring and response.   | Detailed guidance for incident response plans specific to third-party components, adversarial attacks, and provenance failures in GAI. |
| **Governance**             | High-level governance principles applicable to various organizational contexts. | Emphasizes governance tailored to GAI risks, including independent evaluations, human-AI configuration, and critical thinking policies. |

<br><br>

<!-- TOC --><a name="2212-persona-addressed"></a>
##### 2.2.1.2. Persona addressed


| **Function / Task)** | **AI System Owner** | **Risk Managers** | **Cybersecurity Team** | **Software Development Team** | **SRE** | **Software Architecture Team** | **Executive Leadership** | **Legal & Compliance Teams** | **External Vendors** | **Data Scientist / AI Engineer** | **End Users** | **Policy Makers / Regulators** |
|-----------------------------|----------------------|--------------------|-------------------------|--------------------------------|---------|----------------------------------|--------------------------|-----------------------------|-----------------------|----------------------------------|--------------|-------------------------------|
| **1. Govern** |  |  |  |  |  |   |   |   |   |   |   |   |
| Data privacy compliance                       | A                    | C                  | R                       | I                              | I       | C                                | C                        | R                           | C                     | I                                | I            | R                             |
| Third-party vendor assessment                 | R                    | C                  | C                       | I                              | I       | C                                | I                        | R                           | A                     | I                                | I            | C                             |
| Compliance with regulations                   | C                    | C                  | C                       | I                              | I       | I                                | R                        | A                           | I                     | I                                | I            | R                             |
| Policy development and governance             | C                    | C                  | C                       | I                              | I       | C                                | A                        | A                           | I                     | I                                | I            | R                             |
| Transparency and explainability               | R                    | C                  | I                       | C                              | I       | C                                | I                        | C                           | I                     | A                                | C            | R                             |
| Legal compliance auditing                     | I                    | C                  | C                       | I                              | I       | I                                | I                        | R                           | I                     | I                                | I            | R                             |
| Ethical AI practices and policy alignment     | C                    | R                  | C                       | I                              | I       | I                                | A                        | R                           | C                     | C                                | I            | R                             |
| **2. Map** |  |  |  |  |  |   |   |   |   |   |   |   |
| Define AI system scope                        | R                    | A                  | C                       | C                              | C       | C                                | I                        | I                           | C                     | R                                | I            | I                             |
| Identify risks across lifecycle stages        | C                    | R                  | C                       | I                              | I       | C                                | A                        | C                           | I                     | C                                | I            | I                             |
| System architecture design                    | R                    | I                  | C                       | C                              | C       | A                                | I                        | I                           | I                     | C                                | I            | I                             |
| **3. Measure** |  |  |  |  |  |   |   |   |   |   |   |   |
| Model training and validation                 | R                    | C                  | C                       | C                              | I       | C                                | I                        | I                           | C                     | A                                | I            | I                             |
| Post-deployment monitoring                    | A                    | C                  | C                       | C                              | R       | C                                | I                        | C                           | I                     | C                                | I            | I                             |
| Addressing security vulnerabilities           | I                    | C                  | R                       | C                              | R       | I                                | I                        | I                           | I                     | I                                | I            | I                             |
| Provenance and accountability                 | A                    | C                  | C                       | C                              | C       | R                                | I                        | C                           | I                     | C                                | I            | R                             |
| Feedback and continuous improvement           | R                    | R                  | C                       | C                              | C       | C                                | I                        | I                           | I                     | C                                | R            | I                             |
| **4. Manage** |  |  |  |  |  |   |   |   |   |   |   |   |
| Develop risk mitigation strategies            | C                    | R                  | C                       | C                              | I       | R                                | A                        | C                           | I                     | R                                | I            | I                             |
| Incident response planning                    | C                    | R                  | A                       | C                              | R       | C                                | I                        | C                           | I                     | C                                | I            | I                             |
| System deployment                             | R                    | C                  | C                       | R                              | A       | C                                | I                        | I                           | I                     | R                                | I            | I                             |
| Stakeholder communication                     | R                    | C                  | C                       | I                              | I       | I                                | A                        | C                           | I                     | C                                | A            | C                             |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)

<br><br>

<!-- TOC --><a name="2213-guidance-provided"></a>
##### 2.2.1.3. Guidance provided

The NIST AI 600-1 (GUI) provides a structured framework for managing risks unique to generative AI (GAI) systems, emphasizing transparency, accountability, and adaptability. It identifies and addresses technical, misuse, and societal risks associated with GAI, such as confabulation, bias amplification, disinformation, and cybersecurity vulnerabilities. 

The guidance aligns with NIST AI RMF 1.0 functions—Govern, Map, Measure, and Manage—and emphasizes trustworthy AI attributes, including fairness, safety, and privacy. Organizations are encouraged to implement robust governance, transparency in content provenance, independent evaluations, and effective risk mitigation strategies throughout the AI lifecycle. 

This evolving framework ensures organizations can navigate the complex and rapidly advancing generative AI landscape while adhering to ethical and regulatory standards.

<br><br>

<!-- TOC --><a name="222-detail-on-current-framework"></a>
#### 2.2.2. Detail on current framework

The NIST AI 600-1 Framework is a specialized companion resource to the NIST AI RMF 1.0, tailored to address risks specific to Generative Artificial Intelligence (GAI). This document provides actionable guidance for organizations to manage the unique challenges posed by generative AI systems, such as large language models (LLMs) and multimodal generative tools.

<br><br>

***Key Risks Associated with GAI***


| **Risk Category**    | **Description**  |
|----------------------|------------------|
| **Technical Risks**   | **1. Confabulation**: GAI systems generating inaccurate or false content, leading to user deception. |
|                       | **2. Data Privacy**: Potential for GAI to leak sensitive personal data through memorization or inferencing. |
|                       | **3. Bias and Homogenization**: Amplification of systemic biases and reduced diversity in outputs, leading to societal harms. |                           |
|                       | **4. Environmental Impact**: High computational resource usage for training and inference, contributing to significant carbon footprints.                |
| **Misuse Risks**      | **1. Malicious Content**: Use of GAI to create harmful content such as disinformation, deepfakes, or illegal materials. |
|                       | **2. Cybersecurity Exploitation**: Automation of cyberattacks, such as phishing, malware creation, and vulnerabilities to prompt injection or data poisoning. |
| **Societal Risks**    | **1. Erosion of Public Trust**: Disinformation campaigns undermining confidence in institutions and facts. |
|                       | **2. Representational Harms**: Reinforcing harmful stereotypes in GAI outputs, particularly in text-to-image models. |
|                       | **3. Economic Disruption**: Long-term impacts on labor markets, intellectual property, and creative industries. |

<br><br>

***NIST AI RMF Functions Applied to GAI***


| **Function** | **Key Actions**  |
|--------------|------------------|
| **Govern**   | 1. Align GAI development with legal and regulatory requirements (e.g., data privacy, intellectual property).                                               |
|              | 2. Foster accountability by establishing organizational risk tolerances and governance structures.                                                         |
|              | 3. Develop policies for transparency, including documenting training data provenance and model decisions.                                                   |
|              | 4. Ensure robust oversight through independent evaluations proportional to system risks.                                                                   |
| **Map**      | 1. Identify and document risks throughout the AI lifecycle, including technical, operational, and societal dimensions.                                      |
|              | 2. Analyze dependencies on third-party components, such as datasets, libraries, and pre-trained models.                                                    |
|              | 3. Define roles and responsibilities for stakeholder engagement across teams and external parties.                                                         |
| **Measure**  | 1. Conduct pre-deployment testing for robustness, fairness, and safety, including red-teaming and validation.                                              |
|              | 2. Monitor and evaluate system performance for biases, confabulation, and environmental impacts.                                                               |
|              | 3. Implement tools for assessing content provenance, such as watermarking or cryptographic methods, to trace AI-generated outputs.                         |
| **Manage**   | 1. Develop incident response plans to address adversarial attacks (e.g., data poisoning, prompt injection).                                                |
|              | 2. Establish protocols for safe decommissioning of systems, addressing dependencies and user interactions.                                                 |
|              | 3. Engage stakeholders, including end users and policymakers, to address ethical and societal impacts associated with GAI.                                 |

<br><br>

<!-- TOC --><a name="223-what-is-missing-for-defenders-of-ai-systems"></a>
#### 2.2.3. What is missing for defenders of AI systems

While the NIST AI 600-1 Framework provides a comprehensive approach for managing risks associated with generative AI, several aspects critical for defenders of AI systems (e.g., cybersecurity teams, incident responders, and risk managers) are either missing or could benefit from additional detail.

<br><br>

<!-- TOC --><a name="23-nist-ai-adversarial-machine-learning-aml"></a>
### 2.3. NIST AI Adversarial Machine Learning (AML)

<!-- TOC --><a name="231-overview"></a>
#### 2.3.1. Overview

The NIST AI 100-2e2023 - Adversarial Machine Learning framework provides a comprehensive taxonomy and terminology for understanding adversarial machine learning (AML), addressing the security, resilience, and trustworthiness of AI systems. It categorizes attacks based on learning stages, attacker objectives, capabilities, and knowledge levels, covering evasion, poisoning, privacy, and abuse threats across predictive and generative AI systems. 

The framework highlights the unique challenges posed by adversarial attacks, such as evasion via adversarial inputs, poisoning training data or models, and extracting sensitive information from large language models or generative systems. 

It proposes mitigation strategies, including adversarial training, differential privacy, and formal verification, while acknowledging inherent trade-offs between robustness, accuracy, and fairness. Emphasizing the dynamic and evolving nature of adversarial threats, the framework advocates for scalable, context-aware defenses and highlights unresolved issues like supply chain risks, multimodal vulnerabilities, and adaptive attack mitigation. 

<br><br>

<!-- TOC --><a name="2311-scoping-of-ai-system-andor-cybersecurity-purview"></a>
##### 2.2.1.1. Scoping of AI system and/or cybersecurity purview

The NIST AI 100-2e2023 Framework scoping provides a detailed purview of AI systems, adversarial threats, and cybersecurity practices. It establishes clear boundaries around AI lifecycle stages, data modalities, and attack vectors, integrating AML into the broader cybersecurity landscape. 

| **Aspect** | **Scope Description**  |
|------------|------------------------|
| **AI System Categories**       | Covers Predictive AI (PredAI) and Generative AI (GenAI), addressing adversarial risks across all lifecycle stages (design, training, deployment, post-deployment). |
| **Lifecycle Stages**           | 1. Design/Development: Threat modeling and robust architecture. |
|  | 2. Training: Data validation, adversarial training. |
|  | 3. Deployment: Monitoring and real-time defenses. |
|  | 4. Post-Deployment: Updates and anomaly detection. |
| **Data Modalities**            | Includes images, text, audio, video, cybersecurity logs, and multimodal systems requiring specialized defenses and monitoring.                                     |
| **Threat Taxonomy**            | 1. Training-Stage Risks: Poisoning and backdoors. |
|  | 2. Deployment-Stage Risks: Evasion, prompt injection, model extraction. |
|  | 3. Privacy Risks: Membership inference, data leakage. |
| **Supply Chain Security**      | Ensures the integrity of third-party datasets, pre-trained models, and APIs.                                                                                     |
| **Mitigation Strategies**      | 1. Adversarial training and formal verification. |
|  | 2. Real-time anomaly detection. |
|  | 3. Data validation and provenance checks. |
|  | 4. Privacy-preserving methods. |
| **Interdisciplinary Roles**    | Collaboration across AI developers, cybersecurity teams, legal teams, and executive leadership.                                                                 |
| **Threat Intelligence Sharing**| Mechanisms for cross-organization sharing of adversarial incidents and mitigations.                                                                              |
| **Scalability of Defenses**    | Focuses on lightweight, resource-efficient defenses for real-time applications and scalable monitoring.                                                           |
| **Generative AI-Specific Risks**| - Mitigates prompt injection, harmful content, and data leakage. <br> - Monitors model outputs for adversarial manipulation.                                      |
| **Ethical and Legal Considerations** | - Balances robustness with fairness and transparency. <br> - Ensures regulatory compliance in AI operations.                                                  |

<br><br>

<!-- TOC --><a name="2312-persona-addressed"></a>
##### 2.3.1.2. Persona addressed

| **Task/Activity**                                  | **AI System Owner** | **Risk Managers** | **Cybersecurity Team** | **Software Development Team** | **SRE** | **Software Architecture Team** | **Executive Leadership** | **Legal & Compliance Teams** | **External Vendors** | **Data Scientist / AI Engineer** | **End Users** | **Policy Makers / Regulators** |
|----------------------------------------------------|----------------------|-------------------|-------------------------|-------------------------------|----------|-------------------------------|---------------------------|-------------------------------|------------------------|---------------------------------|-------------|----------------------------|
| Define AML strategy and roadmap                   | R                    | A                 | C                       | C                             | C        | C                             | A                       | C                             | C                      | C                               | I           | C                          |
| Identify and assess adversarial risks             | A                    | R                 | C                       | I                             | I        | C                             | I                       | I                             | I                      | R                               | I           | I                          |
| Develop robust AI models and defenses             | I                    | C                 | C                       | R                             | I        | C                             | I                       | I                             | I                      | A                               | I           | I                          |
| Implement adversarial training                    | I                    | C                 | C                       | A                             | I        | C                             | I                       | I                             | I                      | R                               | I           | I                          |
| Perform formal verification for robustness        | C                    | C                 | R                       | A                             | I        | C                             | I                       | I                             | I                      | R                               | I           | I                          |
| Secure AI supply chain (models and datasets)      | R                    | C                 | A                       | C                             | C        | R                             | I                       | C                             | R                      | I                               | I           | I                          |
| Monitor AI systems for adversarial activity       | C                    | C                 | A                       | I                             | R        | C                             | I                       | I                             | I                      | I                               | I           | I                          |
| Evaluate and validate external vendor compliance  | C                    | C                 | A                       | I                             | I        | I                             | I                       | R                             | A                      | I                               | I           | C                          |
| Define policies and governance frameworks         | I                    | C                 | C                       | I                             | I        | I                             | R                       | A                             | I                      | I                               | I           | A                          |
| Conduct training and awareness sessions           | R                    | R                 | C                       | I                             | I        | I                             | I                       | C                             | I                      | I                               | C           | I                          |
| Ensure regulatory compliance                      | A                    | C                 | C                       | I                             | I        | I                             | R                       | A                             | I                      | I                               | I           | R                          |
| Manage trade-offs: accuracy vs. robustness        | A                    | C                 | C                       | C                             | C        | R                             | R                       | I                             | I                      | C                               | I           | C                          |
| Report adversarial risks and defenses to leaders  | C                    | R                 | C                       | I                             | I        | I                             | A                       | C                             | I                      | I                               | I           | I                          |
| Communicate AML risks to end users                | I                    | C                 | C                       | I                             | I        | I                             | A                       | C                             | I                      | I                               | A           | I                          |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)


<br><br>

<!-- TOC --><a name="2313-guidance-provided"></a>
##### 2.3.1.3. Guidance provided

NIST AI 100-2e2023 Framework provides comprehensive guidance to enhance the security, robustness, and trustworthiness of AI systems. Its emphasis on lifecycle security, risk assessment, and interdisciplinary collaboration ensures that AI systems are prepared to face both current and emerging adversarial threats.

<br><br>

<!-- TOC --><a name="232-detail-on-current-framework"></a>
#### 2.3.2. Detail on current framework

The NIST AI 100-2e2023 Framework represents a foundational step in addressing the multifaceted challenges posed by adversarial machine learning (AML). By providing a comprehensive taxonomy and terminology, the framework enables a systematic understanding of the diverse threats to AI systems and outlines actionable strategies to mitigate these risks. It establishes a much-needed bridge between the fields of AI development, cybersecurity, and policy, laying the groundwork for designing, deploying, and governing secure and trustworthy AI systems.

<br><br>

***Purpose and Strategic Goals***

| **Purpose/Goal** | **Description** |
|------------------|-----------------|
| **Define AML Threats**       | Establish a standardized taxonomy and terminology for adversarial risks to unify understanding across domains. |
| **Enhance AI Security**      | Equip stakeholders with tools and strategies to mitigate adversarial risks and ensure resilience.              |
| **Support Risk Management**  | Align AML measures with the broader NIST AI Risk Management Framework for trustworthiness and risk-based decisions. |
| **Foster Trust in AI**       | Address vulnerabilities compromising the safety, fairness, and reliability of AI systems.                    |
| **Address Evolving Threats** | Provide a structured and adaptive approach to mitigate new and emerging adversarial risks.                      |

<br><br>

***Core Taxonomy and Dimensions***

| **Dimension** | **Description** | **Examples** |
|---------------|-----------------|--------------|
| **Stages of Learning**      | Categorizes attacks based on when they occur in the AI lifecycle. | 1. Training Stage: Data Poisoning, Model Poisoning.  |
|  |  | 2. Deployment Stage: Evasion Attacks, Privacy Attacks. |
| **Attacker Objectives**     | Identifies the goals adversaries aim to achieve. | 1. Availability Breakdown: Disrupt system functionality or usability. |
|  |  | 2. Integrity Violation: Cause incorrect or malicious outputs. |
|  |  | 3. Privacy Compromises:  Extract sensitive information from models or datasets.|
| **Attacker Capabilities**   | Specifies what attackers can manipulate or control. | 1. Training Data Control: Modifying or injecting training samples.|
|  |  | 2. Model Control: Altering model parameters or inserting backdoors. |
|  |  | 3. Testing Data Control: Manipulating inputs at inference time. |
|  |  | 4. Query Access: Exploiting API access to extract model outputs or confidence scores. |
|  |  | 5. Source Code Control: Tampering with the codebase or libraries. |
|  |  | 6. Label Limit: Restricting adversarial control over labels. |
| **Attacker Knowledge**      | Defines the level of knowledge attackers have about the AI system. | 1. White-Box Attacks (full knowledge). |
|  |  | 2. Black-Box Attacks (limited access). |
|  |  | 3. Gray-Box Attacks (partial knowledge). |
| **Data Modalities**         | Explains the types of data targeted by adversarial attacks. | 1. Images: Commonly targeted for evasion and poisoning attacks. |
|  |  | 2. Text: Manipulating NLP models using adversarial examples. |
|  |  | 3. Audio/Video: Tampering with speech recognition and video classification. |
|  |  | 4. Cybersecurity: Attacking malware classifiers and intrusion detection systems. |
|  |  | 5. Tabular Data: Exploiting systems in healthcare, finance, and business. |
|  |  | 6. Multimodal Systems: Coordinating attacks across integrated data types. |

<br><br>

***Attack Categories***

| **Category** | **Definition** |**Types** | **Examples** | **Mitigations** |
|-----------------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Evasion Attacks**   | Generate adversarial inputs to mislead models during inference.              | White-Box, Black-Box, Transferability.                                                          | Misclassifying road signs in autonomous vehicles; tricking diagnostic tools in healthcare.       | Adversarial Training, Randomized Smoothing, Formal Verification.                                          |
| **Poisoning Attacks** | Manipulate training data or models to degrade performance or embed triggers. | Availability Poisoning, Targeted Poisoning, Backdoor Poisoning, Model Poisoning.                | Corrupting datasets to bias models; embedding triggers in federated learning models.             | Data Validation, Secure Federated Learning Aggregation, Model Provenance Checks.                         |
| **Privacy Attacks**   | Extract sensitive information from datasets or models.                      | Membership Inference, Data Reconstruction, Model Extraction.                                    | Extracting personal data from AI models; determining if specific data was used in training.      | Differential Privacy, Cryptographic Techniques (e.g., Homomorphic Encryption).                           |
| **Generative AI Attacks** | Exploit vulnerabilities in generative models.                             | Prompt Injection, Data Extraction, Supply Chain Attacks.                                        | Manipulating large language models (LLMs) to reveal sensitive information or generate harmful outputs. | Transparent Model Documentation, Prompt Filtering, Secure Pre-trained Model Validation.                  |

<br><br>

***Mitigation Strategies***

| **Strategy**  | **Description** | **Advantages** | **Challenges/Limitations**  |
|---------------|----------------|-----------------|-------------------------|
| **Adversarial Training**   | Incorporates adversarial examples into the training process to improve robustness.                | Enhances resistance to known adversarial attacks.             | Increases computational cost and may reduce accuracy on clean data.                                 |
| **Randomized Smoothing**   | Adds random noise to inputs, creating smoother decision boundaries that are harder to exploit.    | Simple to implement and improves resilience to perturbations. | Limited effectiveness for certain attack types; may degrade performance on clean inputs.            |
| **Formal Verification**    | Uses mathematical methods to prove model robustness under specified conditions.                   | Guarantees robustness within defined parameters.              | Computationally expensive and challenging to scale for large models.                                |
| **Differential Privacy**   | Introduces noise to outputs or gradients, protecting individual data points in the training set.   | Strong protection against privacy attacks.                    | Reduces model utility and accuracy due to added noise.                                              |
| **Cryptographic Methods**  | Employs techniques like homomorphic encryption and secure multiparty computation for data privacy.| Provides robust privacy guarantees.                          | High computational overhead and complexity in implementation.                                       |
| **Data Validation**        | Filters and verifies the integrity of training datasets to detect and remove malicious inputs.    | Prevents poisoning attacks by ensuring data quality.          | Can be difficult to identify sophisticated poisoning attacks.                                       |
| **Secure Aggregation**     | Ensures robustness in federated learning by securely combining model updates from multiple clients.| Reduces risk of model poisoning in distributed settings.      | Computationally intensive and may require trusted infrastructure.                                   |
| **Model Provenance Checks**| Audits and verifies the origins of pre-trained models and datasets to ensure integrity.            | Mitigates risks from supply chain attacks.                    | May not detect subtle or embedded vulnerabilities in third-party models.                            |
| **Prompt Filtering**       | Applies filters to user inputs in generative AI to prevent harmful or manipulative prompt usage.  | Reduces risks of prompt injection attacks.                    | Requires constant updates to account for new and evolving attack methods.                           |

<br><br>

***Challenges and Open Problems***

| **Challenge/Open Problem** | **Description** | **Implications**  |
|---------|-------------------|---------------------|
| **Scalability of Defenses**       | Many mitigation techniques, such as adversarial training and formal verification, are computationally intensive and hard to scale. | Limits applicability in real-world scenarios involving large datasets and models.                   |
| **Adaptive Threats**              | Adversaries continuously evolve their techniques to bypass existing defenses.                        | Requires ongoing updates and innovation in mitigation strategies to stay effective.                 |
| **Theoretical Boundaries**        | Fundamental questions about the provable robustness of machine learning systems remain unanswered.   | Challenges the development of defenses that are both efficient and theoretically sound.              |
| **Multimodal Robustness**         | Ensuring resilience across models handling multiple data types (e.g., image-text) is complex.        | Multimodal systems are increasingly common, making this a critical area for future research.         |
| **Supply Chain Security**         | Third-party datasets and pre-trained models introduce vulnerabilities to the AI pipeline.            | Poses risks for organizations relying on external resources, requiring stringent validation measures. |
| **Trustworthiness Trade-Offs**    | Balancing robustness, fairness, privacy, and explainability remains challenging.                     | Trade-offs may result in systems that prioritize one attribute over others, impacting overall trust.  |
| **Data Validation Complexity**    | Sophisticated poisoning attacks can evade detection during data validation processes.                | Highlights the need for advanced tools to assess and sanitize datasets effectively.                  |
| **Privacy vs. Utility**           | Privacy-preserving techniques, such as differential privacy, often reduce model performance.         | Striking a balance is essential for systems in sensitive domains like healthcare and finance.         |
| **Evolving Generative AI Threats**| New vulnerabilities, such as prompt injection and data extraction from large language models, emerge rapidly. | Generative AI systems require specialized defenses that keep pace with the evolution of attack methods. |
| **Human Factors**                 | Human errors or biases in system design, data curation, or implementation can amplify adversarial vulnerabilities. | Emphasizes the need for training and awareness among AI practitioners and decision-makers.            |

<br><br>

***Generative AI and Emerging Concerns***

| **Concern** | **Description**  | **Implications** |
|-------------|----------------|--------------------|
| **Prompt Injection**             | Adversaries craft malicious inputs to manipulate the outputs of generative AI systems.             | Leads to harmful, biased, or incorrect outputs that undermine trust in the system.                        |
| **Data Extraction**              | Sensitive or proprietary training data can be inferred or reconstructed from generative models.    | Raises privacy and intellectual property concerns, especially for proprietary datasets.                   |
| **Supply Chain Attacks**         | Pre-trained generative models and training pipelines can be tampered with to embed vulnerabilities.| Introduces risks to organizations relying on third-party models and training data.                        |
| **Bias Amplification**           | Generative models may inherit or amplify biases present in training data.                         | Results in discriminatory or unfair outputs, impacting ethical AI adoption.                               |
| **Corporate Data Integration**   | Generative AI tools, such as LLMs, integrated with proprietary data may expose sensitive information.| Risks unintended leakage of corporate secrets or confidential data through AI outputs.                    |
| **Open vs. Closed Models**       | Open models enhance transparency but increase the surface area for attacks, while closed models limit external scrutiny. | Balancing transparency and security is essential to maintain both accountability and resilience.           |
| **Content Authenticity**         | Generative AI systems can create realistic but false content, such as deepfakes or fake news.      | Poses significant risks to public trust, security, and societal stability.                                |
| **Evolving Attack Methods**      | Adversarial techniques targeting generative AI evolve rapidly, making it challenging to maintain defenses. | Requires continuous innovation in security practices tailored to generative systems.                      |
| **Regulation and Governance**    | Lack of comprehensive policies governing generative AI systems exacerbates risks.                  | Calls for the development of ethical guidelines, auditing standards, and legal frameworks for deployment. |

<br><br>

<!-- TOC --><a name="233-what-is-missing-for-defenders-of-ai-systems"></a>
#### 2.3.3. What is missing for defenders of AI systems

From a defender's perspective, the NIST AI 100-2e2023 Framework provides a solid foundation for understanding adversarial risks but requires enhancements to address practical challenges. Key missing elements include detailed playbooks, incident response protocols, and tools for testing AI robustness. Defenders need more guidance on lightweight, scalable defenses, threat intelligence sharing, and securing the AI supply chain.

<br><br>

<!-- TOC --><a name="3-references"></a>
## 3. References

| Framework | Referenced Material |
| --- | --- |
| NIST CSF 2.0 | [NIST CSF 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) |
| NIST RMF | [NIST RMF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf) |
| NIST AI RMF 1.0 | [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) |
| NIST AI RMF 1.0 for Generative AI (GAI) | [NIST AI RMF 1.0 for Generative AI (GAI)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) |
| NIST AI Adversarial Machine Learning (AML) | [NIST AI Adversarial Machine Learning (AML)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2023.pdf)|

*Document was created with assistance of OpenAI ChatGPT 4o model.*