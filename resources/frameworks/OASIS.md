<!-- TOC start -->

- [OASIS](#oasis)
  - [1. STIX 2.1](#1-stix-21)
    - [1.1. Overview](#11-overview)
      - [1.1.1. Scoping of AI system and/or cybersecurity purview](#111-scoping-of-ai-system-andor-cybersecurity-purview)
      - [1.1.2. Persona addressed](#112-persona-addressed)
      - [1.1.3. Guidance provided](#113-guidance-provided)
    - [1.2. Detail on current framework](#12-detail-on-current-framework)
      - [1.2.1. Core Architecture](#121-core-architecture)
      - [1.2.2. Application for AI Systems](#122-application-for-ai-systems)
    - [1.3. What is missing for defenders of AI systems](#13-what-is-missing-for-defenders-of-ai-systems)
  - [2. References](#2-references)

<!-- TOC end -->


<!-- TOC --><a name="oasis"></a>
# OASIS


<br><br>

<!-- TOC --><a name="1-stix-21"></a>
## 1. STIX 2.1

<!-- TOC --><a name="11-overview"></a>
### 1.1. Overview

The Structured Threat Information Expression (STIX) 2.1 framework is a robust standard designed to facilitate the exchange and representation of Cyber Threat Intelligence (CTI) in a structured, machine-readable format. As artificial intelligence becomes increasingly integrated into cybersecurity systems, defenders require robust frameworks to analyze, respond to, and prevent cyber threats. STIX 2.1, with its structured approach to Cyber Threat Intelligence (CTI), offers key advantages for AI systems defending against advanced threats. 


<br><br>

<!-- TOC --><a name="111-scoping-of-ai-system-andor-cybersecurity-purview"></a>
#### 1.1.1. Scoping of AI system and/or cybersecurity purview


| **Aspect**               | **AI System Scope**   | **Cybersecurity Purview**   |
|--------------------------|-----------------------|-----------------------------|
| **Threat Modeling**      | Building predictive models using STIX objects and relationships.                | Defining comprehensive threat profiles and attack chains.                       |
| **Data Integration**     | Ingesting STIX data from diverse sources for machine learning.                  | Aggregating intelligence into a centralized repository for operational use.      |
| **Pattern Matching**     | Translating STIX patterns into detection rules for AI-driven automation.        | Deploying STIX patterns in security tools for proactive threat identification.   |
| **Graph Analytics**      | Using graph neural networks (GNNs) for attack path analysis.                   | Employing graph-based relationships to map real-world attack vectors.           |
| **Automation**           | Automating detection, classification, and response actions.                    | Streamlining incident response workflows with automated threat analysis.         |
| **Governance**           | Applying confidence scoring and marking definitions to filter intelligence.     | Ensuring adherence to compliance requirements and protecting sensitive data.     |


<br><br>

<!-- TOC --><a name="112-persona-addressed"></a>
#### 1.1.2. Persona addressed


| **Task/Responsibility**                                    | **AI Systems Defender** | **CTI Analyst** | **Threat Hunter** | **SOC Analyst** | **CTI Producer** | **CTI Consumer** | **Red Team Operator** | **Blue Team Operator** | **Researcher** | **Responder** | **Data Scientist/ML Engineer** | **Platform Developer** | **Policy Maker** | **Threat Actor** |
|------------------------------------------------------------|--------------------------|-----------------|-------------------|-----------------|------------------|------------------|-----------------------|------------------------|----------------|---------------|-----------------------------|-----------------------|------------------|------------------|
| **Define threat models**                                   | R                        | A               | C                 | C               | C                | I                | C                     | A                      | A              | C             | C                           | C                     | I                |                  |
| **Analyze Indicators of Compromise (IOCs)**                | A                        | R               | R                 | A               | C                | I                |                      | C                      | C              | A             | C                           | C                     |                  |                  |
| **Create STIX-based CTI objects**                          | C                        | R               | C                 | C               | A                | I                |                      | C                      | A              | C             | C                           | C                     |                  |                  |
| **Automate detection using STIX patterns**                 | A                        | C               | C                 | R               | I                | C                |                      | C                      | C              | C             | R                           | A                     | I                |                  |
| **Develop detection models for emerging threats**          | R                        | C               | C                 | I               | C                | I                | C                     | C                      | A              | I             | A                           | C                     | I                |                  |
| **Monitor and respond to STIX-based alerts**               | R                        | I               | I                 | A               | C                | C                |                      | A                      | I              | R             | I                           | I                     |                  |                  |
| **Generate and share CTI in STIX format**                  | C                        | R               | C                 | I               | A                | C                |                      | I                      | R              | I             | C                           | A                     |                  |                  |
| **Investigate incidents and trace attack paths**           | I                        | C               | C                 | A               | C                | C                |                      | R                      | C              | A             | C                           | C                     |                  |                  |
| **Simulate attack scenarios for testing**                  | C                        | C               | C                 | I               | C                | I                | A                     | R                      | I              | C             | C                           | C                     |                  |                  |
| **Extend STIX objects with custom properties**             | R                        | C               | I                 | I               | C                | C                |                      | C                      | R              | I             | A                           | R                     | I                |                  |
| **Integrate STIX with AI-driven platforms**                | A                        | I               | C                 | I               | I                | C                |                      | I                      | I              | I             | R                           | A                     |                  |                  |
| **Ensure compliance with CTI sharing policies**            | I                        | I               | I                 | I               | C                | C                |                      | I                      | I              | I             | C                           | C                     | A                |                  |
| **Map attacker behavior using STIX and MITRE ATT&CK**      | A                        | R               | R                 | A               | C                | C                |                      | R                      | C              | A             | C                           | C                     | I                |                  |
| **Disseminate tailored CTI to partners**                   | C                        | R               | I                 | I               | A                | R                |                      | C                      | R              | I             | I                           | C                     |                  |                  |
| **Identify vulnerabilities and recommend mitigations**     | A                        | C               | C                 | C               | C                | I                |                      | R                      | R              | C             | C                           | C                     | I                |                  |
| **Produce intelligence on attacker motives and techniques**| C                        | R               | C                 | C               | A                | I                |                      | I                      | A              | I             | I                           | C                     |                  |                  |
| **Exploit vulnerabilities for red-teaming purposes**       |                          |                 |                   |                 |                  |                  | R                     | C                      | I              | I             | I                           | I                     |                  | A                |
| **Adapt AI models based on new STIX intelligence**         | A                        | C               | I                 | I               | C                | C                |                      | I                      | I              | I             | R                           | I                     |                  |                  |
| **Develop and maintain STIX-compatible CTI platforms**     | I                        | C               | C                 | I               | C                | C                |                      | C                      | C              | I             | C                           | A                     | I                |                  |
| **Test AI models using simulated STIX objects**            | A                        | C               | C                 | I               | I                | I                | C                     | C                      | I              | I             | A                           | C                     |                  |                  |

---

***Legend:***
- **R** = Responsible (Performs the task/work)
- **A** = Accountable (Ultimate authority and decision-maker)
- **C** = Consulted (Provides input and expertise)
- **I** = Informed (Kept in the loop)

<br><br>

<!-- TOC --><a name="113-guidance-provided"></a>
#### 1.1.3. Guidance provided


| **Feature**    | **Guidance**        | **Relevance for AI Systems**   |
|----------------|---------------------|--------------------------------|
| **Structured and Machine-Readable Data** | STIX objects are serialized in UTF-8 JSON, ensuring consistency and standardization.          | Enables seamless ingestion and pre-processing of structured data for training and inference.                     |
| **Comprehensive Threat Representation** | Provides Domain Objects (SDOs) for high-level CTI and Cyber-observable Objects (SCOs) for technical details. | Allows AI to model complex attack chains and conduct graph-based analytics for uncovering threat patterns.       |
| **STIX Patterning for Detection Logic** | Defines a domain-specific language (DSL) for describing detection rules and patterns.         | Translates STIX patterns into actionable detection logic for automated systems.                                  |
| **Confidence Scoring**                | Assigns confidence levels to objects and relationships to indicate data reliability.          | Supports probabilistic decision-making and prioritization of high-confidence intelligence.                       |
| **Open Vocabularies for Standardization** | Uses predefined vocabularies for Threat Actor sophistication, Malware types, and Attack Motivations. | Improves accuracy in AI model classification and ensures interoperability across datasets.                       |
| **Extensibility for Customization**   | Allows the addition of new attributes and creation of custom object types.                    | Enables customization for AI-specific metadata like anomaly scores or unique threat landscapes.                  |
| **Relationship Mapping**              | Defines connections between objects (e.g., "Indicator indicates Malware").                   | Enables graph-based analytics and prediction of attack paths.                                                   |
| **Real-Time Intelligence Sharing**    | Integrates with TAXII to enable live data transport and updates.                              | Ensures AI systems receive up-to-date threat intelligence for dynamic adaptation.                                |
| **Data Markings for Governance**      | Includes marking definitions for sharing restrictions and handling guidelines.                | Helps AI systems comply with data governance and process sensitive data securely.                                |
| **Historical Context with Versioning** | Tracks changes to objects through versioning.                                                | Provides historical data for training models and analyzing threat evolution.                                     |
| **Integration with Complementary Standards** | Aligns with MITRE ATT&CK, ATLAS and CAPEC for tactics, techniques, and attack patterns.             | Enriches AI-based threat modeling by mapping observed activity to known attacker behavior.                       |
| **Supporting Graph-Based Models**     | Represents CTI as a graph of nodes (objects) and edges (relationships).                       | Facilitates the use of graph neural networks (GNNs) and advanced analytics for anomaly detection and prediction. |
| **Examples and Schema for Implementation** | Includes JSON examples and validation schemas for all STIX object types.                     | Accelerates AI model development and ensures data integrity for training and inference.                          |


<br><br>

<!-- TOC --><a name="12-detail-on-current-framework"></a>
### 1.2. Detail on current framework

<!-- TOC --><a name="121-core-architecture"></a>
#### 1.2.1. Core Architecture

STIX models CTI as a graph comprising:
* Nodes: STIX Domain Objects (SDOs) and Cyber-observable Objects (SCOs).
* Edges: STIX Relationship Objects (SROs) link nodes to define their relationships.

This approach allows organizations to model complex threat environments by interconnecting key aspects such as threat actors, campaigns, vulnerabilities, and observed data.

<br><br>

***Object Categories and Their Functions***


| **Category**                | **Object Type**               | **Description**                                                                 |
|-----------------------------|------------------------------|---------------------------------------------------------------------------------|
| **STIX Domain Objects (SDOs)** | Attack Pattern               | Defines known patterns of adversarial behavior.                                 |
|                             | Campaign                     | Represents a coordinated set of malicious activities over time.                |
|                             | Malware                      | Describes malicious software, its behaviors, and its targets.                  |
|                             | Indicator                    | Provides patterns that suggest the presence of malicious activity.             |
|                             | Threat Actor                 | Profiles the entity behind attacks, including motivations and capabilities.     |
|                             | Vulnerability                | Details security weaknesses that attackers can exploit.                        |
|                             | Course of Action             | Suggests remediation or mitigation steps for threats.                          |
|                             | Infrastructure               | Describes systems or tools used by attackers to conduct operations.            |
|                             | Report                       | Aggregates threat intelligence into a narrative or summary document.           |
| **STIX Cyber-observable Objects (SCOs)** | IPv4/IPv6 Address         | Represents network IP addresses used in attacks.                               |
|                                          | File                      | Documents file details such as name, size, and hashes.                         |
|                                          | Network Traffic           | Records observed communications, such as protocols and endpoints.             |
|                                          | Process                   | Details processes executed on a system.                                       |
|                                          | Domain Name               | Represents domain names involved in an attack.                                |
|                                          | URL                       | Tracks observed or malicious URLs.                                            |
|                                          | Artifact                  | Represents raw data or binary artifacts associated with an attack.            |
| **STIX Relationship Objects (SROs)**    | Indicates                  | Links an Indicator to an observable that it detects.                          |
|                                          | Uses                      | Links Threat Actors to the tools or malware they utilize.                     |
|                                          | Targets                   | Defines the target (e.g., a sector or organization) of a Campaign or Threat Actor. |
|                                          | Related-to                | Establishes generic connections between objects.                              |
|                                          | Sighting                  | Captures instances of observables or indicators being seen in a specific context. |
| **STIX Meta Objects (SMOs)**            | Marking Definition         | Specifies how shared data can be used or distributed.                         |
|                                          | Language Content           | Adds language-specific translations or details to objects.                    |
|                                          | Extension Definition       | Defines custom properties or objects to extend STIX capabilities.            |
| **STIX Bundle**                         | Bundle                     | Groups multiple STIX objects for transport, sharing, or analysis.             | 

<br><br>

***Advanced Features***

| **Feature**               | **Description**    | **Benefits**  |
|---------------------------|--------------------|---------------|
| **Confidence Scoring**    | Assigns confidence levels to objects and relationships to indicate their reliability.            | Helps prioritize actions based on the trustworthiness of data.                                |
| **STIX Patterning**       | A language to describe detection rules and match observable activity against cyber threat data.  | Automates detection and response by identifying malicious behaviors in real-time telemetry.   |
| **Graph-Based Model**     | Represents CTI as interconnected nodes (objects) and edges (relationships).                      | Enables comprehensive mapping of threats and their interdependencies.                         |
| **Open Vocabularies**     | Standardized terms for properties like malware types, attack motivations, and actor roles.       | Ensures consistency, interoperability, and clarity across organizations and tools.            |
| **Extension Mechanisms**  | Allows new attributes or object types to be added in a standardized way.                        | Supports customization and adaptation to emerging threats without sacrificing interoperability.|
| **Object Versioning**     | Tracks changes to objects over time by maintaining a version history.                           | Enhances traceability and ensures integrity in CTI sharing.                                   |
| **Data Markings**         | Specifies handling and sharing rules for sensitive threat intelligence data.                    | Protects confidentiality and ensures compliance with data-sharing agreements or regulations.  |

<br><br>

<!-- TOC --><a name="122-core-architecture"></a>
#### 1.2.2. Application for AI Systems


| **Application**               | **Key Focus**   | **Details**   |
|---------------------------|-----------------|---------------|
| **AI-Driven Threat Detection and Response** | ***Role of STIX in AI Systems***: Provides machine-readable, structured data for AI.               | 1. Enables training of machine learning models.<br>2. Automates threat detection and responses.|
|                           | ***Real-Time Threat Intelligence Integration***: Facilitates dynamic threat monitoring and action. | 1. Detects Indicators of Compromise (IOCs) like IPs or file hashes.<br>2. Automates mitigations.|
| ***Enhanced Context for AI Models*** | ***Leveraging Domain and Observable Objects***: Builds a comprehensive threat model.              | 1. SDOs provide strategic context (e.g., motivations).<br>2. SCOs offer technical-level details.|
|                           | ***Patterning for Detection Rules***: Defines standardized logic for detection.                     | 1. Translates patterns into detection rules.<br>2. Matches threat behaviors to telemetry data. |
| ***Strengthening Automation with Relationships*** | ***Graph-Based Data Representation***: Maps nodes and edges of cyber threats.                   | 1. Links attack components like Threat Actor to Malware.<br>2. Enables advanced graph analytics.|
|                           | ***Relationship Objects for Contextual Decision-Making***: Adds depth to automated responses.      | 1. Prioritizes actions based on relationships (e.g., "indicates" vs. "targets").              |
| ***Advanced Features Benefiting AI Defenders*** | ***Confidence Scoring***: Assigns reliability levels to intelligence.                           | 1. Enables AI models to weigh and prioritize data.<br>2. Improves accuracy of automated decisions. |
|                           | ***Open Vocabularies for Standardization***: Provides consistent terms for key concepts.            | 1. Improves accuracy of AI-driven categorization.<br>2. Standardizes data for interoperability.|
|                           | ***Extension Mechanisms***: Adds flexibility to meet custom needs.                                 | 1. Tailors intelligence for unique AI systems.<br>2. Allows seamless updates for emerging threats. |


<!-- TOC --><a name="13-what-is-missing-for-defenders-of-ai-systems"></a>
### 1.3. What is missing for defenders of AI systems

While STIX 2.1 is a powerful framework for sharing and representing Cyber Threat Intelligence (CTI), there are several gaps when it comes to AI system-specific threats, including adversarial attacks, model integrity, and real-time learning. Defenders of AI systems need additional tools, object types, and relationships within the STIX framework to represent and address the unique threats posed to AI, especially as these systems become more integral to cybersecurity efforts.

The inclusion of AI-specific elements within STIX 2.1 would provide a more comprehensive approach to protecting AI models and infrastructure from cyberattacks, ensuring that AI-driven cybersecurity solutions can be as secure as possible.

***Key Missing Elements***

1. **Threat Representation for AI:** While STIX 2.1 represents traditional cyber threats well, there are no dedicated constructs for AI-specific threats (e.g., adversarial attacks, data poisoning, model evasion).
2. **AI Model Integrity and Trust:** The architecture doesn't include ways to monitor or assess AI model integrity, making it difficult to track AI-specific weaknesses.
3. **Adversarial Attacks and AI-specific Threat Chains:** Missing definitions for adversarial AI attacks (e.g., adversarial inputs, model inversion) within the STIX model makes it hard to track threats to AI systems.
4. **Dynamic Learning and Real-Time Threat Integration:** AI models evolve over time, and STIX 2.1 does not currently address continuous model updates, leaving defenders without an integrated solution for real-time learning adjustments.
5. **Storage of AI-specific Data in STIX 2.1:** There is a lack of focus on storing, querying, and sharing data about AI models and their associated data streams or continuous learning processes in a way that makes it actionable for defenders.


<br><br>

***Other Challenges and Considerations***

| **Challenge**   | **Description**          | **Impact on AI Systems**   | **Impact on Cybersecurity Operations**   |
|-----------------|--------------------------|----------------------------|------------------------------------------|
| **High Volume Data Streams**                | Managing and processing large amounts of STIX data in real-time or near-real-time scenarios.                  | Performance bottlenecks when ingesting or processing high volumes of STIX data.     | Difficult to maintain real-time detection and response at scale.                   |
|                                             |                                                                                                             | Latency in processing large volumes impacts AI decision-making speed.               | Slower response times and delayed threat detection due to high data volume.        |
| **Accuracy and Relevance of Detection**     | Ensuring that AI models correctly detect and prioritize relevant threats from large datasets.                | High false positive/negative rates if the model is trained on irrelevant data.      | Difficulty in distinguishing relevant from non-relevant threats, impacting response.|
|                                             |                                                                                                             | Misclassification of data could lead to inaccurate automated responses.             | Increased workload for human analysts due to irrelevant alerts.                    |
| **Storage and Querying Efficiency (SQL)**   | Storing and querying graph-based STIX data efficiently in relational databases.                              | SQL databases may struggle with handling highly interconnected data like STIX objects. | Performance degradation when querying for complex relationships in large datasets. |
|                                             |                                                                                                             | Complex joins for relationships can significantly slow down performance.            | Difficulty scaling SQL systems to accommodate the volume and complexity of STIX data. |
| **Storage and Querying Efficiency (NoSQL)** | Handling STIX 2.1 graph data in NoSQL databases that are designed for unstructured data.                      | NoSQL databases may face challenges maintaining relationships in graph-based data.  | Complex querying over unstructured NoSQL data may result in slow responses.       |
|                                             |                                                                                                             | Lack of structured schema leads to difficulties in querying related STIX objects.    | Inconsistent or missing relationships make it difficult to analyze threat connections. |


<br><br>

<br><br>


<!-- TOC --><a name="2-references"></a>
## 2. References

| Framework | Referenced Material |
| --- | --- |
| STIX 2.1 | [STIX 2.1](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.pdf) |


*Document was created with assistance of OpenAI ChatGPT 4o model.*