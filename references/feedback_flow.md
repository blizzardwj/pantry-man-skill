# Feedback Flow — 反馈捕获、数据更新与复用

本文件落实 [SKILL.md](../SKILL.md) 的反馈规则；字段与空文件结构见 [schema.md](schema.md)。以下数据路径均相对于 `[AGENT_HOME]/pantry/data/`。用户个性化规则只写 `profile.json`，不改技能文件。

## 入口与职责

| 入口 | 读取与执行 |
|------|------------|
| 对话中的新事实、纠正（Capture） | 读 feedback 及受影响的数据文件，立即执行已明确的操作，记录事实与更新结果 |
| 捕获后的同日整理（Threshold） | 达到原有阈值时整理 feedback；不等待后台或日界进程 |
| 生成采购计划／每日搭配前（Review） | 每次读 feedback，核对未完成操作与当前有效事实，再读最新业务数据生成计划；不限当天 |
| 确认／修改采购建议 | 读写 shopping.confirmation，先落实删改，本次满足条件时补问一次 |
| 标记已购／记录购买／报告已有或补货 | 使用下方同一套事实更新步骤，逐食材更新 pantry、shopping、history 和 feedback |

**两个状态各管一件事。** `landings[].applied` 只表示该项数据更新已完成；记录的 `status` 表示事实是否仍有效。苹果吃完、库存已清除时，库存落点为 applied=true，耗尽事实仍为 active。是否建议再买由计划选择，不能从 applied 推断。普通不买、删清单、确认加购都不是补货。

## ① Capture：先确定用户说了什么

| 用户表达 | 记录与处理 |
|----------|------------|
| “苹果和黄瓜吃完了” | 两条 stock-change / stockEvent=depleted，通常 importance=3；分别更新两种库存 |
| “菠菜家里有了” | stock-change / available，通常 3；记录现有库存，不生成购买历史 |
| “菠菜已经买了” | stock-change / purchased，通常 3；按购买入口处理，缺少的信息不编造 |
| 新食材／新事实 | ingredient-fact；状态事实通常 3，只有长期习惯等才为 4 |
| “鲈鱼换成鲷鱼片” | 本次修改立即生效；如留反馈则 preference-correction / 2，不自动改长期偏好 |
| “以后不要推荐牛奶” | 明确的长期 preference-correction，按内容记 4 或 5，更新 profile 偏好 |
| 具体搭配反馈／流程建议 | pairing-feedback；按内容判断重要性，提议不等于已确认的规则 |
| “这次不买”／普通删除／未回答原因 | 执行已明确的本次操作，不推断库存、购买或长期偏好；未回答不是一条用户反馈 |

importance：5=画像／流程级，4=长期习惯，3=状态事实，2=一次性微调，1=噪音／待观察。它决定沉淀价值，不是执行用户指令的门槛。寒暄、系统自己提出的问题不记录为用户反馈。

1. 先读 `feedback.json`、相关 `pantry.json`／`shopping.json`／`profile.json` 和需要的月份购买历史。按照 schema 的 `itemKey` 关联同一食材；一条库存反馈只含一种食材，批量原话可保留在各条 source 中。
2. 区分当前事实与历史补述：`effectiveAt` 表示库存事实生效时间，`capturedAt` 是记录时间。“现在有了”以当前观察时间为准，不代表购买日期；历史买过不能证明现在仍有。先后不清的历史事实可记 effectiveAt=null，不据此覆盖当前库存。
3. 相同事件重试复用原反馈 ID、目标条目 ID 和原落点；新的“又吃完”若发生在补货之后，建立新事件，不能与上一次耗尽合并。仅名称相同不能证明同一购买事件。
4. 每个已获授权、信息充分的数据更新写入独立 `landings[]`，保存路径、条目 ID、更新前后值，再执行下节步骤。没有实际更新就用空数组；“以后可能要买”不能预先建立一个待写 shopping 的落点。
   普通加购、删除、确认也可记录实际操作（preference-correction / 2，仅指本次操作，不更新长期偏好），以保存授权与中断恢复依据；这不会修改先前的耗尽事实。记录中只写用户确实要求的操作，不填猜测的原因。
