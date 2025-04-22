<!-- TOC start -->

- [CISA](#cisa)
  - [1. Zero Trust Maturity Model 2.0](#1-zero-trust-maturity-model-20)
    - [1.1. Overview](#11-overview)
    - [1.2. Cybersecurity Purview](#12-cybersecurity-purview)
    - [1.3. Persona Addressed](#13-persona-addressed)
    - [1.4. Guidance Provided](#14-guidance-provided)
    - [1.5. Detail on current framework](#15-detail-on-current-framework)
    - [1.6. What is missing for defenders of AI systems](#16-what-is-missing-for-defenders-of-ai-systems)
  - [2. References](#2-references)

<!-- TOC end -->

# CISA

## 1. Zero Trust Maturity Model 2.0

### 1.1. Overview

The US Cybersecurity and Infrastructure Security Agency (CISA) published the second version of the Zero Trust Maturity Model (ZTMM) in Apr 2023.  "This ZTMM is one of many paths that an organization can take in designing and implementing their transition plan to zero trust architectures in accordance with Executive Order (EO) 14028 'Improving the Nation's Cybersecurity,' which requires that agencies develop a plan to implement a Zero Trust Architecture (ZTA).".  CISA provides a roadmap for incremental adoption of ZTA, clarifying requirements to advance maturity in Zero Trust adoption and thereby improve security.

### 1.2. Cybersecurity Purview

The Zero Trust Maturity Model provides guidance on how to enforce accurate, least privilege access decisions across information systems by assuming that any part of the system may be viewed as compromised. It provides requirements for system governance, access and use that rely on a principle of "don't trust; verify."  This notion of not trusting identities, data, network communications, workloads and even hardware until they are authenticated provides a comprehensive trusted system.  The ZTMM provides a set of levels describing the maturity of an organization's ZTA adoption, from Traditional security (no ZTA), to Initial, Advanced and Optimal ZTA maturity.  With clear best practices and a tiered system encouraging self-evaluation and improvement, the ZTMM provides a system that can characterize and systematically assist improving the security effectiveness of defenders.

### 1.3. Persona Addressed

Zero Trust Architecture is a requirement for US Federal agencies.  CISA directly addresses the security stakeholders of these agencies.  Organizations implementing a Zero Trust Architecture will have similar roles and responsibilities.  The division of responsibilities may vary from organization to organization, but they will generally require executives accountable for driving implementation, architects informing proper implementation, and operators responsible for many implementation details.

***Roles:***  CT/R/IO, CISO, Security Architect, Data Architect, Service Architect, Network Architect, IT, SOC<br> 
***Activities:***  Comply with EO, Enterprise security architecture, Security tooling and deployment, Incident response, Data governance, Identity governance, Asset governance<br>
***Level of responsibility***
+ ***Accountable*** - highest, final authority for the task
+ ***Responsible*** - high, one who completes the task
+ ***Consulted*** - medium, provide input to complete the task
+ ***Informed*** - low, informed about the task

| Activity\Role | C[T/R/I]O | CISO | Security Architect | Data Architect | Service Architect | Network Architect | IT Operator | SOC Operator | 
| ------------- | --------- | ---- | ------------------ | -------------- | ----------------- | ----------------- | ----------- | ------------ |
| Comply with EO | R | **A** | C | C | C | C | I | I |
| Enterprise Security Architecture | I | R | **A** | C | C | C | I | I |
| Security Tooling and Deployment | C | **A** | R | C | C | C | R | R |
| Incident Response | I | **A** | C | C | C | C | I | R |
| Data Governance | I | **A** | C | R | C | C | R | I |
| Identity Governance | I | **A** | C | C | C | R | R | I |
| Asset Governance | I | **A** | C | C | C | C | R | I |

### 1.4. Guidance Provided

The Zero Trust Maturity model informs security stakeholders about their level of Zero Trust Architecture adoption.  It promotes the principle of least privileged access across the domains of data, identity, network, devices and application workloads.  The Zero Trust Maturity model identifies 4 levels of adoption for each of these domains, or pillars.  Traditional maturity implies Zero Trust has not yet been adopted for that domain.  Initial, Advanced and Optimal maturity reflect subsequent levels of ZTA adoption, according to specific features for that domain.  There are also 3 cross-cutting features, apply to all of these pillars individually and across pillar boundaries.  These include Governance as a foundation, Automation and Orchestration above this, and Visibility and Analytics resting on top of these.  This Zero Trust Maturity Model framework provides a roadmap for stakeholders to implement Zero Trust Architecture.

### 1.5. Detail on current framework

**Zero Trust Principles**

***NIST SP 800-207 defines the tenets of Zero Trust:***
1. All data sources and computing services are considered resources.
2. All communication is secured regardless of network location.
3. Access to individual enterprise resources is granted on a per-session basis.
4. Access to resources is determined by dynamic policy—including the observable state of client identity, application/service, and the requesting asset—and may include other behavioral and environmental attributes.
5. The enterprise monitors and measures the integrity and security posture of all owned and associated assets.
6. All resource authentication and authorization are dynamic and strictly enforced before access is allowed.
7. The enterprise works with the Organizations to catalog and inventory existing Cyber Security policies and standards. Policies are updated and created in cross pillar activities as needed to meet critical ZT Target functionality.

Throughout, the principle that no asset nor identity has any inherent trust is reiterated; defenders should assume there is a current breach and take extra steps to establish trust. This applies to all assets and identities within an organization.  The context of an identity's access to a resource should be rich enough to conclude that authorization is warranted, e.g. using multi-factor authentication combined with network and device attestation signals.  These tenets guide the best practices for the different pillars the ZTA uses to specify architectural components.


**Zero Trust Pillars**

The Zero Trust Architecture defines enterprise architectures as comprised of 5 pillars: Data, Identity, Devices, Network Communications, and Application Workloads.
+ Data includes all digital artifacts from files, metadata and fragments to databases to all data in transit, archived, or used at some point
+ Identity refers to the attributes that uniquely define a human or non-human user
+ Devices include all the organizations compute assets, including servers, laptops, network edge devices, printers, and IoT devices
+ Network refers to all communication media, including internal networks, wireless, the global Internet, and other channels for communicating digital information
+ Application Workloads includes programs and services running on organization assets - on-premise, on mobile or in the cloud

The ZTMM maps security implementations for each of the pillars to 4 levels of maturity, based on specific security features required for that pillar to adhere to the Zero Trust principles. The granularity of recommendations enable stakeholders to assess their Zero Trust maturity across these domains and provide steps to Optimal ZTA maturity.  For each pillar, these are the pillar specific features:
+ Data:  Data Inventory Management, Data Categorization, Data Availability, Data Access, and Data Encryption
+ Identity: Authentication, Identity Storage, Risk Assessment, Access Management
+ Devices: Policy and Compliance, Supply Chain Risk Management, Resource Access, Device Threat Protection
+ Network: Segmentation, Traffic Management, Traffic Encryption, Network Resilience
+ Application Workload: Application Access, Application Threat Protection, Application Accessibility, Secure Development Lifecycle, Application Security Testing

<img src="./frameworks/images/Zero-Trust-Maturity-Model-Pillars-from-CISA-2156918887.jpg" alt="Zero Trust Pillars" style="width:40%; height:auto;">

**Zero Trust Cross-Cutting Features**

The ZTMM identifies 3 features that cut across the pillars:  Governance, Automation and Orchestration, and Visibility and Analytics.  Governance serves as the foundation of the Zero Trust pillars.  Organizations must govern their assets and identities, fully aware of all data,, network communication, and application workloads.  Compliance with external and internal policy enforces governance.  This requires Automation and Orchestration of tooling required for the pillar or pillars, enabling comprehensive processes for governance.  Visibility and Analytics, whether from simple measurements and detection rules or complicated behavioral analytics, provide the mechanisms for ensuring that each pillar complies with governance.

"These three cross-cutting capabilities highlight activities to support interoperability of functions across pillars based on the following descriptions: 
+ Visibility and Analytics: Visibility refers to the observable artifacts that result from the characteristics of and events within enterprise-wide environments. The focus on cyber-related data analysis can help inform policy decisions, facilitate response activities, and build a risk profile to develop proactive security measures before an incident occurs.  
+ Automation and Orchestration: Zero trust makes full use of automated tools and workflows that support security response functions across products and services while maintaining oversight, security, and interaction of the development process for such functions, products, and services.  
+ Governance: Governance refers to the definition and associated enforcement of agency cybersecurity policies, procedures, and processes, within and across pillars, to manage an agency's enterprise and mitigate security risks in support of zero trust principles and fulfillment of federal requirements."

### 1.6. What is missing for defenders of AI systems

The Zero Trust Maturity Model explicitly excludes recommendations on best practices for incorporating machine learning and artificial intelligence capabilities with Zero Trust. However, the fundamental concepts introduced by Zero Trust---least privilege, assumption of breach, and continuous authentication and authorization---are relevant for developers of AI systems that have access to sensitive data sets.

***AI Data Access Patterns***
The Zero Trust Maturity Model does not address typical deployments of AI systems, including Retrieval Augmented Generation.  AI is data driven, and vector databases are built for speed and not with Zero Trust access and encryption standards in mind.  The data access patterns for AI systems must implement the controls for proper Zero Trust Architecture, and this guidance is missing.

***AI Training Data Provenance***
If the training data for models is unknown, and the models can reproduce this data, then it is considered ungoverned data in the Zero Trust Architecture. This means that data used to train models must be known and available in order to ensure it complies with policy.  Building trust in that data requires some authentication of it, to verify that it is reputable data.

***AI Authorization Patterns***
Observing the principle of least-privileged access is often ignored in AI adoption, in order to facilitate AI access to data or tools.  The identity of AI application workloads should respect this principle by minimizing access to the least privilege among the AI user and the AI system privileges itself.  User access should not trampoline through AI system use, nor should AI systems provide more authority to users than they are otherwise allowed.

***AI Agency***
The Zero Trust Maturity Model emphasizes that no asset has inherent trust, and therefore, any access to resources must be gated through an authorization mechanism to re-validate the asset's ability to access that resource. While this approach can, and should, be applied to AI systems, there is no explicit mention of constraining the agency of AI systems to make authorization decisions in the ZTMM. The ZTMM does not call out the 

***AI Model Visibility and Analytics***
The behavior of AI systems must be established through monitoring its use.  Since these are stochastic systems, they are prone to produce unpredictable results (hallucinations).  Behavior can change as model versions are updated, and even as prompt templates are modified.  Establishing baseline behavior for AI models is required to understand when they are producing anomalous results.

***AI Driven Conclusions***
Governance for AI driven conclusions is required to ensure that automations comply with internal and external policies.  Determining what conclusions require humans-in-the-loop and what automations are resource limited will mitigate many risks.  Increasing the transparency and explainability of AI systems and requiring them in some use cases will also reduce opaque decision making.

***AI Resilience from Adversarial Attacks***
Vulnerability management for AI systems is a new and changing domain.  Novel attacks against AI systems continue, and the resilience of these systems needs to be increased.  ZTA adoption requires better characterization of AI system attack surface and weaknesses, so that proper defenses may be deployed.

<br><br>

## 2. References

| Framework | Referenced Material |
| --- | --- |
| Zero Trust Maturity Model | [Zero Trust Maturity Model](https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf) |
