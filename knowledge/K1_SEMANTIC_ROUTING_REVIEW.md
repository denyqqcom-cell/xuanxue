# K1 Semantic Routing Review

Project-side recheck found that attribution cleanup is not yet sufficient to open K2. Source records still conflate physical registry bucket with semantic knowledge domain, and some filename-associated names with author roles.

Examples requiring remediation before K2:

- Fengshui registry contains `周易變占法引論` and `揭露铁板神数之内幕`; registry location is not proof that the work belongs to fengshui.
- Bazi registry contains `梅花心易实战详解` and `火珠林密本`; physical folder ownership must not route these into bazi claim extraction.
- Liuren records for `大六壬探原` currently place 撰者、主编、校者 together in `author`; contributor role must not be collapsed into authorship.

K2 remains blocked until every source has an explicit semantic routing decision independent of local folder placement, and filename contributor roles are separated conservatively.

The next local remediation must preserve all 515 canonical records and hashes, add `knowledge_domains / domain_basis / domain_evidence`, and reset ambiguous contributor-as-author cases rather than infer.

K2 must route by `knowledge_domains`, never by registry folder alone.
