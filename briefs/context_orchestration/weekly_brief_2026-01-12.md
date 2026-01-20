# Context Orchestration Through Agent Evolution: From Code to Cowork

This week brought a significant development in context orchestration tools with Anthropic's release of Claude Cowork [[1]](#ref-1). Described as "Claude Code for the rest of your work," this new agent represents an evolution in how leaders can orchestrate context across different types of tasks [[1]](#ref-1).

## The Agent as Context Orchestrator

Claude Cowork, now available to Max subscribers on $100 or $200 per month plans, extends the context orchestration capabilities previously limited to coding tasks [[1]](#ref-1). The tool operates through a new tab in the Claude desktop app, sitting alongside the existing Chat and Code tabs [[1]](#ref-1).

What makes this development notable for context orchestration is how it handles file access and system interactions. Files appear to be mounted into a containerized environment, as evidenced by file paths like "/sessions/zealous-bold-ramanujan/mnt/blog-drafts" [[1]](#ref-1). This containerization represents a specific approach to context management—giving the AI access to your files while maintaining security boundaries.

The interface looks very similar to the desktop interface for regular Claude Code, suggesting that Anthropic views context orchestration patterns as transferable across different work domains [[1]](#ref-1). This consistency matters for leaders learning to orchestrate context: the meta-skills developed in one domain can transfer to others.

## Practical Context Orchestration in Action

Simon Willison tested Cowork with a complex context orchestration task: "Look at my drafts that were started within the last three months and then check that I didn't publish them on simonwillison.net using a search against content on that site and then suggest the ones that are most close to being ready" [[1]](#ref-1).

This single request demonstrates multiple layers of context orchestration:
- **File system context**: Cowork executed system commands to find relevant files
- **Temporal context**: Filtering for files modified within 90 days
- **Web context**: Running 44 individual searches against site:simonwillison.net to verify publication status [[1]](#ref-1)
- **Synthesis**: Combining all contexts to provide actionable recommendations

The agent handled this by running commands like:
```
find /sessions/zealous-bold-ramanujan/mnt/blog-drafts -type f \( -name "*.md" -o -name "*.txt" -o -name "*.html" \) -mtime -90 -exec ls -la {} \;
```

This shows how modern agents orchestrate context by combining file system access, web search, and analytical capabilities [[1]](#ref-1).

## Security as Context Boundary Management

Anthropic's approach to security reveals important tensions in context orchestration. The company states that Cowork can only access files you grant it access to, and it runs in a filesystem sandbox by default [[1]](#ref-1). However, they also warn about the risk of prompt injections in their announcement [[1]](#ref-1).

The summarization applied by WebFetch in Claude Code and Cowork serves partly as a prompt injection protection layer, according to a tweet from Claude Code creator Boris Cherny referenced by Willison [[1]](#ref-1). This highlights a key principle: context orchestration isn't just about what to include—it's also about what to filter out or transform for safety.

## Tensions & Tradeoffs

The release surfaces a critical tension in context orchestration: security responsibility. Willison notes that Anthropic asks users to monitor for prompt injections, but questions whether regular non-programmer users can effectively "watch out for 'suspicious actions that may indicate prompt injection'" [[1]](#ref-1).

This represents a fundamental tradeoff in context orchestration:
- **More context access** = More powerful capabilities
- **More context access** = Greater security risks
- **Security measures** = Additional complexity for users

Anthropic acknowledges they cannot provide guarantees that no future attack will sneak through their defenses and steal user data [[1]](#ref-1). This honest assessment highlights that context orchestration involves accepting and managing risks, not eliminating them entirely.

## Your Context Orchestration Stack

Based on this week's developments, leaders should evaluate:

1. **Agent selection**: Consider whether your use cases benefit from general agents (like Cowork) versus specialized ones (like Claude Code)
2. **Security boundaries**: Define what context different tools should access—Cowork's containerized approach offers one model
3. **Verification workflows**: Cowork's ability to cross-reference file content against web searches demonstrates the value of multi-source verification
4. **Risk tolerance**: Assess your organization's ability to monitor for security issues versus the productivity gains from broader context access

The evolution from Claude Code to Cowork suggests that context orchestration patterns developed for technical tasks can extend to general knowledge work. Leaders who master these patterns in one domain can apply them broadly across their organizations.

## Sources

<a id="ref-1"></a>[1] [Willison, S. (2026, January 12). First impressions of Claude Cowork, Anthropic's general agent](https://simonwillison.net/2026/Jan/12/claude-cowork/#atom-everything)