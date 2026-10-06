# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên           | Mã sinh viên | Phần đóng góp        |
| ---------------- | ------------ | -------------------- |
| Nguyễn Công Vinh | 2A202602519  | Cá nhân, làm toàn bộ |

- Mô hình: `openai:gpt-6-luna`, nhiệt độ: `0`, recursion_limit: 160
- Phiên bản Deep Agents: `0.7.21`, hệ điều hành: Windows, chạy trực tiếp
- Số lần chạy tác vụ đã dùng / ngân sách: **18 / 0.73$**
- Commit của tag `freeze`: `5cce186ec78ad05313bcc3ec897e467538633a76`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Dự đoán subagents đạt điểm eval nhỉnh hơn baseline nhờ chia vai explorer/implementer/reviewer, nhưng không hiệu quả theo token. Trên learn, điểm hai điều kiện hiện bằng nhau ở cả ba tác vụ; subagents dùng trung bình 144.647 token so với 50.596 của baseline (2,86 lần), nên lợi ích cần đến từ kiểm tra độc lập chứ không chỉ thêm lượt gọi.
- H2 (skills-auto so với baseline): Dự đoán skills-auto cải thiện một phần điểm eval ở các quy ước quy trình đã thấy trong learn. Bằng chứng trước eval: code-learn tăng từ 6/10 lên 8/10 và cả ba lượt skills-auto đều đọc một skill; data-learn và logs-learn chưa tăng điểm. Do check quy ước mới có thể khác với feedback learn, dự đoán mức chuyển giao hạn chế, phù hợp cảnh báo quá khớp trong `guides/pseudocode/05_skill_quality.md`.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm learn cao hơn eval vì curator học từ feedback của learn, trong khi eval giữ quy ước mới chưa xuất hiện trong đầu vào. Skills-auto vẫn trượt các check quy ước ở data-learn và logs-learn, cho thấy việc đọc skill chưa bảo đảm chuyển giao sang quy tắc mới.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có các công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Công cụ `execute` cho phép chạy lệnh.
2. Subagent `general-purpose` được khuyên dùng cho các câu hỏi nghiên cứu phức tạp, tìm kiếm file/nội dung và thực thi chuỗi tác vụ nhiều bước. Subagent này là không trạng thái (stateless), chỉ nhìn thấy nội dung prompt (task) được truyền vào và trả về một báo cáo cuối cùng duy nhất, không nhìn thấy toàn bộ hội thoại/ngữ cảnh của tác tử chính.
3. Câu hướng dẫn từ `task`: "The agent's report is not shown to the user; relay a summary yourself."
   Câu hướng dẫn từ `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ     | Check thất bại        | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết)                           |
| ---------- | --------------------- | -------------- | ---------------------------------------------------------------------- |
| code-learn | tests_not_modified    | A              | Check báo các tệp test gốc đã bị sửa, trái yêu cầu rõ trong đề.        |
| code-learn | rule_type_hints       | E              | `RULE: every public function ... has type annotations...`              |
| code-learn | rule_regression_tests | E              | `RULE: add tests/test_regressions.py ... (at least 3)`                 |
| code-learn | rule_changelog        | E              | `RULE: record each fix in CHANGELOG.md ... (at least 3 bullets)`       |
| data-learn | rule_money_in_cents   | E              | `RULE: money values in answer.json are integer cents`                  |
| data-learn | rule_meta_block       | E              | Thiếu metadata `source`, `rows_in`, `rows_used` theo phản hồi của bot. |
| data-learn | rule_clean_csv        | E              | Thiếu `clean.csv` đúng schema và quy tắc chuẩn hóa.                    |
| logs-learn | rule_service_names    | E              | `RULE: service names ... lower-case with '-' replaced by '_'`          |
| logs-learn | rule_sorted_errors    | E              | `RULE: errors is sorted by service, then by timestamp_utc`             |
| logs-learn | rule_schema_header    | E              | `RULE: the top-level object has "schema_version": 2 ...`               |

Nhận xét: 9/10 check thất bại thuộc nhóm E; một check còn lại là A do vi phạm lệnh không sửa test. Skill quy trình có thể nhắc kiểm tra quy ước trước khi kết thúc, nhưng vẫn phải đối chiếu chính xác output với từng yêu cầu.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` chỉ đọc và báo cáo bối cảnh; `implementer` sửa/chạy kiểm tra; `reviewer` rà độc lập. Phân vai tách việc tìm hiểu, thực hiện và kiểm tra.
- `subagent_calls`: code-learn 2 (implementer, reviewer), data-learn 1 (explorer), logs-learn 1 (implementer). Tất cả lượt đều có giao việc; không có trường hợp 0.
- Giao việc nêu đường dẫn và ràng buộc chính: code nêu không sửa test gốc và conventions; data yêu cầu đọc README/CSV, nêu quy tắc và số liệu; logs liệt kê bộ lọc severity, UTC, traceback, repeat count và schema. Code có lượt reviewer riêng; trace chỉ ghi luồng chính và báo cáo cuối, không chứa diễn biến nội bộ.
- Token/thời gian trung bình trên ba tác vụ: baseline 50.596 token và 52,0 giây; subagents 144.647 token và 129,3 giây. Subagents tốn 2,86 lần token và 2,49 lần thời gian; điểm learn không đổi (6/10, 5/8, 6/9 ở cả hai điều kiện).

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy 1 lần, sinh 3 skill hợp lệ; chưa xóa skill nào.

