# Chunk ID Examples and Schema

This page provides comprehensive examples of properly formatted chunk IDs across all domains.

## The Formula (Never Forget)

```
<origin>::<domain>::<subdomain>::<intent>::<nnn>
```

Where:
- `origin` = Type of knowledge (concept, technique, exploit, etc.)
- `domain` = Main field (web, linux, python, rag, etc.)
- `subdomain` = Specific area within domain
- `intent` = What the chunk answers
- `nnn` = 3-digit version (001, 002, etc.)

## Python Programming Examples

### Basics

```
concept::python::syntax::variables::001
concept::python::syntax::data-types::001
concept::python::control-flow::if-else::001
concept::python::control-flow::loops::001
```

### Functions

```
concept::python::functions::definition::001
concept::python::functions::args-kwargs::001
concept::python::functions::return-values::001
```

### Data Structures

```
concept::python::data-structures::lists::001
concept::python::data-structures::dicts::001
concept::python::data-structures::tuples::001
```

### Intermediate

```
technique::python::error-handling::try-except::001
technique::python::files::read-write::001
technique::python::modules::import-system::001
technique::python::venv::environment-setup::001
```

### Advanced

```
technique::python::oop::class-definition::001
technique::python::oop::inheritance::001
technique::python::decorators::basic-usage::001
technique::python::generators::yield-pattern::001
technique::python::async::async-await::001
```

### Real Applications

```
usecase::python::automation::file-organizer::001
usecase::python::scripting::cli-tool::001
usecase::python::web::api-consumption::001
usecase::python::ai::embedding-generation::001
```

## HTML Examples

### Fundamentals

```
concept::html::structure::doctype-html-head-body::001
concept::html::elements::div-span::001
concept::html::elements::semantic-tags::001
concept::html::attributes::id-class::001
```

### Forms

```
concept::html::forms::input-types::001
concept::html::forms::form-submission::001
technique::html::forms::client-validation::001
```

### Best Practices

```
guideline::html::accessibility::aria-basics::001
guideline::html::seo::semantic-markup::001
guideline::html::performance::minimal-dom::001
```

## JavaScript Examples

### Basics

```
concept::javascript::syntax::variables-let-const::001
concept::javascript::data-types::primitive-vs-object::001
concept::javascript::control-flow::if-loops::001
```

### Functions and Scope

```
concept::javascript::functions::arrow-functions::001
concept::javascript::scope::lexical-scope::001
concept::javascript::closures::basic-example::001
```

### DOM and Browser

```
technique::javascript::dom::query-selector::001
technique::javascript::dom::event-listeners::001
technique::javascript::dom::manipulation::001
```

### Async and Modern

```
technique::javascript::async::promises::001
technique::javascript::async::async-await::001
technique::javascript::fetch::api-requests::001
```

### Applications

```
usecase::javascript::web::form-validation::001
usecase::javascript::web::dynamic-content::001
usecase::javascript::security::input-sanitization::001
```

## Web Security Examples

### Concepts

```
concept::web::sql-injection::definition::001
concept::web::xss::definition::001
concept::web::csrf::definition::001
```

### Techniques

```
technique::web::sql-injection::union-based::001
technique::web::sql-injection::blind::001
technique::web::sql-injection::time-based::001
technique::web::xss::stored::001
technique::web::xss::reflected::001
technique::web::lfi::path-traversal::001
technique::web::lfi::null-byte-bypass::001
```

### Exploits

```
exploit::web::sql-injection::database-enumeration::001
exploit::web::sql-injection::file-reading::001
exploit::web::xss::session-stealing::001
exploit::web::lfi::source-code-reading::001
```

## Linux Examples

### Fundamentals

```
concept::linux::os::file-permissions::001
concept::linux::os::user-management::001
concept::linux::os::process-management::001
```

### System Administration

```
technique::linux::admin::user-creation::001
technique::linux::admin::group-management::001
technique::linux::admin::service-management::001
```

### Security and Privilege Escalation

```
concept::linux::privilege-escalation::definition::001
technique::linux::privilege-escalation::suid-enumeration::001
technique::linux::privilege-escalation::sudo-misconfig::001
technique::linux::privilege-escalation::capability-abuse::001
exploit::linux::privilege-escalation::suid-execution::001
```

