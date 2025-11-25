# Introduction to the CoSAI Principles for Secure-by-Design Agentic Systems

## The New Security Paradigm

2025 has seen the launch of the age of agentic AI and the associated shifts in the cybersecurity landscape. As organizations deploy autonomous agents capable of making decisions, executing tasks, and interacting with other systems, we're witnessing a paradigm shift that challenges traditional security models. While foundational security approaches remain necessary, they are no longer sufficient to address the emerging challenges of prompt injection, agent identity, agent provenance, and the entirely new attack surfaces created via the interaction of independent agentic systems (agent-to-agent).

End-to-end security architectures that once protected us are now vulnerable to agent-in-the-middle attacks, while the previously known social engineering tactics are evolving into sophisticated prompt engineering attacks. Organizations may be tempted to rely on human-in-the-loop implementations as sufficient safeguards, but experience shows this creates critical latency that limits the very efficiency we seek from agents. Over-reliance on human intervention can lead to control fatigue, turning well-intentioned safeguards into security theater rather than robust controls.

This creates a fundamental optimization problem: how do we balance the speed and autonomy that make agentic systems valuable against the non-determinism and security risks they introduce? **The core challenge is enabling agentic systems to operate effectively without accepting unbounded security risk.**

To address this challenge, the [Coalition for Secure AI](https://www.coalitionforsecureai.org/) (CoSAI) is releasing our [Principles for Secure-by-Design Agentic Systems](https://github.com/cosai-oasis/cosai-tsc/blob/main/security-principles-for-agentic-systems.md). These principles target agent developers, adopters, and security engineers with practical implementation strategies that security teams can deploy today rather than theoretical frameworks for tomorrow.

## The Three Foundational Principles

Given the tension between leveraging agentic capabilities and minimizing the security impacts of agentic systems, CoSAI’s principles take a defense-in-depth approach. We start with the goal of enabling effective oversight and governance and then proceed to build towards that goal by containing the problem space and then ensuring the integrity of operations within it.

### Enable Human Oversight and Shared Accountability

#### Principle 1: Agentic Systems are Human-governed and Accountable

* architected for **meaningful control** with clear, **shared accountability** throughout their lifecycle.  
* subject to risk-based **actionable controls and oversight** ensuring alignment with expected business outcomes and failure recovery capabilities.  
* **constrained by** well-defined boundaries on authority and aligned with **principals’ risk tolerance**.

#### Why it matters

Meaningful human governance is the ultimate objective of secure-by-design agentic systems. All systems fail—from classical automation to modern AI systems—and humans are fallible too, but the goal is not to have humans approve every action. Instead, we must establish frameworks of accountability and strategic points of control that maximize oversight while minimizing intervention points, ensuring governance without sacrificing the speed and efficiency that make agentic systems valuable.

#### What practitioners can do

**Maximize Oversight While Minimizing Intervention:** Focus on defining and enforcing the rules of engagement for agentic systems rather than micromanaging tasks. Implement clear data governance policies dictating what data can be accessed and for what purpose, establish operational no-go zones for specific actions, and set risk-based thresholds that trigger human review. Reserve direct intervention for high-risk or anomalous events while allowing humans to adjust constraints and parameters.

**Establish Shared Accountability Models:** In ecosystems of third-party models, agents, and platforms, clearly delineate accountability between model producers, agent developers, service implementers, and human principals. Shared accountabilities should be defined and agreed upon before any model selection or system development begins and are essential not only for post-incident remediation but for proactively informing the design and placement of security controls across the agentic system.

**Implement Agile Risk-Based Governance:** Different agentic workloads carry different levels of risk, and governance models must reflect these variations. A system that summarizes news articles requires different controls than one executing financial transactions or modifying production infrastructure. Implement governance capabilities—from simple logging to multi-party approval workflows—that are explicitly tied to the risk profile of the task at hand.

### Minimize the Unknowns and the Blast Radius

#### Principle 2: Agentic Systems are Bounded and Resilient

* designed with **strict, purpose-specific entitlements** on capabilities and resource access.  
* protected by **robust, defensive measures** including foundational cybersecurity controls, confidentiality controls, and AI-specific defenses against all threat actors.  
* built for **continuous validation** of alignment with intended purposes and expected outcomes with predefined failure modes.

#### Why it matters

A core prerequisite for effective governance is containment, but this requires balance. The goal is not to over-constrain agents to the point of ineffectiveness, but to establish secure equilibrium between capabilities and potential risks. The non-deterministic nature of AI means we cannot always predict the exact path an agent will take, making strong foundational cybersecurity controls that strictly limit potential actions to expected and intended purposes critical for minimizing the impact of unexpected behavior or failure.

#### What practitioners can do

**Adapt Zero Trust for Agentic Systems:** Move beyond traditional network segmentation to micro-segmentation of agentic functions. Implement "Agentic Zero Trust" by continuously monitoring agent behavior against expected norms and validating that each action remains within defined authority. Use automated policy enforcement to bound non-determinism in real-time, treating each agent interaction as a potential threat vector while enabling necessary functionality.

**Enforce Strict, Purpose-Specific Entitlements:** Define and enforce granular controls that clearly delineate what data agents can access and what data remains out of bounds for them, as well as what tools they can use, what APIs they can call, and the capacity of compute resources they can consume. While creating granular entitlements has been historically challenging, agentic systems represent substantial amplification of potential risk from data misuse. Focus on three critical areas: data access controls specifically designed for agentic systems, computational resource and external endpoint management, and identity approaches that account for both human operators and autonomous agents.

**Design for Failure, Not Just Success:** Proactively define and architect agent failure modes through deliberate architectural evaluation. Determine appropriate failure strategies based on workload risk and potential for non-deterministic behavior, including failing-safe by halting action, degrading gracefully to limited but predictable functions, or failing-fast to prevent further unintended consequences. Account for Byzantine failure scenarios where agentic systems may fail in unexpected or adversarial ways.

### Ensure Integrity of Execution through Transparency

#### Principle 3: Agentic systems are Transparent and Verifiable

* supported by **secure AI supply chain controls** covering provenance and selection, model integrity, and runtime validation.  
* generating **comprehensive telemetry** of inputs, plans, decisions, communications, and outputs.  
* enabling **real-time monitoring, comprehension and forensic analysis** for oversight and incident response.

#### Why it matters

A governable system requires both containment and integrity. The threat landscape for agentic systems is fundamentally different—end-to-end security is broken in agent-in-the-middle scenarios, social engineering tactics are evolving into prompt engineering attacks, and agent-to-agent communication creates attack vectors that traditional monitoring approaches may miss entirely. For agentic systems, integrity means that all components and actions must be observable, their behavior and provenance verifiable, with comprehensive telemetry that enables detection of anomalous behavior at machine speed.

#### What practitioners can do

**Secure the AI Supply Chain:** An agentic system is only as strong as its weakest component. Implement controls to ensure the provenance and integrity of models, integrated tools, and the data that defines agent behavior—including training datasets, evaluation data, and core system prompts. Adapt established frameworks like SLSA to provide verifiable provenance for agent and model artifacts, use rigorous data governance to ensure integrity, and implement continuous runtime validation to verify that the system running in production is precisely the system that was approved.

**Generate Comprehensive Telemetry:** You cannot defend what you cannot see. Instrument agentic systems to produce detailed, immutable logs of inputs, internal reasoning or planning steps, tool usage, communications, and final outputs. This telemetry serves as the foundation for real-time monitoring, threat detection, and crucial forensic analysis during incident response, enabling the detection of prompt engineering attacks and agent-to-agent manipulation.

**Evolve Threat Models and Response Playbooks:** Update existing threat models to account for agent-specific vectors and adapt incident response playbooks for agentic challenges. Develop capabilities to react faster than threat actors can move through agent-enabled networks, including procedures for quarantining rogue agents and differentiating malicious, manipulated outputs from model hallucinations. Use AI systems to monitor AI systems, enabling anomaly detection and response at machine speed.

## Building a Secure Future, Together

These principles are not an endpoint, but a starting point focused on enabling innovation by providing a secure foundation for the growth of agentic systems. The security landscape for agentic systems will evolve at an incredible pace as attackers leverage agentic capabilities, compressing attack timelines and increasing the speed and scale of their campaigns. As agent-to-agent interactions become more complex, we can expect novel attack vectors and exploitation methods we haven't yet imagined, requiring defensive systems that will react faster than ever before.

The community must drive the emergence of new standards and best practices to create a common language for security and interoperability, including industry-specific frameworks and regulatory requirements specifically addressing agentic security. Critical research areas demanding immediate attention include advanced failure mode prediction and handling, real-time alignment verification techniques, robust non-human identity frameworks, cross-agent trust and verification protocols, and optimization of human-AI collaboration patterns.

By establishing clear **governance**, implementing robust **containment**, and ensuring end-to-end **integrity**, we can build agentic systems that are not only powerful but also worthy of our trust. The organizations that begin adapting their security practices early will be best positioned to safely leverage agentic systems as they become increasingly prevalent. The future of AI security isn't about choosing between innovation and protection—it's about **building systems that excel at both**.  

This is a shared challenge that requires a collective effort. We invite you to read the full principles [document](https://github.com/cosai-oasis/cosai-tsc/blob/main/security-principles-for-agentic-systems.md) and use them to guide your own work. To contribute to the ongoing development of implementation guidance and best practices, we encourage you to join the conversation in the [CoSAI working group for the secure design of agentic systems](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems) as we continue to build a secure future for agentic AI.

