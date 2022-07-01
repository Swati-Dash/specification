---
specification: conservation-area
name: conservation area
plural: conservation areas
specification-status: working draft
start-date: ''
end-date: ''
entry-date: '2022-06-09'
datasets:
    - dataset: conservation-area
      fields:
        - field: reference
        - field: name
          description: the official name for the conservation area
        - field: geometry
        - field: documentation-url
          description: an optional URL of a document providing the authoritive source of the boundary. For example a PDF containing a map of the area indicated with a red-line boundary.
        - field: notes
        - field: start-date
        - field: end-date
        - field: entry-date
    - dataset: conservation-area-document
      fields:
        - field: reference
        - field: name
          description: the title of the conservation area document
        - field: documentation-url
          description: the URL of the webpage citing the document
        - field: document-url
          description: the URL of the document
        - field: document-type
          description: "the type of the conservation area document which MUST be one of the following values: 'area-appraisal', 'notice', or blank"
        - field: notes
        - field: start-date
        - field: end-date
        - field: entry-date
---