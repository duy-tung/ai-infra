# Phase 15 — Autonomous Systems (chọn lọc)

Chỉ học các mục dưới — phục vụ Sprint 3 (production discipline).

## Lessons cần capture (chỉ phần này)

- [ ] Permission model
- [ ] Rollback
- [ ] Kill switch
- [ ] Cost governor
- [ ] Failure modes

## Câu hỏi định hướng

- Permission model: ask / auto / readonly / policy-as-code — ánh xạ tới mức rủi ro hành động.
- Rollback: agent thay đổi state thật thì rollback thế nào (git revert, DB compensating txn)?
- Kill switch: trigger gì (cost vượt, loop, error rate)? ai bấm (auto vs human)?
- Cost governor: hard cap per-run vs per-day; token budget vs USD budget.

## Notes

<!-- Dùng _template.md cho mỗi lesson. -->
