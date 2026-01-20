# Context Orchestration Through Agent Evolution: From Code to Cowork

This week brought a significant development in context orchestration tools with Anthropic's release of Claude Cowork [[1]](#ref-1). Described as "Claude Code for the rest of your work," this new agent represents an evolution in how leaders can orchestrate context across different types of tasks [[1]](#ref-1).

## The Agent as Context Orchestrator

Claude Cowork, now available to Max subscribers on $100 or $200 per month plans, demonstrates how agent systems are becoming general-purpose context orchestration tools [[1]](#ref-1). The interface maintains consistency with Claude Code, appearing as a new tab alongside existing Chat and Code tabs in the Claude desktop app [[1]](#ref-1).

What makes this development notable for context orchestration is how it handles file access and system interactions. Files are mounted into a containerized environment, as evidenced by paths like "/sessions/zealous-bold-ramanujan/mnt/blog-drafts" [[1]](#ref-1). This containerization represents a specific approach to context management—giving the AI access to your files while maintaining security boundaries.

## Practical Context Orchestration in Action

Simon Willison's test of Cowork reveals the practical mechanics of context orchestration [[1]](#ref-1). He asked the system to "Look at my drafts that were started within the last three months and then check that I didn't publish them on simonwillison.net using a search against content on that site and then suggest the ones that are most close to being ready" [[1]](#ref-1).

This single request triggered multiple context orchestration actions:
- File system exploration using find commands
- 44 individual web searches against site:simonwillison.net
- Analysis and recommendation generation

The system executed commands like `find /sessions/zealous-bold-ramanujan/mnt/blog-drafts -type f \( -name "*.md" -o -name "*.txt" -o -name "*.html" \) -mtime -90 -exec ls -la {} \;` [[1]](#ref-1). This shows how modern agents orchestrate context by combining file access, web search, and analytical capabilities in a single workflow.

## Security as Context Boundary Management

Anthropic's approach to security reveals a fundamental tension in context orchestration. The company states that Cowork can only access files you grant it access to, and it runs in a filesystem sandbox by default [[1]](#ref-1). However, they also warn users about the risk of prompt injections in their announcement [[1]](#ref-1).

The summarization applied by WebFetch in Claude Code and Cowork serves partly as a prompt injection protection layer, according to Claude Code creator Boris Cherny [[1]](#ref-1). This highlights how context orchestration isn't just about what information to include—it's also about filtering and protecting against malicious context.

## Tensions & Tradeoffs

The release surfaces a critical tension in context orchestration: security responsibility. Anthropic asks users to monitor for "suspicious actions that may indicate prompt injection" [[1]](#ref-1). Willison challenges this approach: "I do not think it is fair to tell regular non-programmer users to watch out for 'suspicious actions that may indicate prompt injection'!" [[1]](#ref-1).

This represents a broader challenge in context orchestration tools. As Willison notes, "Anthropic are being honest here with their warnings: they can attempt to filter out potential attacks all they like but the one thing they can't provide is guarantees that no future attack will be found that sneaks through their defenses and steals your data" [[1]](#ref-1).

## The Evolution from Specialized to General Agents

Willison suggests that "Claude Code is a 'general agent' disguised as a developer tool" [[1]](#ref-1). This observation points to a trend in context orchestration: tools initially designed for specific domains (like coding) are revealing broader capabilities for general knowledge work.

The naming choices in this space also matter. Willison suggests OpenAI may regret using the name "ChatGPT Agent" for their browser automation tool [[1]](#ref-1), implying strategic considerations in how these context orchestration tools are positioned and understood by users.

## Your Context Orchestration Stack

Based on this week's developments, leaders should evaluate:

1. **Agent Selection**: Consider whether specialized agents (like Claude Code) or general agents (like Cowork) better serve your context orchestration needs
2. **Security Boundaries**: Assess your comfort level with containerized file access versus the security risks of prompt injection
3. **Workflow Integration**: Evaluate how agent systems can combine file access, web search, and analysis in single workflows
4. **User Training**: Determine whether your team can effectively monitor for security issues in agent interactions

The shift from Claude Code to Cowork demonstrates that context orchestration tools are rapidly evolving from specialized to general-purpose systems. The challenge for leaders isn't just adopting these tools—it's understanding the tradeoffs between access, security, and usability in their context orchestration strategies.

## Sources

<a id="ref-1"></a>[1] [Willison, S. (2026, January 12). First impressions of Claude Cowork, Anthropic's general agent](https://simonwillison.net/2026/Jan/12/claude-cowork/#atom-everything)