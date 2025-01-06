
# Technical Steering Committee (TSC) Brief on Workstreams

## Governance and Logistics 

### How do we organize our work 
OASIS Staff will help with any issues with the WS tools. Please contact [Claudia Rauch](mailto:claudia.rauch@oasis-open.org), either via email or on Slack.

* **Slack groups**  
  * \#ws1-supply-chain  
  * \#ws2-defenders  
  * \#ws3-sec-governance  
  * Guidance on usage of Slack channels in the channel  
* **Google drive**  
  * [TSC folder](https://drive.google.com/drive/folders/1bKp-Byf6wiqjihoXrLw1_DEUq_35arxj?usp=sharing)  
  * [WS1 folder](https://drive.google.com/drive/folders/1jOKqSdJTQLKmcaX12Ldys1Zezmg2iQQ1?usp=sharing)  
  * [WS2 folder](https://drive.google.com/drive/folders/17meHzILhwaNS_OdrrauDq5OmlR3mXN39?usp=sharing)  
  * [WS3 folder](https://drive.google.com/drive/folders/1Ksx0_GF_1lGLP8MueUjgmW7Ef-Qnhxwz?usp=sharing)  
* **Github**  
  * [https://github.com/cosai-oasis](https://github.com/cosai-oasis)   
  * One folder for each work stream (with be created by OASIS)  
  * Co chairs will be maintainers of the WS  
* **Meeting Link**  
  * To be provided by one of the co-chairs   
* **Mailing lists**  
  * [Supply Chain Security WS list](https://lists.oasis-open-projects.org/g/cosai-supply-chain-ws)  
  * [Preparing Defenders WS list](https://lists.oasis-open-projects.org/g/cosai-defenders-ws)  
  * [AI Risk Governance WS list](https://lists.oasis-open-projects.org/g/cosai-risk-governance-ws)

### Logistics expectations for each workstream: 

**Workstream chairs lead weekly meetings that include:**

* Setting and driving an overall technical agenda (within scope described below)   
* Setting a per-meeting agenda and scheduling weekly meetings  
  * OASIS staff can help with calendar invitations  
* Capturing and sharing minutes with the mailing group  
* Following up on action items  
* Inviting Akila and JR to kickoff meetings

**Key responsibilities:**  
* Review and follow the [Workstream Governance Guidelines](https://github.com/cosai-oasis/oasis-open-project/blob/main/TSC-WS-GOVERNANCE.md)  
* Facilitate voting as needed (OASIS staff available for support)  
* Implement decision-making processes like lazy consensus  
* Manage GitHub repository including documentation, issues/PR backlog  

**Reporting structure:**  
* Provide regular progress updates to TSC (weekly updates and bi-weekly syncs)

### Milestones from TSC and Call to Action for WS Leads

* **Due by Oct 21st:**  
  * Review: [TSC Milestones and deliverables](https://github.com/cosai-oasis/oasis-open-project/blob/main/CHARTER.md#5-milestones-and-deliverables)   
  * Initial kickoff sessions for WS  
  * Establish weekly cadence  
* **Due by Nov 18th:**  
  * Define workstream focus areas  
  * Develop technical agenda based on provided scope. example:  
    * Focus area is “Model use and selection: How can consumers be assured about the controls that have been in place during the training/tuning of models?” Based on this, create a workback plan.  
  * Create timeline for achieving workstream goals before EOY  
* **Due by Dec 31st**  
  * A paper offering a preliminary expertise and landscape survey from members on each of the 3 founding WS  
    * Software Supply Chain Security for AI systems  
      * Including composition and provenance and use in AI Applications  
    * Preparing Defenders for a Changing Cybersecurity Landscape  
      * Including needed investments for a changing threat landscape  
      * Common pitfalls and patterns related to integration of AI and classical systems  
    * AI Security and Privacy Governance  
      * Including best practices/scorecard for analyzing risk related to AI security and your processes  
* **Ongoing oversight:**   
  * Biweekly check-ins with TSC chairs to track progress  
  * Review workstream advancement and address blockers as needed

## Technical guidance

### Introduction

CoSAI’s Project Governance Board has established three foundational workstreams to launch CoSAI's activities:

1. Software Supply Chain Security for AI Systems  
2. Preparing Defenders for a Changing Security Landscape  
3. AI Risk Governance

This document outlines the goals and scope for each workstream, providing detailed guidance for cross-industry teams. These guidelines will serve as a foundation for developing appropriate best practices, frameworks, and standards.

### Workstream 1: Software Supply Chain Security for AI Systems

#### Workstream Leadership: 
This workstream will be led by: 
* Matt Maloney, Cohere  
* Jay White, Microsoft  
* Andre Elizondo, Wiz

#### Scope
Significant efforts are ongoing to extend SSDF and SLSA principles to the security of AI development. Classical software SSDF and SLSA solutions provide the foundation for secure software development yet the individual organizations continue to face challenges integrating provenance solutions into their infrastructure and development practices including determining how to address changes in provenance proofs, shifts in publisher trust, etc... As the efforts to expand provenance controls into the AI domain advance, this CoSAI workstream will focus on lowering the barriers to AI provenance adoption and risk management.

For the purposes of this workstream, provenance has the meaning defined in NIST SP 800-53 Rev. 5, and does not include broader considerations such as copyright/IP.

#### Targeted Persona
* AI application developers who consume the model  
* Data Scientists  
* Model creators

#### Classes of Use Cases
The following classes of use cases are in scope: 

##### *Model selection and use:*

* How do I compare two fit-for-purpose models, in terms of the risk posed by using one model vs. another?   
* How can consumers be assured about the controls that have been in place during the training/tuning of models?  
* How can consumers confirm the integrity of synthetic and existing non-AI generated data prior to using it in their Ai applications? What governance do consumers need to confirm the integrity of the data?  
* What sovereign/geo-specific policies apply to the usage of the models?

##### *Model governance technical controls:*

* How do I reflect the dependencies of my application on the models and in turn, the models on the data that has been used to train/tune them?   
* How do we secure against the malicious dependencies in OSS models while safely using their capabilities?  
* How can one ensure the integrity of the models being used?  
* How does a model creator surface necessary usage governance information to the model user?   
* How can an app developer confirm the security of their data when they use a model?  
* Should we have standardized versioning of a model?   
* How do i validate using sanitized data for model pre-training/post training  
* Data Poisoning: Evaluate the model's resilience to training data contamination, where an attacker introduces malicious samples to influence the model's behavior.

##### *Model usage/prompt security:*

* Input Manipulation Resistance. Assess the model's robustness against carefully crafted inputs designed to fool the model.  
* Model Extraction Protection  
* Privacy Preservation: Protect against attacks that could reveal training data by sanitizing user prompts before sending them to the model. Develop techniques to remove or mask personally identifiable information while maintaining prompt effectiveness. This helps preserve user privacy when interacting with AI models.  
* Backdoor Detection: Evaluate the model for hidden functionalities that could be triggered by specific, unusual inputs

#### *What is not in scope:*

* Aspects of Provenance such as copyright information, licensing information and terms and conditions.

#### Reference materials

* [https://github.com/cosai-oasis/oasis-open-project/blob/main/WORKSTREAMS.md](https://github.com/cosai-oasis/oasis-open-project/blob/main/WORKSTREAMS.md)   
* [https://github.com/cosai-oasis/oasis-open-project/blob/main/CHARTER.md\#8-initial-contributions-from-existing-work](https://github.com/cosai-oasis/oasis-open-project/blob/main/CHARTER.md#8-initial-contributions-from-existing-work)   
* Model cards, fact sheets etc  
* Model signing and attestation (sigstore etc)  
* Extensions SLSA extended to MLSecOps  
* Model cards  
  * OpenAI: [OpenAI o1 System Card](https://assets.ctfassets.net/kftzwdyauwt9/67qJD51Aur3eIc96iOfeOP/71551c3d223cd97e591aa89567306912/o1_system_card.pdf)  
  * Anthropic: [The Claude 3 Model Family: Opus, Sonnet, Haiku](https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf)   
  * IBM: [AI FactSheets 360](https://aifs360.res.ibm.com/) Granite 

#### Possible Deliverables 

* Guidance and best practices regarding the evaluation of model and data provenance statements  
* Approaches for addressing model provider provenance risks as an organization integrates 3rd-party models  
* Best practices for evaluating full AI application provenance including the classical software elements and the AI models  
* Proposals for the inclusion of additional provenance data to enable high-efficacy model provenance evaluation, such as:  
  * Who performed the training and which phase of training (e.g., pre-training, feature engineering, fine-tuning, prompt engineering, etc)  
  * Governance and oversight of the training processes  
  * Development lifecycle tampering controls and evidence  
  * Training environment controls  
* Training data geography, geographical constraints on use, etc  
* How do Data-\>Model-\>Generation claims connection/transit through elements like C2PA etc.

### Workstream 2: Preparing Defenders for a Changing Security Landscape 

#### Workstream Leadership 

This workstream will be led by: 
* Vinay Bansal, Cisco  
* Josiah Hagen, Trend Micro

#### Scope 

Develop a defender’s framework to identify needed investments to address the security impacts of AI use by business applications, attackers, and defenders as well as mitigations techniques and best practices. The Defender’s framework aims to scale investments and mitigation strategies with the emergence of pivotal offensive cybersecurity advancements in AI models.

#### Targeted Persona

* CISO  
* Security Practitioners  
* AI application developers

#### Classes of Use Cases

The following classes of use cases are in scope: 

##### *Threat and vulnerability management:*

* How can we participate in an AI ecosystem of vendors to get timely access to disclosure of AI product vulnerabilities, e.g., access to PSIRT information via CISA’s JCDC, an AI-ISAC or other construct  
* What are the threat and vulnerability advisories around AI artifacts (models, data etc) and how can I get access to such feeds in a programmatic way?

##### *AI Attack surface management:*

* Developing anomaly detection systems for AI model usage patterns  
* Creating guidelines for logging and auditing AI model interactions  
* Establishing frameworks for detecting potential model abuse (e.g., unusual query patterns, output anomalies, detecting and preventing social engineering attacks that leverage AI)  
* Implementing secure APIs with advanced authentication and rate limiting  
* Developing tools for monitoring model drift and unexpected behaviors  
* Determine if the AI models being used in my enterprise are being abused?  
* How can I ensure that the models used in my enterprise have not been subjected to distillation attacks?  
* Establishing guidelines for verifying the authenticity of digital communications from a human and not from an AI agent

##### *Human-AI Interfaces and Collaboration*

* Establishing best practices for human oversight of AI systems in critical applications  
* Implementing "human-in-the-loop" processes for high-stakes AI decisions

#### *What is not in scope:*

* Security for AI autonomous agents  
* Security of Agentic Frameworks

#### *Possible Deliverables:* 

* Education around the coming wave of vulnerability discovery and agent-driven attacks  
  * What does a threat intel feed on AI Attacks look like?   
  * How does one get access to such a feed?  
* Recommendations for avoiding abuse of publicly accessible LLMs from being co-opted as intelligence in attacks  
* Avoiding distillation attacks, especially from advanced attackers  
* Coordinated Disclosure in AI Contexts (e.g. AI-ISAC possibilities, PSIRT leverage for AI product vuln, etc)   
  * How to balance accelerating attackers, and informing defenders?  
* Education and guidance on how to build AI Red Teaming capabilities that are needed for developers of software and hardware for AI solutions as well as user of AI framework  
* Definition of training corpus and materials required to support the development of AI agent(s) to support defenders, DCR: Access to compute for learning.  
* Detection patterns for abusive inputs

### Workstream 3: AI Risk Governance

#### Workstream Leadership 

This workstream will be led by: 

* Jay White, Microsoft  
* Lauren Clark, Thomson Reuters  
* Manhar Arora, EY

#### Scope 

Develop a risk and controls taxonomy, checklist, and scorecard to guide practitioners in readiness assessments, management, monitoring, and reporting of their AI products, services, and components.

#### Targeted Persona

* Chief Risk Officers  
* Compliance Officers  
* CISOs, CIOs, and CEOs  
* Policy and regulation framers

#### Classes of Use Cases

The following classes of use cases are in scope: 

##### *Governance when introducing AI to your company*

* What are the dimensions of AI Risk that apply in my industry and company that I need to address in my AI application governance?  
* What are the applicable AI regulations in my geography, my industry etc?  
* What are the policies that are applicable in my industry and my company?  
* What is an organizational heat-map for AI risk?  
* What sovereign/geo-specific policies apply to the usage of the models?

##### *Governance when using AI* 

* What is the oversight process for usage of AI and how is it administered in my company?  
* What business controls and technical controls are needed to govern the usage of AI in my enterprise?  
* What specific PETS can I harness to demonstrate compliance?  
* Internal policies, external regulations, government policies  
* Explainability and transparency on model decision making   
* What aspects of the model governance need to be surfaced to application developers?

##### *Governance to users and external authorities*

* What is a sufficient trail of evidence to prove compliance with controls?  
* How can external authorities use model cards to understand models leveraged by an organization?

#### *What is not in scope:*

* AI being used for 'job loss' etc   
* Trustworthy AI

#### *Reference materials:*

* IBM Whitepaper: [https://ibm.biz/genaiwhitepaper](https://ibm.biz/genaiwhitepaper)

#### *Possible Deliverables:* 

* Executive risk committee stakeholder recommendations (particularly around C-suite AI ownership)  
* Suggest a tiered approach based on high, medium, low risks and corresponding controls. Map to evolving regulatory expectations.  
* Tradeoffs of data control invariants and PETs [(link)](https://en.wikipedia.org/wiki/Privacy-enhancing_technologies) including Differential Privacy, TEEs / confidential computing, etc and the related impacts to model performance or other security and technical robustness properties  
* Launch rubric or scorecard for evaluating organizational readiness for secure AI integration and use, based on the capability of the AI system

