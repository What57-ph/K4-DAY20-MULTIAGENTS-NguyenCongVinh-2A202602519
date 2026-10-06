# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| | | |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`:
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker:
- Số lần chạy tác vụ đã dùng / ngân sách:
- Commit của tag `freeze`:

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Dự đoán subagents đạt điểm eval nhỉnh hơn baseline nhờ chia vai explorer/implementer/reviewer, nhưng không hiệu quả theo token. Trên learn, điểm hai điều kiện hiện bằng nhau ở cả ba tác vụ; subagents dùng trung bình 144.647 token so với 50.596 của baseline (2,86 lần), nên lợi ích cần đến từ kiểm tra độc lập chứ không chỉ thêm lượt gọi.
- H2 (skills-auto so với baseline): Dự đoán skills-auto cải thiện một phần điểm eval ở các quy ước quy trình đã thấy trong learn. Bằng chứng trước eval: code-learn tăng từ 6/10 lên 8/10 và cả ba lượt skills-auto đều đọc một skill; data-learn và logs-learn chưa tăng điểm. Do check quy ước mới có thể khác với feedback learn, dự đoán mức chuyển giao hạn chế, phù hợp cảnh báo quá khớp trong `guides/pseudocode/05_skill_quality.md`.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm learn cao hơn eval vì curator học từ feedback của learn, trong khi eval giữ quy ước mới chưa xuất hiện trong đầu vào. Skills-auto vẫn trượt các check quy ước ở data-learn và logs-learn, cho thấy việc đọc skill chưa bảo đảm chuyển giao sang quy tắc mới.

## 3. Làm quen Deep Agents (Phần 0.3)

1.
2.
3.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | tests_not_modified | A | Check báo các tệp test gốc đã bị sửa, trái yêu cầu rõ trong đề. |
| code-learn | rule_type_hints | E | `RULE: every public function ... has type annotations...` |
| code-learn | rule_regression_tests | E | `RULE: add tests/test_regressions.py ... (at least 3)` |
| code-learn | rule_changelog | E | `RULE: record each fix in CHANGELOG.md ... (at least 3 bullets)` |
| data-learn | rule_money_in_cents | E | `RULE: money values in answer.json are integer cents` |
| data-learn | rule_meta_block | E | Thiếu metadata `source`, `rows_in`, `rows_used` theo phản hồi của bot. |
| data-learn | rule_clean_csv | E | Thiếu `clean.csv` đúng schema và quy tắc chuẩn hóa. |
| logs-learn | rule_service_names | E | `RULE: service names ... lower-case with '-' replaced by '_'` |
| logs-learn | rule_sorted_errors | E | `RULE: errors is sorted by service, then by timestamp_utc` |
| logs-learn | rule_schema_header | E | `RULE: the top-level object has "schema_version": 2 ...` |

Nhận xét: 9/10 check thất bại thuộc nhóm E; một check còn lại là A do vi phạm lệnh không sửa test. Skill quy trình có thể nhắc kiểm tra quy ước trước khi kết thúc, nhưng vẫn phải đối chiếu chính xác output với từng yêu cầu.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` chỉ đọc và báo cáo bối cảnh; `implementer` sửa/chạy kiểm tra; `reviewer` rà độc lập. Phân vai tách việc tìm hiểu, thực hiện và kiểm tra.
- `subagent_calls`: code-learn 2 (implementer, reviewer), data-learn 1 (explorer), logs-learn 1 (implementer). Tất cả lượt đều có giao việc; không có trường hợp 0.
- Giao việc nêu đường dẫn và ràng buộc chính: code nêu không sửa test gốc và conventions; data yêu cầu đọc README/CSV, nêu quy tắc và số liệu; logs liệt kê bộ lọc severity, UTC, traceback, repeat count và schema. Code có lượt reviewer riêng; trace chỉ ghi luồng chính và báo cáo cuối, không chứa diễn biến nội bộ.
- Token/thời gian trung bình trên ba tác vụ: baseline 50.596 token và 52,0 giây; subagents 144.647 token và 129,3 giây. Subagents tốn 2,86 lần token và 2,49 lần thời gian; điểm learn không đổi (6/10, 5/8, 6/9 ở cả hai điều kiện).

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy 1 lần, sinh 3 skill hợp lệ; chưa xóa skill nào.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| python-regression-maintenance | Quy trình chung cho sửa package Python; không gắn tên file/hàm của task | Các bước phù hợp feedback về type hints, regression tests và changelog. Chưa đủ để bảo đảm tuân thủ lệnh giữ nguyên test gốc trong lần chạy; check `tests_not_modified` vẫn trượt. | 10 dòng; description nêu tình huống kích hoạt; code-learn đọc 1 skill. |
| structured-log-triage | Quy trình chung cho chuẩn hóa log và tổng hợp lỗi | Hướng dẫn đúng về continuation/traceback, tên service, lọc severity, sắp xếp và schema; không chứa đáp án cụ thể. Các check quy ước của logs-learn vẫn trượt dù skill được đọc. | 11 dòng; description nêu đúng tác vụ log; logs-learn đọc 1 skill. |
| tabular-data-normalization | Quy trình chung cho bảng dữ liệu bẩn | Hướng dẫn đúng về khóa trùng, missing values, timezone, đơn vị tiền, metadata và kiểm tra output; không chứa dữ liệu/đáp án riêng của sales.csv. Các check quy ước của data-learn vẫn trượt dù skill được đọc. | 12 dòng; description nêu đúng nhóm tác vụ bảng; data-learn đọc 1 skill. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
