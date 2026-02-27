---
htb: true
machine: ""
difficulty: ""
os: ""
ip: ""

tags:
  - HTB
  - Enum
  - Exploitation
  - PrivEsc
  - Web
  - Notes

type: writeup

wordlists:
  dir_fuzz: []
  param_fuzz: []
  subdomains: []
  extensions: []
  custom: []
  notes: []

sqli:
  present: false
  methods:
    - union
    - error-based
    - boolean-based
    - time-based
  vector: ""
  payloads: []
  notes: []

xss:
  present: false
  methods:
    - reflected
    - stored
    - blind
  vector: ""
  payloads: []
  notes: []

lfi:
  present: false
  methods:
    - traversal
    - null-byte
  vector: ""
  payloads: []
  notes: []

rce:
  present: false
  methods:
    - command-injection
    - upload
    - deserialization
    - python-rce
    - php-rce
  vector: ""
  payloads: []
  notes: []

passwords:
  present: false
  creds: []
  hashcat:
    used: false
    modes:
      - "0"
      - "1000"
  notes: []

enum_tools:
  - nmap
  - ffuf
  - whatweb
  - burp

enum_findings:
  ports: []
  services: []
  notes: []

privesc:
  present: false
  technique: ""
  vector: ""
  tags:
    - suid-binary
    - writable-script
    - cronjob
    - sudo-misconfig
    - capabilities
    - docker
    - path-hijack
    - kernel-exploit
  tools: []
---

# HTB Writeup Template

## Enumeration

## Exploitation

## PrivEsc

## Notes
