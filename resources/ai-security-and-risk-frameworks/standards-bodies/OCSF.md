<!-- TOC start -->

- [OCSF](#ocsf)
  - [1. Open Cybersecurity Schema Framework (OCSF)](#1-open-cybersecurity-schema-framework-ocsf)
    - [1.1. Overview](#11-overview)
    - [1.2. Scoping of AI system and/or cybersecurity purview](#12-scoping-of-ai-system-andor-cybersecurity-purview)
    - [1.3. Persona addressed](#13-persona-addressed)
    - [1.4. Guidance provided](#14-guidance-provided)
    - [1.5. Detail on current framework](#15-detail-on-current-framework)
    - [1.6. What is missing for defenders of AI systems](#16-what-is-missing-for-defenders-of-ai-systems)
  - [2. References](#2-references)

<!-- TOC end -->

# OCSF

## 1. Open Cybersecurity Schema Framework (OCSF)

### 1.1. Overview

The Open Cybersecurity Schema Framework (OCSF) is an open-source, vendor-neutral framework designed to standardize security event data across various security products. It was created to address inconsistent log formats, interoperability issues, and complex security analytics caused by disparate security data sources. 

The cybersecurity landscape is evolving at an unprecedented pace, with organizations leveraging multiple security tools, platforms, and technologies to detect, analyze, and respond to threats. However, a lack of standardization in security event data formats has led to significant challenges:

+ ***Inconsistent Log Formats:*** Different security tools (e.g., SIEM, EDR, NDR, IDS, SOAR) generate logs in proprietary formats, making correlation complex.
+ ***Data Silos:*** Security analysts must normalize and map logs manually, delaying threat detection and response.
+ ***High Integration Costs:*** Organizations spend millions of dollars on custom connectors and ETL pipelines to unify data.
+ ***Limited Automation:*** Disparate data structures make it difficult for AI/ML models to detect anomalies efficiently.

The Open Cybersecurity Schema Framework (OCSF) directly addresses these issues by providing a standardized, vendor-neutral schema for cybersecurity event data.


### 1.2. Scoping of AI system and/or cybersecurity purview

<br><br>

***OCSF Scoping in AI Systems***

OCSF enables AI-driven security analytics by providing structured, standardized security event data. This table outlines key AI use cases and how OCSF supports them.

| **AI Functionality**   | **OCSF Guidance**    | **AI Use Cases**     |
|------------------------|----------------------|----------------------|
| **Data Standardization for AI Models**     | Ensures AI receives well-structured, normalized security event data.                              | 1. AI-driven SIEM/XDR for faster security threat detection. <br> 2. AI-based UEBA for behavioral anomaly detection. |
| **AI-Driven Security Analytics**           | Provides a common security event structure for AI correlation engines.                            | 1. AI-powered SOC automation for real-time log triage and prioritization. <br> 2. AI-enhanced attack pattern recognition. |
| **Threat Intelligence & Correlation**      | Enables AI to cross-correlate security events across multiple domains.                        | 1. AI-based forensic investigations using OCSF event metadata. <br> 2. AI-powered fraud detection for identity compromise analysis. |
| **Real-Time Threat Detection**             | Provides standardized timestamps, severity levels, and categories for ML models.                 | 1. Time-series anomaly detection for detecting security incidents. <br> 2. AI-powered intrusion detection based on OCSF-defined thresholds. |
| **Automated Incident Response**            | Enables AI-driven SOAR platforms to use structured logs for security automation.                 | 1. AI-driven automated playbooks using structured OCSF logs. <br> 2. Automated incident prioritization using AI-based risk scoring. |
| **Predictive Analytics & Threat Forecasting** | Supports AI-based predictive security models with historical event correlation.             | 1. AI-powered attack surface monitoring based on historical OCSF logs. <br> 2. AI-driven attack path prediction using event correlation. |
| **Compliance & Security Auditing**         | Helps AI-driven tools analyze logs for policy violations and regulatory compliance.          | 1. AI-driven automated compliance scanning (e.g., SOC 2, GDPR). <br> 2. AI-based security policy enforcement using NLP models. |

<br><br>

***OCSF Scoping in Cybersecurity***

OCSF enhances cybersecurity operations by providing a standardized approach to security event logging, threat detection, and compliance enforcement. This table outlines key cybersecurity domains and how OCSF supports them.

| **Cybersecurity Domain**   | **OCSF Guidance**     | **Cybersecurity Use Cases**  |
|----------------------------|-----------------------|------------------------------|
| **Security Operations (SOC)**          | Standardizes log ingestion and correlation for SIEM, XDR, and security monitoring.           | 1. Automated log correlation in SIEMs (Splunk, Sentinel, QRadar). <br> 2. Threat detection playbooks using OCSF-defined event categories. |
| Cloud Security & Zero Trust        | Enables consistent security event monitoring across multi-cloud and hybrid environments.      | 1. Cloud security monitoring in AWS GuardDuty, Azure Sentinel. <br> 2. Zero Trust access models using OCSF authentication logs. |
| Threat Intelligence & Incident Response | Maps security events to known adversary techniques for faster detection and response.       | 1. Threat intelligence platforms using OCSF for structured threat feeds. <br> 2. Incident response teams querying OCSF logs for forensic investigations. |
| Policy & Compliance Enforcement    | Simplifies audit logging, security assessments, and compliance reporting.                    | 1. Automated compliance enforcement (SOC 2, GDPR, NIST). <br> 2. Regulatory audits using OCSF event mappings. |
| Security Automation & SOAR         | Provides structured event formats for automated incident handling and response.              | 1. SOAR playbooks using OCSF for automated security workflows. <br> 2. Automated threat mitigation based on OCSF-defined alerts. |
| Forensics & Legal Defensibility    | Structures event logs to improve investigation timelines and digital forensics.              | 1. Legal defensibility through structured event retention. <br> 2. Incident reconstruction using OCSF event sequences. |


<br><br>

### 1.3. Persona addressed

***Target Audience***

+ **CISO/SSO:** Strategic alignment of security event logging and monitoring.
+ **Security Architects:** Designing structured logging and security monitoring for AI.
+ **SOC Operations:** Implementing OCSF for real-time threat detection and SIEM integration.
+ **IT Operations:** Ensuring consistent logging and monitoring for AI environments.
+ **Service Operations:** Operationalizing security monitoring for AI services.

<br><br>

***Roles and Activities***

| **Activity**                          | **Executives** | **CISO/SSO** | **Service Architects** | **IT Architects** | **Security Architects** | **IT Operations** | **SOC Operations** | **Service Operations** | **Auditors/Policy Makers** | **Researchers/Data Scientists** | **Users/Practitioners** |
|--------------------------------------------|---------------|-------------|------------------------|-------------------|------------------------|-------------------|-------------------|------------------------|----------------------------|------------------------------|-------------------------|
| Define OCSF Adoption Strategy          | **A**             | R           | C                      | C                 | C                      | I                 | I                 | I                      | C                          | C                            | I                       |
| Schema Design & Customization          | I             | I           | R                      | C                 | **A**                      | I                 | C                 | I                      | I                          | R                            | I                       |
| Integration with Security Tools        | I             | **A**           | R                      | R                 | R                      | R                 | R                 | R                      | I                          | C                            | I                       |
| Event Mapping & Normalization          | I             | C           | C                      | R                 | **A**                      | I                 | R                 | R                      | I                          | C                            | I                       |
| Security Operations & Monitoring       | I             | C           | I                      | I                 | C                      | R                 | **A**                 | C                      | I                          | I                            | C                       |
| Incident Detection & Response          | I             | C           | I                      | I                 | C                      | R                 | **A**                 | R                      | I                          | I                            | C                       |
| Data Analytics & Reporting             | I             | C           | I                      | C                 | C                      | I                 | R                 | I                      | C                          | **A**                            | C                       |
| Compliance & Audit Reporting           | I             | R           | C                      | C                 | C                      | I                 | C                 | I                      | **A**                          | C                            | I                       |
| Threat Intelligence Correlation        | I             | C           | **A**                      | C                 | C                      | I                 | R                 | I                      | C                          | C                            | C                       |
| Training & Awareness Programs          | **A**             | R           | C                      | C                 | C                      | I                 | I                 | I                      | C                          | C                            | R                       |
| Continuous Schema Improvement          | I             | C           | R                      | C                 | **A**                      | I                 | C                 | I                      | C                          | **A**                            | I                       |
| Research & Development                 | I             | C           | I                      | I                 | C                      | I                 | C                 | I                      | C                          | **A**                            | I                       |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)
- **"-"** = No direct involvement

<br><br>

### 1.4. Guidance provided

The Open Cybersecurity Schema Framework (OCSF) provides a structured and standardized approach to security event data, which directly benefits Artificial Intelligence (AI) and Machine Learning (ML) systems used in cybersecurity. OCSF helps AI-driven security analytics, threat detection, and automation by ensuring consistent, high-quality data ingestion and processing.

The structured, enriched, and extensible data model of OCSF makes it an ideal foundation for AI-driven cybersecurity solutions. By leveraging OCSF, AI models can: 

+ Improve threat detection accuracy
+ Enhance correlation and anomaly detection
+ Automate incident response
+ Support predictive analytics and risk forecasting
+ Enable AI-driven compliance monitoring

OCSF bridges the gap between raw security event data and AI analytics, making security operations more efficient, intelligent, and automated. 



### 1.5. Detail on current framework

OCSF is designed to normalize security event data while remaining flexible and extensible. The framework is structured into three main layers:

**Architectural Design of OCSF**

OCSF is structured into three primary layers: **Data Model Layer, Processing Layer, and Consumption Layer**, each playing a critical role in standardizing cybersecurity event data.

| **Layer**           | **Description**                                                                                     | **Key Components**                                                                                           |
|---------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| **Data Model Layer** | Defines the **core event schema** and organizes event data into structured formats.               | - **Event Classes** (e.g., Authentication, Network Traffic) <br> - **Categories** (logical grouping of events) <br> - **Profiles** (contextual attributes) <br> - **Extensions** (custom attributes & event types) |
| **Processing Layer** | Manages data ingestion, validation, and transformation processes.                                | - **Event Mapping** (translates raw logs to OCSF format) <br> - **Validation Engine** (ensures schema compliance) <br> - **Event Enrichment** (adds contextual data via profiles) |
| **Consumption Layer** | Enables security teams to analyze, correlate, and automate security events using OCSF-standardized data. | - **Threat Detection & Response** (SIEM, XDR, SOAR) <br> - **Incident Investigation & Forensics** <br> - **Threat Intelligence Correlation** <br> - **Security Automation & AI-driven Analytics** |

**Key Features of OCSF**


OCSF introduces several key features that enhance security data interoperability, threat detection, and automation.

| **Feature**                  | **Description**                                                                                  |
|------------------------------|----------------------------------------------------------------------------------------------|
| **Schema-Agnostic & Extensible** | Works with any storage format (JSON, Parquet, Syslog, etc.) and supports custom extensions.  |
| **Structured Taxonomy**       | Organizes security events into well-defined categories, event classes, and profiles.     |
| **Interoperability**          | Enables seamless integration across SIEM, SOAR, XDR, and cloud security platforms.        |
| **Improved Threat Detection** | Provides structured event attributes that enhance threat correlation & automation.   |
| **Lower Operational Costs**   | Reduces the need for custom log parsers and data transformation pipelines.                |
| **Supports Compliance & Regulations** | Aligns with NIST, ISO 27001, MITRE ATT&CK, and CIS Controls for standardized compliance reporting. |

**Structured Taxonomy of OCSF**

OCSF organizes security event data into six key constructs, ensuring structured classification, extensibility, and interoperability.

| **Construct**          | **Description**                                                                               | **Example Usage** |
|-----------------------|----------------------------------------------------------------------------------------------|-------------------|
| **Data Types & Attributes** | Defines primitive (strings, integers, timestamps) and complex (User, Process, Device) data types. | `IP Address`, `MAC Address`, `Timestamp`, `Process Name` |
| **Objects**           | Represents structured collections of attributes that define entities involved in an event. | `User`, `Process`, `Device`, `Network Connection` |
| **Event Classes**      | Represents specific types of security events. Each class has a unique identifier.         | `Authentication`, `File Access`, `Network Connection` |
| **Categories**         | Groups event classes into logical security domains for organization and searchability.    | `System Activity`, `Findings`, `IAM`, `Network Activity` |
| **Profiles**          | Overlays additional attributes to enrich event data with context.                         | `Malware Detection Profile`, `Cloud Profile` |
| **Extensions**        | Allows customization by adding new attributes, event classes, or categories without modifying the core schema. | Custom `IoT Security Events`, `Industry-Specific Threat Indicators` |



### 1.6. What is missing for defenders of AI systems

While OCSF (Open Cybersecurity Schema Framework) provides a structured way to standardize security event data, it currently lacks specific provisions for AI system defenders. AI-driven cybersecurity solutions require specialized telemetry, threat models, and security controls that are not fully addressed in OCSF. OCSF needs enhancements to support AI system defenders, focusing on AI-specific threat detection, logging, and governance. This table outlines key gaps, issues, and potential solutions.

| **Category**  | **Issue**   | **Potential Solution**     |
|---------------|-------------|----------------------------|
| **AI-Specific Threat Event Categories** | Lacks event classes for AI security threats (e.g., data poisoning, model evasion, adversarial ML). | 1. Introduce AI-Specific Event Classes in OCSF. <br> 2. Align with MITRE ATLAS for adversarial ML threats. |
| **AI Logging & Telemetry**            | No standard way to log AI security events (e.g., model drift, inference anomalies, training data integrity). | 1. Extend OCSF attribute dictionary to include AI telemetry. <br> 2. Define structured logs for AI model access & modifications. |
| **AI Threat Intelligence & IOCs**     | No support for AI-specific threat intelligence feeds, such as adversarial samples, model scraping, or model inversion attacks. | 1. Introduce AI-related threat intelligence fields. <br> 2. Integrate with MITRE ATLAS and AI-specific IOCs. |



<br><br>


## 2. References

| Framework | Referenced Material |
| --- | --- |
| Open Cybersecurity Schema Framework (OCSF) | [OCSF](https://ocsf.io/) |
