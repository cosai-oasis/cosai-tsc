# MITRE's ATLAS Framework

## Official Web Site

[https://attack.mitre.org/](https://atlas.mitre.org/)

## Purpose and Coverage
The Adversarial Threat Landscape for Artificial-Intelligence Systems (ATLAS) extends MITRE's well-established ATT&CK framework to include adversarial machine learning threats. ATLAS helps security analysts understand and mitigate vulnerabilities specific to AI/ML systems by addressing threats such as:

- Data poisoning during collection or preprocessing
- Model evasion through adversarial examples
- Model inversion and extraction attacks
- Privacy violations through inference techniques

The framework provides a methodical approach to AI security through a curated set of vulnerabilities and adversary behaviors vetted by industry and academic research groups.

## Strengths
ATLAS effectively maps AI-specific threats and attack techniques, creating a common language for security professionals to discuss AI vulnerabilities. Its integration with the broader ATT&CK framework allows organizations to incorporate AI security into existing security programs, leveraging familiar concepts and methodologies.

## Limitations
While powerful for identifying how AI systems can be attacked, ATLAS falls short in addressing AI supply chain security specifically. The framework doesn't provide detailed prescriptive mitigations tailored to the AI domain and current ecosystems, instead relying on more traditional and generic security controls derived from the broader ATT&CK framework.

A crucial limitation is that ATLAS doesn't adequately contextualize threats within the broader AI supply chain. For example, while data poisoning is identified as a risk, the framework doesn't distinguish whether poisoning occurs at the data sourcing stage, during preprocessing, or via a compromised third-party dataset.

Additionally, ATLAS lacks comprehensive guidance on model provenance, cryptographic integrity verification, and the risks associated with using pre-trained models from untrusted sources—all critical considerations as AI systems increasingly rely on open-source tools, cloud APIs, and foundation models.