5. 不明确的食材、数量或历史时间，只保留已知信息；执行其余明确操作。仅当歧义会导致错误改动时针对它澄清，不把询问删除原因当作操作前提。

## ② 数据更新与中断恢复

`landings[]` 使用 schema 定义的 `target / path / itemId / before / after / applied`。目标可以是 pantry、shopping、profile 或一个 history 月文件；规则、模板、范例都是 profile 内的路径，没有单独的 rule 文件。每项保存**目标最终值**，不要保存“再加 2 个”这样的相对动作。

1. 将实际操作及 before/after 先写入 feedback，applied=false。`path` 指对象字段或条目数组；数组靠固定 itemId 定位，不能靠可能变化的下标。新条目的 ID 在这里确定。
2. 对每个落点先核对后续事实及当前目标：
   - 当前目标等于 after：操作已生效，补记 applied=true，不重复写入。
   - 等于 before 且未被后续事实取代：写入 after（after=null 表示删除），成功后记 applied=true。
   - 后续事实已取代这项操作：不重放旧值；保留原 applied，填 supersededBy=新反馈 ID。
   - 两边都不等、也无法确定先后：暂不覆盖，保留未完成状态，必要时说明具体冲突；不自动回放删除、加库存或加清单。
3. 更新每个实际写入文件的 meta.lastUpdated（history 无此字段）；history.stats 从现存记录重算，不累加重试次数。文件写入中断后从第 2 步核对，不重新产生 IDs。
4. 补货取代旧耗尽时，在写新库存前，先将对应旧记录置 decayed、将旧记录未完成且相冲突的落点标 supersededBy。旧落点若早已 applied=true，保留这个历史结果。新事实仍有 pending 落点时由 Review 继续核对。
5. 其他明确新操作也先取消与它冲突的旧 pending 落点，例如删清单取消该条目未完成的加购。只取消具体落点，不因此 decay 耗尽事实；购买事件的库存落点过时，也不取消它仍需写入的历史记录。开始新提案时，取消旧提案未完成的 confirmation 更新，防止恢复时覆盖新计划；新记录及 supersededBy 在同一次 feedback 写入中保存。

所有已授权但未完成且未 superseded 的落点都应核对，不因 importance 低而跳过；已完成或明确过时的操作不重放。日志的 active/decayed 与操作是否完成分别判断。

## ③ 事件处理：逐食材闭合

| 事件 | 更新及不变量 |
|------|--------------|
| 明确吃完某食材 | 记录 depleted，删除／清零陈述覆盖的 pantry 条目；没有条目时不造负库存，可用空 landings。若只吃完一份，其他同种库存仍保留，选品时继续核对。记录 active，不自动写 shopping |
| 只展示补货建议 | 不写购物条目，不改变耗尽记录 |
| 确认加入清单／直接要求加购 | 匹配 unchecked 的 itemKey，新增或更新 shopping，避免重复；不改库存，不 decay |
| 本次不买／删清单 | 删除指定建议或购物条目，不改库存、画像或耗尽记录；同轮不自动加回。新计划仍可按原有依据选择 |
| 当前已经有／明确补货 | 逐食材记录 available；更新当前 pantry，仅 decay 被它取代的旧耗尽事实。不从“已有”生成购买历史，也不把已有但可能仍需增购的清单项擅自标为已购 |
| 当前已经买回／标记已购 | 记录 purchased，按下方购买步骤更新；仅对应食材旧耗尽事实 decayed |
| 历史买过 | 记录有依据的购买历史；不把旧购买当作今天补货，不使后来发生的耗尽失效 |
| 补货后再次吃完 | 新建 depleted 事件与实际落点，新一轮 active；不恢复旧记录或沿用旧事件的 applied |

