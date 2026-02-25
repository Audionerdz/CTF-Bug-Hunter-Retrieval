# Chunk ID Examples

A comprehensive reference of properly formatted chunk IDs across all domains.

## The Formula

```
<origin>::<domain>::<subdomain>::<intent>::<nnn>
```

| Part | Meaning | Example |
|------|---------|---------|
| `origin` | Type of knowledge | `concept`, `technique`, `exploit` |
| `domain` | Main field | `web`, `linux`, `python` |
| `subdomain` | Specific area | `sql-injection`, `privilege-escalation` |
| `intent` | What the chunk answers | `definition`, `enumeration` |
| `nnn` | 3-digit version | `001`, `002` |

## Web Security

```
concept::web::sql-injection::definition::001
concept::web::xss::definition::001
concept::web::csrf::definition::001
technique::web::sql-injection::union-based::001
technique::web::sql-injection::blind::001
technique::web::sql-injection::time-based::001
technique::web::xss::stored::001
technique::web::xss::reflected::001
technique::web::lfi::path-traversal::001
technique::web::lfi::null-byte-bypass::001
exploit::web::sql-injection::database-enumeration::001
exploit::web::xss::session-stealing::001
exploit::web::lfi::source-code-reading::001
```

## Linux

```
concept::linux::os::file-permissions::001
concept::linux::os::user-management::001
concept::linux::privilege-escalation::definition::001
technique::linux::privilege-escalation::suid-enumeration::001
technique::linux::privilege-escalation::sudo-misconfig::001
technique::linux::privilege-escalation::capability-abuse::001
technique::linux::admin::user-creation::001
technique::linux::admin::service-management::001
reference::linux::commands::file-management::001
reference::linux::commands::text-processing::001
reference::linux::tools::nmap-cheatsheet::001
```

## Python

```
concept::python::syntax::variables::001
concept::python::syntax::data-types::001
concept::python::functions::definition::001
concept::python::data-structures::lists::001
concept::python::data-structures::dicts::001
technique::python::error-handling::try-except::001
technique::python::files::read-write::001
technique::python::oop::class-definition::001
technique::python::async::async-await::001
usecase::python::automation::file-organizer::001
usecase::python::ai::embedding-generation::001
```

## JavaScript

```
concept::javascript::syntax::variables-let-const::001
concept::javascript::functions::arrow-functions::001
concept::javascript::closures::basic-example::001
technique::javascript::dom::query-selector::001
technique::javascript::dom::event-listeners::001
technique::javascript::async::promises::001
technique::javascript::async::async-await::001
technique::javascript::fetch::api-requests::001
```

## HTB Machines

```
htb::gavel::web::enum::nmap-scan::001
htb::gavel::web::enum::git-exposure::001
htb::gavel::web::exploit::git-dumper::001
htb::gavel::web::exploit::rce-chain::001
htb::gavel::system::priv-esc::kernel-exploit::001
htb::facts::web::finding::lfi-vulnerability::001
htb::facts::linux::finding::world-writable-config::001
```

## RAG System (Meta-chunks)

```
guide::rag::chunking::single-intent::001
guide::rag::chunking::chunk-size::001
guide::rag::namespacing::organization::001
procedure::rag::vectorization::openai-embedding::001
procedure::rag::indexing::pinecone-upload::001
reference::rag::chunk-id::schema::001
reference::rag::metadata::fields::001
```

## YouTube Tutorials

```
tutorial::youtube::python::venv-setup::001
tutorial::youtube::python::basic-scripting::001
tutorial::youtube::javascript::dom-basics::001
```

With metadata:

```yaml
---
chunk_id: tutorial::youtube::python::virtualenv-setup::001
domain: python
chunk_type: tutorial
confidence: medium
reuse_level: universal
source: youtube
creator: freeCodeCamp
---
```

The video creator goes in METADATA, not in the chunk_id.

## Good vs Bad IDs

**Good:**

```
concept::web::sql-injection::definition::001
technique::linux::priv-esc::suid-enumeration::001
htb::gavel::web::enum::git-exposure::001
```

**Bad:**

```
chunk_001                           <-- No semantics
concept_sql_injection               <-- Wrong separator (use ::)
htb-gavel-git-exposure::001         <-- Wrong format
web_sql_injection_2026-02-12_001    <-- Date in ID (NO)
concept::web::sql-injection::eng::001  <-- Language in ID (NO)
```

## Versioning

When you improve a chunk:

```
Old:  concept::python::syntax::variables::001
New:  concept::python::syntax::variables::002
```

Keep the old one for version tracking and historical reference.

## Prefix Search

Chunk IDs enable powerful prefix filtering:

```
"technique::web::"     --> All web exploitation techniques
"htb::gavel::"         --> All Gavel machine chunks
"concept::"            --> All foundational concepts
"exploit::web::lfi::"  --> All LFI exploits
```
