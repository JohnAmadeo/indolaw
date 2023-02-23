# Overview

Indolaw is a proof-of-concept open-source project that consists of 2 components:

a) A Python parser that coverts Indonesian law PDFs into a JSON representation that captures the semantic structure of the law (e.g a law is made of chapters, which are made of paragraphs, which are made of articles, etc.)

b) A Next.js front-end that renders the JSON representation of a law in HTML

# Evaluation / Features

**NOTE:** The UI is entirely in Indonesian, but for some of the demoes below I have utilized Chrome's Google Translation feature to show the UI in English so more people can follow along.

This approach provides a superior UX to traditional law PDFs for several reasons:

1. **Responsive**: Rendered as HTML, the law is easier to read across all device sizes, especially mobile, as it is responsive. PDFs are particularly painful to read on mobile.

![](/assets/responsive.gif)

2. **Table of Contents**:

- Rather than having to first skim the whole PDF to get a sense of what will be covered in the law, the JSON representation extracts a table of contents & renders it as a sidebar. This allows users to quickly understand the law's structure.
- Rather than CTRL+F-ing around in a PDF, users can use the table of contents sidebar to quickly hop between parts of the law

![](/assets/table-of-contents.gif)

3. **URL Linking**: Rendered as HTML, a user can link to a specific article (e.g http://hukumjelas.com/uu/1974/1#pasal-10 links to article 10 of Law 1 of 1974), which is not possible in PDF. This could enable better collaboration among lawyers, or allow journalists to highlight specific articles as they cover the legislative process.

![](/assets/url-linking.gif)

4. **Copy/Paste**: Often, law students or lawyers want to copy text from the PDF into an editor like MS Word, but copy/paste from the PDF into Word often leads to inconsistent formatting. This causes users to waste time cleaning up the formatting in their editor. Rendered as HTML, we ensure copy/paste is done in a format that MS Word and Google Docs understands.

![](/assets/copy-paste.gif)

5. **Side-by-Side Article & Commentary**: In Indonesian laws, after all the articles are listed in the main body, there is an addendum with extended commentary/clarifications on the meaning of various articles. In the PDF, a user has to scroll back-and-forth between an article & its commentary. In the JSON representation, we semantically capture the location of an article & its associated commentary, so that in HTML we can show them side-by-side for easier reading.

![](/assets/side-by-side.gif)

# Inspiration

This project was inspired by my experience taking US law classes while at Yale. Specifically, the existence of software with good UX that democratized access to laws - such as Oyez and Cornell LII - provided the initial spark.

# Contributions

This project was built by Willem Chua, Melissa Lauw, and John Amadeo Daniswara (me).
