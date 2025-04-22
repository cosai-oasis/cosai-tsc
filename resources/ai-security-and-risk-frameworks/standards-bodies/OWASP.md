<!-- TOC start -->

- [OWASP](#owasp)
  - [1. Top 10 for LLM Applications 2025](#1-top-10-for-llm-applications-2025)
    - [1.1. Overview](#11-overview)
    - [1.2. Scoping of AI system and/or cybersecurity purview](#12-scoping-of-ai-system-andor-cybersecurity-purview)
    - [1.3. Persona addressed](#13-persona-addressed)
    - [1.4. Guidance provided](#14-guidance-provided)
    - [1.5. Detail on current framework](#15-detail-on-current-framework)
    - [1.6. What is missing for defenders of AI systems](#16-what-is-missing-for-defenders-of-ai-systems)
  - [2. References](#2-references)

<!-- TOC end -->


# OWASP


## 1. Top 10 for LLM Applications 2025


### 1.1. Overview

The OWASP Top 10 for LLM Applications (2025) highlights critical security risks associated with large language model (LLM) applications, emphasizing threats that can compromise confidentiality, integrity, and availability. As name of this paper emplies, it is focusing on top 10 risks:

1. ***Prompt injection*** remains a major concern, allowing attackers to manipulate LLM behavior and bypass safety controls. 
2. ***Sensitive information disclosure*** can lead to unintended exposure of personally identifiable information (PII) and proprietary data. 
3. ***Supply chain risks*** introduce vulnerabilities from third-party models, datasets, and dependencies, making rigorous vetting essential. 
4. ***Insecure output handling*** poses risks of code injection and cross-site scripting (XSS) if LLM-generated content is not properly sanitized. 
5. ***Excessive agency***, where LLMs have unchecked permissions, can lead to unauthorized actions and security breaches. 
6. ***Unbounded resource consumption*** (denial-of-service attacks) can overwhelm systems through excessive query loads, requiring rate limiting and anomaly detection. 
7. ***Data poisoning*** threatens model integrity by injecting manipulated training data, leading to biased or malicious outputs. 
8. ***System prompt leakage*** can expose internal logic, enabling attackers to reverse-engineer security mechanisms. 
9. ***Overly permissive integrations*** pose risks when LLMs are granted excessive API access, increasing the attack surface. 
10. ***Model theft and extraction attacks*** threaten intellectual property by leveraging repeated queries to reconstruct model behavior. 

To mitigate these risks, organizations must enforce strong input/output validation, least privilege principles, robust authentication, adversarial testing, continuous monitoring, and AI-specific security controls to safeguard LLM applications from evolving threats.

<br><br>

### 1.2. Scoping of AI system and/or cybersecurity purview

***AI System Scoping: Components and Boundaries***

| **AI System Scope**                 | **Description** |
|--------------------------------------|----------------|
| **Model Lifecycle Security**         | Covers pre-training, fine-tuning, deployment, and monitoring of LLMs. Protects against model poisoning, adversarial attacks, and unauthorized modifications. |
| **Data Ingestion & Processing**      | Ensures data integrity, provenance, and compliance with privacy laws (GDPR, CCPA). Implements data sanitization, differential privacy, and access controls. |
| **AI Supply Chain Risks**            | Manages third-party models, dataset security, and dependency vulnerabilities. Introduces Software Bill of Materials (SBOM) for AI and model provenance verification. |
| **Secure Model APIs & Interfaces**   | Covers authentication, authorization, and secure API interactions. Mitigates unauthorized API access, prompt injection, and excessive agency. |
| **End-User Interaction & Prompt Handling** | Implements content moderation, input validation, and prompt filtering to defend against prompt manipulation and malicious injections. |
| **System Prompt & Configuration Protection** | Prevents system prompt leakage, unauthorized configuration changes, and model inversion attacks. |
| **Adversarial & Security Testing**   | Deploys adversarial robustness training, anomaly detection, and penetration testing for AI security validation. |

<br>

***Cybersecurity Purview: AI-Specific Threats and Defenses***

| **Cybersecurity Domain**             | **AI-Specific Considerations** |
|--------------------------------------|--------------------------------|
| **Identity & Access Management (IAM)** | Enforces RBAC, OAuth-based access control, and zero-trust principles for AI APIs and LLM services. |
| **Threat Detection & Incident Response** | Deploys AI-driven anomaly detection, logging, and adversarial attack monitoring. |
| **Data Security & Governance**        | Implements data encryption, secure storage, and regulatory compliance with GDPR, CCPA, and ISO/IEC standards. |
| **Application Security**              | Applies secure output handling, sanitization, and context-aware filtering to prevent SQL injection, XSS, and LLM-based attacks. |
| **Cloud & Edge AI Security**          | Addresses cloud-based LLM deployments, AI supply chain integrity, and edge AI security risks. |


<br>

### 1.3. Persona addressed

***Target Audience***

+ **CISO/SSO:** Governance of secure AI application development.
+ **Service Architects:** Designing resilient AI services against LLM-specific vulnerabilities.
+ **Security Architects:** Implementing security controls against adversarial LLM threats.
+ **IT Architects:** Securing AI deployment pipelines and infrastructure.
+ **SOC Operations:** Monitoring and detecting AI-specific attacks (e.g., prompt injection).
+ **Researchers/Data Scientists:** Securing LLMs and ensuring adversarial robustness.


<br><br>

***Roles and Activities***

| **Activity**                          | **Executives** | **CISO/SSO** | **Service Architects** | **IT Architects** | **Security Architects** | **IT Operations** | **SOC Operations** | **Service Operations** | **Auditors/Policy Makers** | **Researchers/Data Scientists** | **Users/Practitioners** |
|--------------------------------------------------|--------------|-------------|--------------------|---------------|-------------------|--------------|--------------|-----------------|----------------------|----------------------|------------------|
| Secure Development Lifecycle (SDLC)         | **A**            | R           | R                 | C             | C                 | C            | I            | C               | I                    | C                    | I                |
| Risk-Based Approach to LLM Security         | **A**            | R           | C                 | C             | R                 | I            | C            | I               | R                    | C                    | I                |
| Threat Modeling for LLM Applications        | I            | R           | C                 | C             | **A**                 | I            | C            | I               | R                    | C                    | I                |
| Secure AI Supply Chain Management           | **A**            | R           | R                 | C             | R                 | C            | I            | I               | R                    | C                    | I                |
| Robust Access Control & Data Privacy        | **A**            | R           | C                 | C             | R                 | R            | C            | C               | R                    | C                    | I                |
| Secure Output Handling & Content Moderation | I            | R           | C                 | C             | **A**                 | R            | R            | C               | C                    | C                    | C                |
| AI Model Robustness & Adversarial Defense   | I            | R           | C                 | C             | R                 | C            | **A**            | C               | C                    | R                    | C                |
| Monitoring & Incident Response              | I            | R           | C                 | C             | R                 | R            | **A**            | C               | C                    | C                    | C                |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement

<br><br>

### 1.4. Guidance provided

The OWASP Top 10 for LLM Applications (2025) provides structured guidance to ensure secure AI system deployment, mitigate cybersecurity risks, and establish compliance with industry standards. Below is a summary of the key guidance outlined in the framework.


| **Category**       | **Guidance** |
|--------------------|--------------|
| ***Secure Development and Risk Mitigation*** | 1. Adopt a Zero-Trust Approach: Treat the LLM as an untrusted entity and enforce strict input validation and output filtering. <br> 2. Apply OWASP ASVS Standards: Follow Application Security Verification Standards (ASVS) for input validation, sanitization, and authentication. <br> 3. Implement Content Security Policy (CSP): Prevent Cross-Site Scripting (XSS) and code injection via secure encoding mechanisms. <br> 4. Use Parameterized Queries: Protect against SQL injection with prepared statements for database operations. <br> 5. Monitor and Log Model Activity: Deploy anomaly detection to identify suspicious behavior. |
| ***Data Protection and Privacy Considerations*** | 1. Educate Users on Secure AI Usage: Train users on safe LLM interactions and avoiding disclosure of sensitive data. <br> 2. Ensure Transparency in Data Handling: Maintain clear policies on data retention, processing, and deletion. <br> 3. Reference OWASP API Security Best Practices: Prevent API misconfigurations and protect against sensitive data leaks. <br> 4. Use Homomorphic Encryption: Secure AI processing with encrypted computations. <br> 5. Apply Tokenization and Redaction: Sanitize sensitive data before it enters the AI pipeline. |
| ***Model Security and Robustness*** | 1. Guard Against System Prompt Leakage: Conceal system prompts to prevent unauthorized access to model configurations and security rules. <br> 2. Avoid Over-Reliance on System Prompts: Ensure security controls are enforced externally, rather than relying on AI-generated constraints. <br> 3. Employ Adversarial Robustness Training: Defend against data poisoning and model inversion attacks through continuous AI security testing. <br> 4. Use Centralized ML Model Inventory: Maintain an AI Model Bill of Materials (ML SBOM) to track dependencies and security risks. <br> 5. Watermark LLM Outputs: Implement digital watermarking to detect unauthorized use of AI-generated content. |
| ***Secure AI System Operations*** | 1. Limit Model Privileges: Ensure LLMs do not have excessive permissions to execute unintended actions (Excessive Agency risks). <br> 2. Apply Rate Limiting and Quotas: Enforce throttling mechanisms to prevent unbounded resource consumption (Denial-of-Service attacks). <br> 3. Implement Multi-Agent Segregation: Ensure role-based separation for AI agents interacting with external systems. <br> 4. Monitor AI API Calls: Deploy continuous monitoring and anomaly detection for all LLM interactions with backend systems. |
| ***Incident Response and Compliance*** | 1. Define an AI Security Incident Response Plan: Establish predefined actions to contain, analyze, and remediate AI-related security breaches. <br> 2. Ensure Compliance with Global AI Security Standards: Align with NIST AI RMF, MITRE ATLAS, ISO/IEC 42001, and OWASP ML Security Top 10. <br> 3. Perform Regular Security Audits: Conduct periodic AI system assessments to ensure continued alignment with cybersecurity best practices. |


<br><br>

### 1.5. Detail on current framework

OWASP Top 10 for LLM Applications (2025) document for each risk follows a consistent structure:
+ Title & Risk Identifier (LLM01 - LLM10)
+ Description of the Risk
+ Common Vulnerability Examples
+ Prevention & Mitigation Strategies
+ Example Attack Scenarios
+ Reference Links to Related Frameworks & Research

Document aligns security best practices with MITRE ATLAS tactics and provides detailed mitigation measures using "Zero Trust Model for AI", "RBAC and OAuth-Based Access Controls", "Adversarial Robustness Training", "Watermarking and Secure AI Supply Chain Management​".


### 1.6. What is missing for defenders of AI systems

AI security requires continuous adaptation as adversaries develop new attack techniques. The OWASP Top 10 for LLM Applications must expand its scope by integrating MITRE ATLAS threat intelligence, red teaming methodologies, and AI-specific security controls. By addressing gaps in AI supply chain security, adversarial attack prevention, and incident reporting, defenders can better protect LLM applications in enterprise, cloud, and military environments.

<br><br>


## 2. References

| Framework | Referenced Material |
| --- | --- |
| Top 10 for LLM Applications 2025 | [Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) |
