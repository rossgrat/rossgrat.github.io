---
date: 2026-04-14T11:10:53-05:00
draft: true
title: "Q: What do (TV) ER Doctors and Software Developers have in Common?"
tags:
  - none
---
A: Observability.

I've been watching The Pitt recently (excellent show, I highly recommend both Seasons 1 & 2), and I noticed a similarity between the ER Doctors on the show, and my day-to-day work as a software developer.

ER Doctors (and likely doctors in general, I don't really know I'm not a doctor) need observability to make decisions about how to treat a patient, just like Software Engineers need observability to make decisions about how to triage an incident or fix a bug. If either profession doesn't have the right or enough information, it's much harder for them to make the right decision (of course the stakes are certainly much higher for the Doctor.) 

What does observability look like for the ER Doctors on the Pitt? It looks like EKG/ECG, blood tests, drug screens, X-Rays, CT Scans, etc. 

What does observability look for a Backend Engineer working in the application layer? It looks like Grafana for dashboards, Mimir for metric counters, histograms, gauges, Loki for logs, Tempo for traces. It looks like OpenTelemetry for creating logs, metrics, and traces and Prometheus for consuming them. 

In Season X, Episode Y, Resident Doctor Samira Mohan treats a patient that appears to be suffering from the possible onset of Schizophrenia. SPOILER: It is later revealed that the patient has been applying skin care products with massive does of the heavy metal Mercury, which have been causing the problems.

Topic: What should we measure?

Topic: Building an intuition about what is right and wrong based on experience

You can generalize the importance of observability across even more fields than just the Software Developer and ER Doctor. Anyone who needs to make decisions about something, needs some measurable data on which to base those decisions. Otherwise, we're really just taking a shot in the dark.