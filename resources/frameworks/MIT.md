<!-- TOC start -->

- [MIT](#mit)
  - [1. MIT AI Risk Repository](#1-mit-ai-risk-repository)
    - [1.1. Overview](#11-overview)
    - [1.2. Scoping of AI system and/or cybersecurity purview](#12-scoping-of-ai-system-andor-cybersecurity-purview)
    - [1.3. Persona addressed](#13-persona-addressed)
    - [1.4. Guidance provided](#14-guidance-provided)
    - [1.5. Detail on current framework](#15-detail-on-current-framework)
    - [1.6. What is missing for defenders of AI systems](#16-what-is-missing-for-defenders-of-ai-systems)
  - [2. References](#2-references)

<!-- TOC end -->

# MIT

## 1. MIT AI Risk Repository

### 1.1. Overview

MIT FutureTech along with the University of Queensland developed the AI Risk Repository to provide an accessible and extensible overview of threats from AI.  The Risk Repository includes a website with a growing repository of over 1000 risks taken from other publications, using the corpus of publications to inform taxonomies on AI Risk.  A high level causal taxonomy and a more detailed multi-level domain taxonomy are provided as tools for policy makers, risk evaluators, industry and academic AI users, developers, and defenders.  


### 1.2. Scoping of AI system and/or cybersecurity purview

The AI Risk Repository addresses risks from the human-level capabilities of AI systems.  The domain taxonomy contains 7 main domains, of which the domain Privacy and Security contains the subdomain AI system security vulnerabilities and attacks.  Other risks MIT identifies including violations of privacy, misuse of AI to conduct fraud or cyberattacks, and misalignment of AI systems also inform defenders of AI systems of additional risks to these systems.  Risks of human overreliance on AI or human loss of agency are worth considering as a great of deal of security becomes automated with AI tools.


### 1.3. Persona addressed

This work seeks to address all stakeholders of AI risk.  As such it aims for policymakers and regulators with a comprehensive treatment of risks, and comprehensible taxonomies.  It also serves academics and researchers well, synthesizing dozens of other AI risk frameworks and taxonomies, and providing both a starting and landing spot for additional work on AI risk.  Finally it informs industry of risks of AI systems, so that safer systems may be developed.  As such, it does not specifically address cyber defenders nor defenders of AI systems.


### 1.4. Guidance provided

The causal and domain taxonomies provide common terminology to discuss AI risks.  Tying these risks to a body of knowledge detailing these risks as well as mapping to incidents manifesting the risk make the AI Risk Repository a map to additional detail on risk research.  Providing a database to record new risks and incorporate new frameworks keeps the risk map up to date.



### 1.5. Detail on current framework

**Causal Taxonomy**

The Causal Taxonomy provides three risk features, each with three values:
+ ***Entity:*** Human, Computer, Other
+ ***Intent:***  Unintentional, Intentional, Other
+ ***Timing:*** Pre-Deployment, Post-Deployment, Other

The simplicity of this enables quick assignment of the cause of a risk, pointing to preventative strategies for what, how and when a risk should be mitigated.  These features are easily explained to a wide audience, and serve as a durable risk taxonomy, with distinctions that will continue to provide value in understanding the causes of AI risk.


| **Category**       | **Level**         | **Description**                                      |
|--------------------|------------------|------------------------------------------------------|
| AI                | Decision-based    | Due to a decision or action made by an AI system    |
| Human             | Decision-based    | Due to a decision or action made by humans         |
| Other             | Ambiguous         | Due to some other reason or ambiguous factors       |
| **Intentionality**| **Type**          | **Description**                                      |
| Intentional       | Expected Outcome  | Due to an expected outcome from pursuing a goal    |
| Unintentional     | Unexpected Outcome| Due to an unexpected outcome from pursuing a goal  |
| Other            | Unspecified       | Without clearly specifying the intentionality      |
| **Timing**       | **Stage**         | **Description**                                      |
| Pre-deployment   | Before Deployment | Before the AI is deployed                          |
| Post-deployment  | After Deployment  | After the AI model has been trained and deployed   |
| Other           | Unspecified       | Without a clearly specified time of occurrence     |


**Domain Taxonomy**

The AI Risk Repository groups risk into 7 major domains, each with subdomains.  This taxonomy was built using experts synthesis of publications on AI risks, with natural language analysis to cluster the topics.  The domains and subdomains are identified in the AI Risk Repository as shown in this table: 


| **Domain**                         | **Subdomain**                                                    |
|------------------------------------|-----------------------------------------------------------------|
| **1. Discrimination & Toxicity**      | 1.1. Unfair discrimination and misrepresentation                    |
|                                    | 1.2. Exposure to toxic content                                      |
|                                    | 1.3. Unequal performance across groups                             |
| **2. Privacy & Security**             | 2.1. Compromise of privacy by obtaining, leaking, or inferring sensitive information |
|                                    | 2.2. AI system security vulnerabilities and attacks                |
| **3. Misinformation**                 | 3.1. False or misleading information                               |
|                                    | 3.2. Pollution of information ecosystem and loss of consensus reality |
| **4. Malicious Actors & Misuse**      | 4.1. Disinformation, surveillance, and influence at scale          |
|                                    | 4.2. Cyberattacks, weapon development or use, and mass harm       |
|                                    | 4.3. Fraud, scams, and targeted manipulation                       |
| **5. Human-Computer Interaction**     | 5.1. Overreliance and unsafe use                                   |
|                                    | 5.2. Loss of human agency and autonomy                            |
| **6. Socioeconomic & Environmental Harms** | 6.1. Power centralization and unfair distribution of benefits      |
|                                    | 6.2. Increased inequality and decline in employment quality       |
|                                    | 6.3. Economic and cultural devaluation of human effort           |
|                                    | 6.4. Competitive dynamics                                         |
|                                    | 6.5. Governance failure                                           |
|                                    | 6.6. Environmental harm                                           |
| **7. AI System Safety, Failures & Limitations** | 7.1. AI pursuing its own goals in conflict with human goals or values |
|                                    | 7.2. AI possessing dangerous capabilities                         |

**Ongoing Monitoring and Integrations**

The approach to create the AI Risk Repository used published data to drive the groupings, collecting a large body of information on AI Risks and determining the repeated themes.  The AI Risk Repository framework was updated in December 2024 to map additional risk frameworks or taxonomies to the AI Risk Repository, including a number of 2024 publications from leading groups on AI safety.  Regular updates such as this are required to keep frameworks applicable in a changing technological landscape.

The AI Risk Repository is mapped to the AI Incident Database, an open public repository for indexing harms or near-harms from AI systems.  The AI Risk Repository promotes a side project, the AI Incident Tracker, that maps new incidents added to the AI Incident Database to the AI Risk Repository.  This approach grounds theoretical risks with real incidents, and provides an extensible methodology to incorporate new information.

The Paris Peace Forum selected the AI Risk Repository as one the of 50 AI Projects they will promote at the 2025 AI Action Summit.  The AI Risk Repository will inform more policy makers, auditors, and AI technologists promoted in this way, and its adoption is likely to increase across the global audience.


### 1.6. What is missing for defenders of AI systems

The AI Risk Repository implications for Industry states: "As shown in our causal analysis, many risks are presented as being about AI, while in reality the mitigation of these risks requires a human doing something differently during conceptualisation, design, development, governance, or use."  While the guidance provided does indicate many mitigations to human caused risks for AI, there is little specifically informing defenders of AI systems.

Key items that would help inform defenders of AI systems about risks include:
+ A threat model that shows increased risks from attacks on AI systems
+ Decomposing AI systems into reference architectures
  + Vulnerabilities are rarely 'system' vulnerabilities, and often apply to a component
  + SPM decomposes systems to ensure their security
  + ZTA decomposes systems to ensure their security
+ Signing or authenticating provenance
  + Model Bill Of Materials, Software Bill Of Materials
  + Human signed content vs AI self-identified content 
+ Mapping Risks to Remediations
  + Associate each of the risks identified to steps that can prevent or resolve the risk


<br><br>


## 2. References

| Framework | Referenced Material |
| --- | --- |
| MIT AI Risk Repository | [MIT AI Risk Repository](https://airisk.mit.edu/) |