| Skill                         | Tổng quát hay riêng cho tác vụ học?                                     | Đúng hay sai (nêu chỗ sai nếu có)                                                                                                                                                                              | Độ dài, `description` và `skills_read` ở Phần 3.4                       |
| ----------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| python-regression-maintenance | Quy trình chung cho sửa package Python; không gắn tên file/hàm của task | Các bước phù hợp feedback về type hints, regression tests và changelog. Chưa đủ để bảo đảm tuân thủ lệnh giữ nguyên test gốc trong lần chạy; check `tests_not_modified` vẫn trượt.                             | 10 dòng; description nêu tình huống kích hoạt; code-learn đọc 1 skill.  |
| structured-log-triage         | Quy trình chung cho chuẩn hóa log và tổng hợp lỗi                       | Hướng dẫn đúng về continuation/traceback, tên service, lọc severity, sắp xếp và schema; không chứa đáp án cụ thể. Các check quy ước của logs-learn vẫn trượt dù skill được đọc.                                | 11 dòng; description nêu đúng tác vụ log; logs-learn đọc 1 skill.       |
| tabular-data-normalization    | Quy trình chung cho bảng dữ liệu bẩn                                    | Hướng dẫn đúng về khóa trùng, missing values, timezone, đơn vị tiền, metadata và kiểm tra output; không chứa dữ liệu/đáp án riêng của sales.csv. Các check quy ước của data-learn vẫn trượt dù skill được đọc. | 12 dòng; description nêu đúng nhóm tác vụ bảng; data-learn đọc 1 skill. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Bảng so sánh (`report/table.md`):
| Task | baseline | subagents | skills-auto | skills-auto2 |
|---|---|---|---|---|
| code-learn | 6/10 | 6/10 | 8/10 | 6/10 |
| data-learn | 5/8 | 5/8 | 3/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 3/9 | 1/9 |
| code-eval | 6/11 | 6/11 | 6/11 | 6/11 |
| data-eval | 5/9 | 5/9 | 5/9 | 5/9 |
| logs-eval | 0/10 | 6/10 | 6/10 | 0/10 |
| **Mean score - learning tasks** | 0.63 | 0.63 | 0.50 | 0.45 |
| **Mean score - evaluation tasks** | 0.37 | 0.57 | 0.57 | 0.37 |
| **Mean tokens per run** | 53,872 | 160,916 | 134,269 | 98,283 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 | 6/6 |