### Commands and Tools

```
reference::linux::commands::file-management::001
reference::linux::commands::text-processing::001
reference::linux::commands::privilege-escalation::001
reference::linux::tools::nmap-cheatsheet::001
reference::linux::tools::grep-advanced::001
```

## YouTube Tutorial Examples

### General Pattern

```
tutorial::youtube::python::venv-setup::001
tutorial::youtube::python::basic-scripting::001
tutorial::youtube::javascript::dom-basics::001
tutorial::youtube::html::forms-crash-course::001
```

### With Full Metadata

```yaml
---
chunk_id: tutorial::youtube::python::virtualenv-setup::001
domain: python
chunk_type: tutorial
confidence: medium
reuse_level: generic
source: youtube
creator: freeCodeCamp
video_length: "15m"
---

This tutorial explains how to create and activate a Python virtual environment
using venv and pip, with practical examples and best practices.
```

**Important:** The video creator goes in METADATA, not in the chunk_id.

## HTB Machine Examples

### Enumeration Phase

```
htb::gavel::web::enum::nmap-scan::001
htb::gavel::web::enum::git-exposure::001
htb::gavel::web::enum::directory-fuzzing::001
```

### Exploitation Phase

```
htb::gavel::web::exploit::git-dumper::001
htb::gavel::web::exploit::source-analysis::001
htb::gavel::web::exploit::rce-chain::001
```

### Post-Exploitation

```
htb::gavel::system::priv-esc::kernel-exploit::001
htb::gavel::system::priv-esc::sudo-misconfig::001
```

### Findings

```
htb::facts::web::finding::lfi-vulnerability::001
htb::facts::linux::finding::world-writable-config::001
```

## RAG System Examples (Meta-chunks)

### Guiding Principles

```
guide::rag::chunking::single-intent::001
guide::rag::chunking::chunk-size::001
guide::rag::namespacing::organization::001
guide::rag::manifest::structure::001
```

### Procedures

```
procedure::rag::chunking::create-chunk::001
procedure::rag::vectorization::openai-embedding::001
procedure::rag::indexing::pinecone-upload::001
```

### References

```
reference::rag::chunk-id::schema::001
reference::rag::metadata::fields::001
reference::rag::namespace::guidelines::001
```

## Multi-Language Support

### Python (Multiple Languages)

```
concept::python::syntax::variables::en_001
concept::python::syntax::variables::es_001
concept::python::syntax::variables::fr_001
```

Then metadata specifies language:
```yaml
language: en
```

**Pro Tip:** Keep chunk_id clean, put language in metadata.

## Quality Rules

### ✅ GOOD Examples

```
concept::web::sql-injection::definition::001
technique::linux::priv-esc::suid-enumeration::001
htb::gavel::web::enum::git-exposure::001
exploit::web::lfi::null-byte-bypass::001
reference::linux::commands::privilege-escalation::001
tutorial::youtube::python::async-await::001
```

### ❌ BAD Examples

```
chunk_001                           ← No semantics
concept_sql_injection              ← Wrong separator (should be ::)
htb-gavel-git-exposure::001        ← Wrong format
web_sql_injection_2026-02-12_001   ← Date in ID (NO!)
concept::web::sql-injection::eng::001  ← Language in ID (NO!)
technique::web::xss-reflected::001 ← Should be xss::reflected
```

## Versioning Pattern

When you improve a chunk:

```
Old:  concept::python::syntax::variables::001
New:  concept::python::syntax::variables::002
```

Keep the old one for:
- Historical reference
- Version control
- Tracking improvements
- Learning from changes

## Searching by ID Pattern

IDs enable prefix search:

```
GET chunks where chunk_id STARTS WITH "technique::web::"
  → Returns all web exploitation techniques

GET chunks where chunk_id STARTS WITH "htb::gavel::"
  → Returns all Gavel machine chunks

GET chunks where chunk_id STARTS WITH "concept::"
  → Returns all foundational concepts
```

---

**Next:** Learn [Chunk Fields Explained](chunk-fields.md)
