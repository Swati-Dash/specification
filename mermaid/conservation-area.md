---
title: Conservation area datasets
---
```mermaid
erDiagram
    conservation-area {
        string reference
        string name
        url documentation-url
        wkt geometry
        string notes
        string organisation
        date entry-date
        date start-date
        date end-date
    }
    conservation-area-document {
        string reference
        ref conservation-area
        string name
        url documentation-url
        url document-url
        string document-type
        string notes
        string organisation
        date entry-date
        date start-date
        date end-date
    }
    conservation-area-document ||--o{ conservation-area : references
```