Thống kê `check_breakdown.py`:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     11/18         0/12          57,149      0/3
baseline      learn    17/18         0/9           50,596      0/3
subagents     eval     17/18         0/12         177,185      0/3
subagents     learn    17/18         0/9          144,647      0/3
skills-auto   eval     16/18         1/12         116,382      3/3
skills-auto   learn    12/18         2/9          152,155      3/3
skills-auto2  eval     11/18         0/12         107,414      3/3
skills-auto2  learn    12/18         0/9           89,153      3/3
```

Không có lần chạy nào bị `skills_modified = true` sau khi đóng băng.

## 8. Phân tích

1. So với `baseline`, không có điều kiện nào cải thiện điểm trung bình trên tác vụ học (0.63 -> 0.50 đối với skills-auto). Trên tác vụ **đánh giá**, cả `subagents` và `skills-auto` đều cải thiện điểm trung bình từ 0.37 lên 0.57 (chủ yếu là nhờ tác vụ logs-eval tăng từ 0/10 lên 6/10). Việc điểm học giảm nhưng điểm đánh giá tăng hoặc giữ nguyên cho thấy sự nhiễu đáng kể của mô hình hoặc tác dụng phụ của skills (gây nhầm lẫn trong một số task học nhưng lại vô tình giúp ích trong task đánh giá).
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`): Skill do curator sinh ra đã giúp tăng điểm check quy ước trên tác vụ học từ 0/9 lên 2/9. Tuy nhiên, trên tác vụ đánh giá (eval), check quy ước chỉ đạt 1/12. Check quy ước mới của tác vụ đánh giá phần lớn không được skill giúp, vì skill sinh ra từ tập học (learn) đã bám vào các quy ước cũ, không thể khái quát hóa hoàn toàn cho những quy ước chưa từng xuất hiện.
3. Dựa vào `skills_read = 3/3` ở các lượt học: Ở `code-learn`, skill đã giúp pass thêm được 2 check quy ước (điểm tăng từ 6/10 lên 8/10), do skill cung cấp hướng dẫn nhắc nhở về type hint và changelog. Ngược lại, dù đã đọc skill, điểm ở `data-learn` lại bị sụt giảm từ 5/8 xuống 3/8; điều này xảy ra vì skill tập trung quá nhiều vào quy tắc cũ khiến tác tử quên mất hoặc thực hiện sai các chỉ thị cốt lõi của tác vụ (ví dụ: bị nhiễu thông tin định dạng).
4. Chi phí token: `baseline` tốn khoảng 50k - 57k token mỗi lượt. `subagents` tốn nhiều nhất (144k - 177k, gấp ~3 lần baseline) do phải gọi nhiều subagent. `skills-auto` tốn 116k - 152k. Nếu xét trên hiệu quả điểm số/token, `baseline` vẫn là tốt nhất. Tuy nhiên đa tác tử (`subagents`) đã khắc phục được lỗi kỹ thuật trên `logs-eval` (0/10 -> 6/10) nên nếu ưu tiên độ chính xác trên task khó, mức chi phí này có thể chấp nhận được.
5. Quá khớp (Overfitting): Các skill sinh ra có dấu hiệu quá khớp nhẹ vào các yêu cầu quy ước cụ thể của tập học. Nhóm đã phòng tránh rò rỉ dữ liệu bằng cách chỉ cung cấp `detail` (quy tắc bị vi phạm) mà không cung cấp dữ liệu eval hoặc đáp án cụ thể vào prompt của curator.
6. Nhiễu: Điểm ở một số tác vụ học dao động dù dùng cùng một bộ skill, cho thấy mô hình có tính ngẫu nhiên (nhiễu). Độ tin cậy của chênh lệch điểm 1-2 điểm trong bảng mục 7 là không cao và cần chạy nhiều lần để lấy trung bình.

## 9. Hạn chế và tính hợp lệ