**购买步骤（所有购买入口共用）：**

1. 确定本次实际买了哪些食材及能确认的数量、日期、价格。匹配 feedback 与 history 中是否已有同次购买，重试复用原事件；不能仅因食材相同就合并两次真实购买。
2. 当前买回：对每种食材更新 pantry。已知新增量可与可换算的已有量相加，但在落点中保存相加后的最终值；“已经有了”是现有量而非新增量，不累加。已有数量未知或新增量未知时不能算出精确总量，按 schema 记未知或保留分别可确认的批次，不把购物计划的数量当成实买数量。只让此前被覆盖的 depleted 记录 decayed；其余食材不动。
3. 明确买完某个待购条目时，将该条目 checked=true；只买一部分时扣减可确认的剩余需求，仍保留 unchecked。无法确认是否买足时保留待购，不凭买过同名食材就清掉全部需求。普通清单删除不进入购买步骤。
4. 购买日期已知时，用该日期的 `history/YYYY-MM.json`，每次购买用固定 record ID；多食材同次购买共用该记录，不生成重复账目。金额或数量未知按 schema 省略。日期未知时把已知购买信息保留在 feedback.content 中，暂不写月文件；以后用户提供日期时补同次购买落点，不再入库一次。无需为记全购买细节阻塞当前库存更新。
5. 检查该事件各落点结果与被取代的旧耗尽记录，简短报告实际完成的操作。日期、时间先后或关联不清的部分保留未知，不能以捕获时间改写历史。

**画像、规则和搭配：** 明确偏好写 profile.preferences／cookingStyle／notes，结构模板写 pairingTemplates，用户确认过的具体菜写 exemplars，用户级流程规则写 rules。待确认的 agent 推论不建“已授权落点”。同 structure 的 confirmed 范例 ≥3 道时可提议升模板，用户确认后才写；不改 SKILL.md。原有四层消费（范例 > 模板 > 画像 > 通用）继续适用，健康约束和明确偏好优先。

## ④ Threshold：同日整理

在 Capture 完成后的自然执行点检查原有阈值：当日新反馈 importance 累积 ≥8，或同实体／同类型 ≥3 条。达到时静默整理，不依赖常驻进程。

- merge 只合并同一事实的重复记录，不合并跨补货周期的耗尽、不同实际购买或不同食材。保留原话和历史，重复记录用 mergedInto 指向保留项；不因此再次写库存。
- 用户再次明确确认同一事实可使 importance +1（上限 5）；系统重试、系统提问和沉默均不算确认。状态事实重复不自动升级为长期偏好。
- 新事实取代旧事实时按实际先后标 decayed，不能只凭 capturedAt 新就覆盖旧事实；核对对应数据和未完成落点。
- 同类型 ≥3 条只触发检查，不自动产生偏好；升级沉淀仍需明确内容支持及原有 imp≥4 或重复确认，agent 推论需用户确认。
- 无参考价值的 decayed 记录可标 evicted，日志不删除；尚有未完成且未 superseded 落点的记录不淘汰。importance≥4 不因时间流逝单独淘汰。普通不买／删清单或时间过去不让有效耗尽事实自行失效。

## ⑤ Review：每次生成计划前

1. 读 feedback，按第②节核对未完成且未 superseded 的已授权落点，不限捕获日期或 importance；不从旧建议创建购物写入。
2. 读更新后的 pantry、shopping、profile。对 active、无 mergedInto、stockEvent=depleted 的记录，按 itemKey 核对后续补货事实；有明确取代证据则逐项 decay。当前存在库存但时间冲突未解时，不重放旧删除，也不当作确定缺货推荐。
3. **采购计划**：从仍有效耗尽事实中选择参考，结合画像、偏好、库存、已有 unchecked 清单、本次饭菜目标和数量；不是全部必推。已有待购项避免重复，已有足量库存不补购；当前确认中 removedItemKeys 不自动加回。候选与 applied 无关，不需要 pending/dismissed 补货状态。
4. **每日搭配**：只使用当前已确认购物条目与库存，不把耗尽候选或 confirmation.proposedItems 加入食材池。按更新后的 profile.rules、exemplars、pairingTemplates 和偏好生成。
5. 不从上次删除事件或未回答原因创建补问；补问只挂在本次确认调整中。

