# Operations & Support Dashboard

## Audience
Operations manager, support leads, QA lead

## Purpose
Track support performance, identify backlog risk, and monitor SLA compliance.

## Core KPIs
- Tickets Created
- Tickets Resolved
- Average Resolution Time (hours)
- SLA Compliance (%)
- Backlog Volume

## Recommended Visuals
- KPI cards (volume, SLA, resolution time)
- Daily/weekly ticket trend line
- Ticket status funnel (open -> in progress -> resolved)
- Agent leaderboard (resolved tickets, avg handling time)
- Category heatmap (issue type x priority)

## Filters/Slicers
- Date
- Priority
- Issue Category
- Agent

## Data Tables Needed
- `fact_tickets`
- `fact_sla_events`
- `dim_agent`
- `dim_priority`
- `dim_date`

## Build Checklist
- [ ] Create ticket lifecycle metrics
- [ ] Build SLA breach and compliance measures
- [ ] Add drill-through page per agent
- [ ] Add conditional formatting for SLA breaches
- [ ] Publish screenshot to `screenshots/`