1. Tập dữ liệu quá nhỏ: Mỗi điều kiện chỉ được chạy trên 3 tác vụ học và 3 tác vụ đánh giá. Điều này khiến điểm số dễ bị thay đổi do nhiễu (1 check pass/fail làm lệch % rất lớn).
2. Mỗi cấu hình chỉ chạy 1 lần: Các LLM (như gpt-6-luna) có sự dao động trong đầu ra, nên một lần chạy chưa phản ánh chính xác năng lực thực sự (cần chạy 3-5 lần để lấy phương sai).
3. Các quy ước (house rules) được thiết kế sẵn và cứng nhắc: Điều này khiến các kỹ năng do AI sinh ra (skill) khó có thể khái quát hóa (generalize) cho một tập luật hoàn toàn mới ở tập đánh giá.

## 10. Kết luận

Thử nghiệm cho thấy kỹ thuật đa tác tử (`subagents`) và tự tiến hóa (`skills-auto`) có khả năng giúp vượt qua những điểm tắc nghẽn khó trên tác vụ lạ (tăng eval từ 0.37 lên 0.57), chủ yếu bằng cách khắc phục các lỗi kỹ thuật và thêm sự nhắc nhở. Tuy nhiên, khả năng khái quát hóa các luật lệ mới của `skills-auto` vẫn rất thấp (chỉ 1/12 house rules đạt trên eval) và chi phí token tăng gấp 2-3 lần. Đề xuất cải tiến tiếp theo là áp dụng vòng tiến hóa thứ hai (hợp nhất skill) hoặc cho phép tác tử tự sinh skill ngay trong thời điểm chạy (hot-path).

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  1. `pytest tests/test_01_provided.py`
  2. `python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').content)"`
  3. `python scripts/tour.py`
  4. `pytest tests/test_02_agent.py -k subagents`
  5. `pytest tests/test_02_agent.py`
  6. `pytest tests/test_03_runner.py`
  7. `python -m lab.runner --condition baseline --tasks data-learn`
  8. `python -m lab.runner --condition baseline --tasks code-learn logs-learn`
  9. `python -m lab.runner --condition subagents --tasks learn`
  10. `pytest tests/test_04_curator.py`
  11. `python -m lab.curator`
  12. `python -m lab.runner --condition skills-auto --tasks learn`
  13. `git add -A && git commit -m "hypotheses"`
  14. `git add -A && git commit --allow-empty -m "freeze skills" && git tag freeze`
  15. `python -m lab.runner --condition baseline --tasks eval`
  16. `python -m lab.runner --condition subagents --tasks eval`
  17. `python -m lab.runner --condition skills-auto --tasks all`
  18. `python scripts/verify_freeze.py`
  19. `python -m lab.compare > report/table.md`
  20. `python scripts/check_breakdown.py`
- Thử thách mở rộng (nếu có): **Hướng 6b - Vòng tiến hóa thứ hai**.
  - Đã chạy hàm `curate_skills` lần 2 lấy input là các lỗi từ các lần chạy `learn` của vòng 1 (`skills-auto`) và sinh bộ skill mới tại `skills/auto2`.
  - Kết quả: Các skill mới có khuynh hướng trở nên cồng kềnh, lan man hoặc "học vẹt" (quá khớp nặng hơn). Cụ thể, điểm số đánh giá (eval) của `skills-auto2` giảm mạnh từ 0.57 (của skills-auto) xuống bằng mức baseline là 0.37. Tác vụ `logs-eval` lại rớt về 0/10 và bị kẹt lặp lại rất lâu (mất 18 phút). Số luật (house rules) áp dụng thành công trên tập đánh giá giảm từ 1 xuống 0.
  - Nhận xét: Tiến hóa liên tục qua nhiều thế hệ mà không có sự chọn lọc chặt chẽ hoặc phản hồi chất lượng (feedback vòng lặp) sẽ dẫn đến "skill bloat" (phình to) và suy thoái năng lực (degradation). Việc chạy thử cho thấy giới hạn của curator khi dựa trên output sai lệch từ trước.
- Ghi chú khác:
