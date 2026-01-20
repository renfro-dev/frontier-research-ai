# Context Orchestration Through Agent Evolution: From Code to Cowork

This week brought a significant development in context orchestration tools with Anthropic's release of Claude Cowork [[1]](#ref-1). Described as "Claude Code for the rest of your work," this new agent represents an evolution in how leaders can orchestrate context across different types of tasks [[1]](#ref-1).

## The Agent as Context Orchestrator

Claude Cowork, now available to Max subscribers on $100 or $200 per month plans, extends the context orchestration capabilities previously limited to coding tasks [[1]](#ref-1). The tool operates through a new tab in the Claude desktop app, sitting alongside the existing Chat and Code tabs [[1]](#ref-1).

What makes this development notable for context orchestration is how it handles file access and information flow. Files appear to be mounted into a containerized environment, as evidenced by file paths like "/sessions/zealous-bold-ramanujan/mnt/blog-drafts" [[1]](#ref-1). This containerization represents a specific approach to context management—giving the AI access to selected information while maintaining boundaries.

The system can only access files you explicitly grant it permission to see [[1]](#ref-1). This design choice highlights a fundamental principle of context orchestration: curation happens at the access level, not just at the query level.

## Practical Context Orchestration in Action

Simon Willison tested Cowork with a complex context orchestration task: "Look at my drafts that were started within the last three months and then check that I didn't publish them on simonwillison.net using a search against content on that site and then suggest the ones that are most close to being ready" [[1]](#ref-1).

This single request demonstrates multiple layers of context orchestration:
- **Temporal filtering**: Finding files from the last three months
- **Cross-context verification**: Checking web content against local files
- **Synthesis**: Evaluating readiness based on multiple data sources

Cowork executed this by running system commands to find files, then performing 44 individual searches against site:simonwillison.net [[1]](#ref-1). This shows how modern context orchestration tools sequence operations—first gathering local context, then enriching it with external data.

## The Security-Context Tradeoff

Anthropic explicitly warns about prompt injection risks in their announcement [[1]](#ref-1). This surfaces a critical tension in context orchestration: the more context you give an AI system, the larger the attack surface for prompt injections.

The summarization applied by WebFetch in Claude Code and Cowork serves partly as a prompt injection protection layer, according to Claude Code creator Boris Cherny [[1]](#ref-1). This reveals how context orchestration tools must balance information richness with security filtering.

Anthropic's approach shifts some security responsibility to users, asking them to monitor for "suspicious actions that may indicate prompt injection" [[1]](#ref-1). Willison challenges this approach: "I do not think it is fair to tell regular non-programmer users to watch out for 'suspicious actions that may indicate prompt injection'!" [[1]](#ref-1).

## Containerization as Context Boundary

Cowork runs in a filesystem sandbox by default [[1]](#ref-1). This architectural choice represents a specific philosophy of context orchestration: rather than giving the AI unrestricted access and trying to filter at the query level, the system creates hard boundaries at the infrastructure level.

This approach trades flexibility for security. Leaders using such tools must decide upfront which contexts to make available, rather than dynamically adjusting access during use.

## Visual Context Generation

Beyond text and file manipulation, Cowork can generate visual content. Willison tested this by asking for "exciting animated encouragements," which Cowork created as an artifact [[1]](#ref-1). This capability extends context orchestration beyond information retrieval to content creation, though display issues were noted [[1]](#ref-1).

## Tensions & Tradeoffs

This week's developments highlight several context orchestration tensions:

1. **Access vs. Security**: Granting file access enables powerful workflows but increases prompt injection risks [[1]](#ref-1)

2. **User Responsibility vs. System Guarantees**: Anthropic acknowledges they "can't provide guarantees that no future attack will be found that sneaks through their defenses" [[1]](#ref-1)

3. **Generalization vs. Specialization**: Moving from "Claude Code" to "Claude Cowork" suggests a trend toward general-purpose context orchestration, though the interface remains similar [[1]](#ref-1)

## Your Context Orchestration Stack

Based on this week's developments, leaders should evaluate:

1. **Access Control Systems**: How do you grant and revoke context access to AI tools?
2. **Containerization Strategy**: Should sensitive contexts be isolated in sandboxed environments?
3. **Security Monitoring**: Who in your organization can realistically monitor for prompt injection attempts?
4. **Cross-Context Workflows**: Which tasks require combining local and web-based context?

The evolution from specialized coding agents to general-purpose work agents represents a shift in how we think about context orchestration. The challenge isn't just what information to surface, but how to maintain security boundaries while enabling powerful cross-context workflows.

## Sources

<a id="ref-1"></a>[1] [Willison, S. (2026, January 12). First impressions of Claude Cowork, Anthropic's general agent](https://simonwillison.net/2026/Jan/12/claude-cowork/#atom-everything)