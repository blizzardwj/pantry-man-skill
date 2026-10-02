# 反馈运行规则重构验证 — 2026-09-28

> 历史验证记录。2026-09-30 的 [DEC-021](../DECISIONS.md#dec-021) 已移除新操作的 `landings[]` 写前／恢复流程，并收窄反馈准入；下文描述的是 2026-09-28 的实现和检查，不是当前运行指令。当前行为见 [SKILL.md](../SKILL.md) 与 [feedback_flow.md](../references/feedback_flow.md)。

范围：[IDEA-018](../IDEAS.md#idea-018)，落实 [DEC-017](../DECISIONS.md#dec-017)、[DEC-018](../DECISIONS.md#dec-018)，字段选择见 [DEC-019](../DECISIONS.md#dec-019)。撰写时实现位于工作区，后提交为 [3e6d1bd](https://github.com/blizzardwj/pantry-man-skill/commit/3e6d1bd)；设计提交基线为 `3a1628b`。本报告不表示已验证长期用户效果。

## 运行契约变化

- [SKILL.md](../SKILL.md)：采购／搭配前跨日 Review；新增、移除、标记已购、记录购买共用反馈更新步骤；确认草稿与已确认清单分开。
- [feedback_flow.md](../references/feedback_flow.md)：逐食材耗尽与补货、普通删清单、不回答、当次补问、独立落点和中断核对。
- [schema.md](../references/schema.md)：feedback v2、itemKey、stockEvent／effectiveAt、landings[]、shopping.confirmation，以及未知数量／购买细节的表示。
- README 更新用户可见的反馈行为；开发 fixtures／字段 probe 改用 v2，原历史购买用例补上明确购买日期，避免测试要求编造日期。运行仍为纯指令和 schema，没有新增运行脚本。

## 已执行检查

| 检查 | 结果与范围 |
|------|------------|
| `python3 dev/validate_static.py` | PASS，0 FAIL、1 WARN；frontmatter、4 个 reference 文件、无新增 agent 专属路径、74 个 probe 字段都有 schema 说明。WARN 为原有 4 处 cron add 占位，与本次无关 |
| `git diff --check` | PASS，无空白错误 |
| 文档链接、显式锚点及 JSON 检查 | PASS：303 个本地链接（完成记录补链前）、显式锚点唯一性与目标、8 个 JSON 示例、21 个开发 JSON；v2 种子及 probe 的 ID／supersededBy／mergedInto 关联检查通过 |
| skill-creator 的 `quick_validate.py` | 未能启动：当前 Python 缺少 PyYAML（ModuleNotFoundError: yaml）；未将此项记为通过。仓库自带静态检查已覆盖 frontmatter 与引用路径 |

## 作者执行的场景验证

这里的执行者是本次修改规则的 agent。使用临时目录，按规则实际写入样例数据，然后由现有 runner 或独立断言检查结果；不是独立 agent 盲测，也不是一个可以代替 skill 的代码实现。没有读取或修改真实 pantry 用户数据。

| 场景／输入 | 执行及观察结果 |
|-------------|----------------|
| “苹果和黄瓜都吃完了” | `python3 dev/run_golden.py prepare stock_change_deplete` 后执行；`assert stock_change_deplete --home /tmp/pantry_golden_zdmwplle` PASS（5 个断言）。分别产生 active 的苹果／黄瓜 depleted 记录，库存两项移除，鸡蛋保留；库存落点 applied=true |
| 补记 2026-08-13 牛奶15元、面包12元，共27元，明确不代表当前库存 | `prepare purchase_history` 后执行；`assert purchase_history --home /tmp/pantry_golden_0riflloi` PASS（3 个断言）。记录写入 2026-08，recordCount=1、totalSpent=27；附加断言当前库存仍空 |
| 在耗尽场景之后加购苹果，再说“删掉，这次不买”；模拟加购已写、applied 未回写 | 在第一个临时目录继续执行：苹果购物项删除，两种耗尽仍 active；旧加购落点 supersededBy 指向删除事件。检查通过，旧 pending 不再有重试资格 |
| 后来明确只买回苹果2个、6元，黄瓜未买；模拟旧耗尽与新购买写入未回执 | 苹果旧记录 decayed，黄瓜仍 active；旧删除落点 superseded。库存与历史已经等于购买落点 after，恢复只补 applied；字节比较验证库存／历史未再次写入，苹果数量仍2、购买记录仍1。检查通过 |
| 确认建议时删菠菜、芹菜、生菜，剩余鸡蛋确认，然后不回答原因 | `/tmp/pantry_confirmation_review_3dpg7zax`：先删改，再将鸡蛋写正式清单，confirmation=confirmed；发送一次问题前保存 clarificationAskedAt。重新读取后标记仍在；未回答时没有新增反馈、库存、购买或画像，JSON 保持不变。检查通过；是否提问的判断由作者执行，不是独立模型行为评测 |

以上临时目录仅是本轮执行证据位置，不作为仓库依赖；临时数据可能被环境清理。两个 golden 用例定义保留在 dev/golden_cases，可交给独立执行者再次运行。

## 规则走查与剩余限制

已逐项走查：跨日无新反馈仍读有效耗尽；候选不由 applied 控制且不是全部必推；已有库存／清单避免重复需求；只确认清单不 decay；部分确认仅写获准项；“已有”不造购买记录；只买一项逐项 decay；新的耗尽不合并进旧周期；本次不想买／沉默不更新长期偏好；提问不是用户反馈；删2项、改数量或替换不触发删3项规则；新计划不追问旧原因；明确长期不推荐正常更新偏好。

这些走查支持文档内部的一致性，不是各场景均已由独立 agent 执行的证明。未运行完整 golden suite、跨 agent 行为回归或长期饮食计划效果评估。先保存提问标记再发问选择的是“最多一次尝试”，不能保证中断时消息必达；before/after 不匹配且证据不足的更新仍需核对，不强行回放。未在真实用户文件上执行旧反馈归档或清理。
