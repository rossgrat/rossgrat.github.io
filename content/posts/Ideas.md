---
date: 2026-09-29T11:17:28-05:00
draft: true
title: ""
tags:
  - none
---
Ideas
- AI workflow and rules of the road. What can I do and not do well? How to protect learning and career development
- frontpair, getting my Audient id14 to send audio to Zoom on channels 1 & 2


**Transparency**
I'm going to start out this post with the qualifier that these are all untested and un-researched ideas. My career experience thus far is limited, and I haven't, until recently, really concerned myself with thoughts on interpersonal interactions between cross-functional teammates, or organizational culture.

If I had to guess, I'd say the ideas that I'm going to present here bridge disciplines like organizational behavior, organizational sociology, business anthropology, and maybe even some social psychology. I know absolutely nothing about any of these areas of study, so you can value what follows against this lack of experience.

I feel these things in my gut, and I feel the need to express them publicly, and as record for my future self. I feel that by laying them out here (and generally being too lazy to spend the time deep diving into definitive studies), I can prove or disprove my gut feelings by framing my future workplace interactions through this lense.



The ideas that I have are about transparency. I believe that teams and organizations will


Publishing things in a public space, such as public slack channels, public documents, 







- Public record and accountability
	- More eyes means earlier in design processes means better decisions? (or do things get bogged down in meetings and disagreements?)
- Preventing cliques
	- Transparency from leadership leads to trust in decisions?
	- Trusting teams and non-leads to interpret in-progress information
- Cite that study about transparency maybe being problematic when there are no private spaces


# Job Board Post Followups

# Appendix (Move these to separate posts)
### A Transactional Outbox

Before we discuss each stage of pipeline, I want to briefly talk about the system that the pipeline is build on, which is called a transactional outbox. The idea here is that we're using Postgres as a message queue, because we're also storing data in that same postgres database, and by encompassing our job processing and data storage in the same database transaction, we circumvent the dual write / distributed transaction problem TODO: LINK I'm not going to describe this problem in detail here, but I've attached an article if you're not familiar. (Or I highly recommend Designing Data Intensive Applications, a.k.a the backend bible.)


Why use an outbox pattern? What makes an message queue and specifically an outbox well suited to this task?
- LLM calls take time
- Resilience / durability
- Rate limiting
- First an aside, the dual-write problem / distributed transactions, how an outbox fixes this problem

### Go Channels in Fetchers

One fetcher I think is particularly cool is the Workday fetcher. Workday is a JSON API fetcher, but it is of the List + Get API flavor. There is currently only one company I'm fetching that uses workaday,
TODO


### LLM Evals

TODO

# So how does it run?

## Self-hosting on old hardware

As I've said multiple times in this post, I didn't want this to cost anything. I couldn't avoid paying for LLM credits (I looked at local, open-weight LLM models. TLDR; I don't have the compute to run one of those), but I could leverage an old laptop I have to get away with not paying AWS for EC2 or Lightsail.


TODO: Docker container network. 

TODO: Tailscale vs Cloudflare tunnels

TODO: Custom domain

TODO: Pic of laptop? Could be fun


## Observability

Systems are hard to debug if you can't see into them. My observability stack is hosted on the same machine as my job board.

The primary thing to observe is the pipeline itself. Processing thousands of jobs comes with risks. I'm not overly worried about web traffic since there should be exactly one visitor to my site (me), and 9 times out of 10 I'm checking my job board from the same local network that my host is on.

TODO: Pic of metrics / Grafana dashboard?




Goals of this post:
- I'm technical, I can build things
- I'm a senior-level engineer, I think about big problems, tradeoffs, product, cost when I build things


Why did I build this?
Diagram of the pipeline workflow, talk about the outbox pattern
Talk about cost tradeoffs between anthropic models
Talk about scrapers?
Talk about targeted spend (mentioned that some stages of the pipeline could be reworked to take advantage of decision models like Jev)
Talk about observability, screenshot of Grafana here is good
Talk about self-hosting on an old laptop and serving to the internet using jobs.grattafiori.dev
Mention that the build can take advantage of those tests, I forget what they're called, if need be
Mention shortcomings, next steps
Callout that FE is agentic coded, and I didn't read any of it, outside of specifying the technology 

Follow-up posts
- Compare and contrast tailscale and cloudflare tunnels
- Maybe a small aside about the runner pattern that I really like, and option functions
- 