<a id="confirmation-flow"></a>
## ⑥ 采购确认：删改先生效，本次补问一次

`shopping.json.confirmation` 只保存当前／最近一份采购建议的确认上下文，字段见 schema；其中 proposedItems 不属于已确认购物条目，也不是反馈日志。

1. 展示新的采购建议时创建 confirmation.id，status=open，保存 proposedItems，removedItemKeys=[]，clarificationAskedAt=null。继续调整同一份建议必须复用该 ID 和已有标记；只有确实开始新计划才换 ID，不能每条消息重新建一轮。
2. 用户删改先更新 proposedItems；单纯删除的不同 itemKey 记入 removedItemKeys 并去重。删 3 个苹果只算一项；改数量或替换不计删除阈值。用户明确重新加入可移出该排除集合。已在正式清单中的明确删除照常执行，但后来单独改一份已确认清单不触发本规则。
3. 完成本次用户明确的删改后，若本轮累计删 ≥3 个不同条目、仍有会影响计划的未知原因且 clarificationAskedAt=null，就围绕最有帮助的未知信息问一次。用户已解释原因就处理事实，不重复问。提问前先把 clarificationAskedAt 写为当前时间，再发送；中断后不自动重发，以“最多一次”为界，不保证消息必达。
4. 例如：“菠菜、芹菜、生菜这几样是家里已有，还是这次不打算买？也可以分别说明。”不要求逐项回答。问题本身不写成 pairing-feedback，不因删满 3 项就固定记 imp 4。
5. 回答“已有／买了”按第③节逐食材处理；“这次不想买”维持当前删除；明确长期偏好按画像处理。未回答只说明原因未知，不猜测、不追问、不阻塞其他请求。以后主动回答时按其事实处理，不重开旧问题。
6. 用户明确确认时，先记录已授权的清单及 confirmation 更新落点，再将调整后的 proposedItems 去重写入 categories.food.items，最后清空已确认的 proposedItems、标 status=confirmed；部分确认只写明确获准的项并将它们移出 proposedItems，其余仍在 open 提案中。若同句既删 ≥3 项又确认，先执行清单更新，再在本次回执补问一次；问不问、答不答均不撤销确认。用户取消整份建议时标 cancelled，不要求解释。确认和问题标记写入中断后，核对条目 ID／itemKey 和已确认范围，不重新添加被删项；同一 confirmation.id 的 clarificationAskedAt 一旦非空，任何恢复或后续调整都不得重置为 null。
7. 后续新计划可以重新选择曾被删的食材；替换 confirmation 时不携带旧 removedItemKeys 或旧问题，也不追问旧原因。旧回答若后来补充，仍可独立作为真实反馈处理。

<a id="legacy-feedback"></a>
## 开发版旧数据

本契约只读写 `feedback.meta.version = "2.0"` 的记录，不解释旧 landing/applied，不做兼容推断。遇到旧反馈文件，将其原样移至同目录唯一命名的 `feedback.legacy-<timestamp>.json`（时间戳使用文件名安全的 YYYYMMDDTHHMMSS，重名则加后缀），再创建 schema 的空 v2 文件；保留 pantry、shopping、profile 和 history。归档失败就保留原文件，不覆盖，并说明具体失败。归档文件不参与 Review；不靠它自动采购、删库存或恢复偏好。这里是开发版重建规则，不是常规 eviction；常规日志只改状态，不删除。
